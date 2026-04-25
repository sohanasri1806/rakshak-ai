import spacy
import joblib # Used to load saved models
from sentence_transformers import SentenceTransformer

# 1. Load the shared Embedding Model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 2. Load Spacy for Location Extraction
nlp = spacy.load("en_core_web_sm")

# 3. Load your Pre-trained Classifiers (Assumes you saved them)
# For now, if you haven't saved them yet, you'll need to keep the 
# training code, but it's better to save them as .pkl files.
try:
    disaster_classifier = joblib.load('models/disaster_clf.pkl')
    type_classifier = joblib.load('models/type_clf.pkl')
    severity_classifier = joblib.load('models/severity_clf.pkl')
    severity_encoder = joblib.load('models/severity_encoder.pkl')
except:
    print("Warning: Model files not found. Run training script first.")

# --- CONSTANTS ---
NEGATION_WORDS = ["no threat","no tsunami","no danger","no risk", "false alarm", "safe", "all clear"]

SEVERITY_KEYWORDS = {
    "Catastrophic": ["destroyed","massive destruction","many dead"],
    "Severe": ["collapsed","major damage","evacuated","rapid"],
    "Moderate": ["strong","moderate","roads flooded","houses flooded","power outage"],
    "Minor": ["light tremor","minor flooding","small fire"]
}

# --- UTILITY FUNCTIONS ---
def extract_location(text):
    doc = nlp(text)
    for ent in doc.ents:
        if ent.label_ in ["GPE","LOC"]:
            return ent.text
    return "Unknown"

def has_negation(text):
    text = text.lower()
    return any(word in text for word in NEGATION_WORDS)

def predict_severity(message):
    text = message.lower()
    for level, words in SEVERITY_KEYWORDS.items():
        if any(w in text for w in words): return level
    
    emb = model.encode([message])
    pred = severity_classifier.predict(emb)[0]
    return severity_encoder.inverse_transform([pred])[0]

# --- THE MAIN PIPELINE FOR THE WEBSITE ---
def analyze_message(message):
    text_lower = message.lower()

    # -------------------------------
    # 🔹 Step 1: Negation Check
    # -------------------------------
    if has_negation(message):
        return {"message": message, "disaster": False, "confidence": 0.0}

    # -------------------------------
    # 🔹 Step 2: ML Prediction
    # -------------------------------
    emb = model.encode([message])
    prob = disaster_classifier.predict_proba(emb)[0][1]

    # -------------------------------
    # 🔥 Step 3: KEYWORD FALLBACK
    # -------------------------------
    disaster_keywords = {
        "Flood": ["flood", "flooding", "water", "rain", "overflow"],
        "Earthquake": ["earthquake", "tremor", "quake"],
        "Wildfire": ["fire", "wildfire", "smoke"],
        "Hurricane": ["hurricane", "cyclone", "storm"],
        "Tornado": ["tornado"]
    }

    detected_type = "Unknown"

    for d_type, words in disaster_keywords.items():
        if any(word in text_lower for word in words):
            detected_type = d_type
            break

    # -------------------------------
    # 🔹 Step 4: Decision Logic
    # -------------------------------
    if prob < 0.5:
        # 👉 If ML fails but keyword found → STILL treat as disaster
        if detected_type != "Unknown":
            location = extract_location(message)
            severity = predict_severity(message)

            return {
                "message": message,
                "disaster": True,
                "confidence": round(prob, 3),
                "type": detected_type,
                "location": location,
                "severity": severity
            }

        return {
            "message": message,
            "disaster": False,
            "confidence": round(prob, 3)
        }

    # -------------------------------
    # 🔹 Step 5: ML Success Case
    # -------------------------------
    disaster_type = type_classifier.predict(emb)[0]
    location = extract_location(message)
    severity = predict_severity(message)

    return {
        "message": message,
        "disaster": True,
        "confidence": round(prob, 3),
        "type": disaster_type,
        "location": location,
        "severity": severity
    }