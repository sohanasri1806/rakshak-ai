from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_mysqldb import MySQL
import bcrypt
import os
from google import generativeai
import trafilatura
import requests
from geopy.geocoders import Nominatim
from twilio.rest import Client

# Import your custom modules
from model_logic import analyze_message
from simulation_data import SIMULATED_MESSAGES
from flask_cors import CORS

# Get absolute path for templates and static folders
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
CORS(app) # Allows external mobile access

app.secret_key = os.urandom(24)

# --- MySQL Configuration ---
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'XXXXX' 
app.config['MYSQL_DB'] = 'rakshak_db'

mysql = MySQL(app)

# --- External Services Config ---
geolocator = Nominatim(user_agent="rakshak_ai", timeout=10)
# Twilio Setup (Replace with your actual credentials)
import os
TWILIO_SID = os.environ.get('TWILIO_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')  # Twilio Sandbox Number

# Global index to track simulation batches
sim_state = {"index": 0}

GUIDELINES_DATA = {
    'Earthquake': {
        'before': [ 'Secure heavy furniture to walls',
            'Keep emergency supplies ready (water, food, first aid)',
            'Know how to turn off gas and electricity',
            'Practice drop, cover, and hold on technique',
            'Keep important documents in safe place'],
        'during': ['Drop to hands and knees immediately',
            'Take cover under sturdy desk or table',
            'Hold on until shaking stops',
            'If outdoors, move away from buildings',
            'If in vehicle, stay inside with seatbelt on',
            'Never use elevators'],
        'after': ['Check for injuries and provide first aid',
            'Inspect home for damage',
            'Shut off gas if you smell it',
            'Turn on radio for emergency information',
            'Use phone only for emergencies',
            'Expect aftershocks']
    },
    'Flood': {
        'before': ['Know evacuation routes in your area',
            'Assemble emergency kit with water and food',
            'Store important documents in waterproof container',
            'Keep sandbags available',
            'Install check valves in plumbing',
            'Trim trees and clear gutters'],
        'during': [ 'Evacuate immediately if ordered',
            'Move to higher ground',
            'Avoid walking/driving through flood water',
            'Turn off electricity if water is rising',
            'Do not attempt to rescue others unless trained',
            'Keep away from power lines'],
        'after': ['Return home only when authorities say it is safe',
            'Document property damage with photos',
            'Clean contaminated surfaces',
            'Check for structural damage',
            'Boil water before drinking if advised',
            'Dispose of contaminated food']
    },
    'Wildfire': {
        'before': [ 'Create 100-foot defensible space around home',
            'Use fire-resistant roofing and siding materials',
            'Keep gutters clean and free of leaves',
            'Maintain trees and remove dead branches',
            'Prepare emergency evacuation kit',
            'Know evacuation routes and designated shelters'],
        'during': ['Evacuate immediately if ordered',
            'Close all windows and doors',
            'Remove lightweight curtains',
            'Turn off natural gas at meter',
            'Leave outdoor lights on',
            'Drive with headlights on'],
        'after': [ 'Return home only when authorities declare it safe',
            'Watch for hot spots in vegetation',
            'Check roof and attic for embers',
            'Wear protective clothing while cleaning',
            'Document damage for insurance',
            'Contact your insurance company']
    },
    'Hurricane': {
        'before': [ 'Install storm shutters on windows',
            'Trim trees regularly',
            'Reinforce roof and garage doors',
            'Stock emergency supplies for 1 week',
            'Create family communication plan',
            'Secure outdoor items or bring them inside'],
        'during': [  'Stay indoors away from windows',
            'Go to interior room on lowest floor',
            'Listen to weather updates constantly',
            'Keep flashlights and batteries ready',
            'Do not go outside even if it seems calm',
            'Stay in shelter until all-clear given'],
        'after': [ 'Check for injuries and provide aid',
            'Survey property for damage',
            'Take photos for insurance claims',
            'Clear debris and standing water',
            'Avoid downed power lines',
            'Boil water if advisories issued'
        ]
    },
    'Tornado': {
        'before': [ 'Identify a safe room in your home (basement or interior room)',
            'Practice tornado drills with family',
            'Know the difference between watch and warning',
            'Install weather alert radio',
            'Keep important documents accessible',
            'Trim trees near your home'],
        'during': ['Go to safe room immediately',
            'Stay away from windows',
            'Cover yourself with mattress or blankets',
            'Close all interior doors',
            'If in car, drive away from tornado path',
            'If caught outside, lie flat in ditch or low area'],
        'after': [ 'Check for injuries and provide first aid',
            'Inspect home for structural damage',
            'Stay out of damaged buildings',
            'Use flashlights not candles',
            'Avoid walking through debris',
            'Document damage for insurance']
    }
}

generativeai.configure(api_key="XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")
model = generativeai.GenerativeModel('gemini-2.5-flash') # Updated to a stable model version

# --- HELPER: WHATSAPP ALERT ---
def send_phone_alert(phone, d_type, loc, sev):
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        guideline = GUIDELINES_DATA.get(d_type, {}).get('during', ['Stay safe'])[0]
        body = f"🚨 *RAKSHAK AI ALERT* 🚨\n\n*Type:* {d_type}\n*Loc:* {loc}\n*Severity:* {sev}\n*Action:* {guideline}"
        client.messages.create(body=body, from_=TWILIO_PHONE_NUMBER, to=phone)
    except Exception as e:
        print(f"Twilio Error: {e}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/health', methods=['GET'])
def health():   
    return jsonify({"status": "healthy", "message": "API is running"}), 200

@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        phone = data.get('phone')
        loc_name = data.get('location')
        password_raw = data.get('password')

        # Validations
        if not all([name, email, phone, loc_name, password_raw]):
            return jsonify({"status": "error", "message": "All fields required!"}), 400
        if len(password_raw) < 8:
            return jsonify({"status": "error", "message": "Password must be at least 8 characters!"}), 400

        # Extract Coordinates
        try:
            geo = geolocator.geocode(loc_name)
            lat, lng = (geo.latitude, geo.longitude) if geo else (None, None)
        except:
            lat, lng = None, None

        hashed = bcrypt.hashpw(password_raw.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        cur = mysql.connection.cursor()
        try:
            cur.execute("""INSERT INTO users(name, email, password, phone_no, location, latitude, longitude) 
                           VALUES (%s, %s, %s, %s, %s, %s, %s)""", 
                        (name, email, hashed, phone, loc_name, lat, lng))
            mysql.connection.commit()
            return jsonify({"status": "success", "message": "Account created! Coordinates extracted."}), 201
        except Exception as e:
            return jsonify({"status": "error", "message": "Email already registered."}), 409
        finally:
            cur.close()
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        # Validation
        if not email or not password:
            return jsonify({"status": "error", "message": "Email and password required."}), 400
        
        password_candidate = password.encode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("SELECT id, name, password FROM users WHERE email = %s", [email])
        user = cur.fetchone()
        cur.close()

        if user and bcrypt.checkpw(password_candidate, user[2].encode('utf-8')):
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return jsonify({"status": "success", "user_id": user[0], "name": user[1], "redirect": url_for('dashboard')})
        return jsonify({"status": "error", "message": "Invalid email or password."}), 401
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('index'))
    return render_template('dashboard.html', name=session['user_name'])

@app.route('/api/simulate', methods=['GET'])
def simulate():
    try:
        idx = sim_state["index"]
        batch = SIMULATED_MESSAGES[idx: idx + 10]
        sim_state["index"] = (idx + 10) % len(SIMULATED_MESSAGES)

        results = []
        disaster_counts = {}

        for item in batch:
            try:
                raw = analyze_message(item['text'])
                analysis = raw[0] if isinstance(raw, tuple) else raw

                # ✅ Get location from model
                location_name = analysis.get('location')

                if not location_name or location_name == "Unknown":
                    continue

                # ✅ Convert to coordinates
                geo = geolocator.geocode(location_name)
                if not geo:
                    continue

                analysis['lat'] = geo.latitude
                analysis['lng'] = geo.longitude

                results.append(analysis)

                # ✅ Disaster handling
                if analysis.get('disaster'):
                    loc = f"{analysis['lat']},{analysis['lng']}"
                    disaster_counts[loc] = disaster_counts.get(loc, 0) + 1

                    # 🔥 FOR TESTING → use 1 instead of 5
                    if disaster_counts[loc] >= 1:
                        cur = mysql.connection.cursor()

                        cur.execute("""
                            SELECT phone_no FROM users 
                            WHERE ABS(latitude - %s) < 0.05 
                            AND ABS(longitude - %s) < 0.05
                        """, (analysis['lat'], analysis['lng']))

                        users = cur.fetchall()

                        print("📍 Location:", location_name)
                        print("👥 Users found:", users)

                        for u in users:
                            send_phone_alert(
                                u[0],
                                analysis.get('type'),
                                location_name,
                                analysis.get('severity')
                            )

                        cur.close()

            except Exception as e:
                print(f"Error analyzing message: {e}")
                continue

        return jsonify(results), 200

    except Exception as e:
        print(f"Simulate error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/analyze_url', methods=['POST'])
def analyze_url():
    data = request.json
    url = data.get('url')
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        text = trafilatura.extract(response.text)
        if not text: return jsonify({"status": "error", "message": "No content found."})
        
        raw = analyze_message(text[:1000])
        analysis = raw[0] if isinstance(raw, tuple) else raw
        if analysis.get('disaster'):
            analysis['guidelines'] = GUIDELINES_DATA.get(analysis.get('type'))
            
        return jsonify({"status": "success", "data": analysis})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})

@app.route('/api/chat', methods=['POST'])
def chat():
    user_query = request.json.get('message')
    system_instruction = "You are Rakshak AI. Answer ONLY disaster-related safety queries."
    try:
        response = model.generate_content(f"{system_instruction}\n\nUser: {user_query}")
        return jsonify({"reply": response.text})
    except:
        return jsonify({"reply": "System busy."}), 500

import requests

@app.route('/api/nearby_safe_places', methods=['POST'])
def get_real_safe_places():
    data = request.json
    lat = data.get('lat')
    lng = data.get('lng')

    # Fallback to Database if frontend didn't send live GPS
    if not lat or not lng:
        if 'user_id' in session:
            cur = mysql.connection.cursor()
            cur.execute("SELECT latitude, longitude FROM users WHERE id = %s", [session['user_id']])
            user_coords = cur.fetchone()
            cur.close()
            if user_coords and user_coords[0]:
                lat, lng = float(user_coords[0]), float(user_coords[1])
            else:
                return jsonify({"status": "error", "message": "No location available."})
        else:
            return jsonify({"status": "error", "message": "Please login."})

    # Fetch REAL data from OpenStreetMap (Overpass API)
    # This query looks for hospitals and fire stations within 5km (5000m)
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
      node["amenity"="hospital"](around:5000,{lat},{lng});
      node["amenity"="fire_station"](around:5000,{lat},{lng});
      node["emergency"="shelter"](around:5000,{lat},{lng});
    );
    out body;
    """
    try:
        print(f"[DEBUG] Fetching safe places for lat={lat}, lng={lng}")
        headers = {
            'User-Agent': 'rakshak-ai-app',
            'Accept': 'application/json',
        }
        response = requests.get(overpass_url, params={'data': overpass_query}, headers=headers, timeout=30)
        response.raise_for_status()
        osm_data = response.json()
        
        print(f"[DEBUG] Overpass API returned {len(osm_data.get('elements', []))} elements")
        
        places = []
        for element in osm_data.get('elements', []):
            places.append({
                "name": element.get('tags', {}).get('name', 'Emergency Facility'),
                "type": element.get('tags', {}).get('amenity', 'Shelter').capitalize(),
                "lat": element['lat'],
                "lng": element['lon']
            })
        print(f"[DEBUG] Returning {len(places)} formatted places")
        return jsonify({"status": "success", "places": places, "center": [lat, lng]})
    except requests.exceptions.Timeout:
        print(f"[ERROR] Overpass API timeout")
        return jsonify({"status": "error", "message": "API request timeout. Please try again."}), 504
    except requests.exceptions.ConnectionError:
        print(f"[ERROR] Overpass API connection error")
        return jsonify({"status": "error", "message": "Cannot reach Overpass API. Check your internet connection."}), 503
    except Exception as e:
        print(f"[ERROR] Safe places error: {str(e)}")
        return jsonify({"status": "error", "message": f"Service error: {str(e)}"}), 500
    
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,debug=True)