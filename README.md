# Rakshak AI – Intelligent Disaster Response System

Rakshak AI is an **AI-powered disaster response and alert system** designed to analyze disaster-related messages, detect emergencies, identify disaster types, determine affected locations, estimate severity levels, and provide real-time alerts and safety precautions to users and rescue teams.

The system helps improve **disaster awareness, response coordination, and public safety** by combining **Machine Learning, NLP, geolocation mapping, and automated notifications**.

---

## Features

### 1. Disaster Detection

* Analyzes incoming disaster-related messages.
* Detects whether the message indicates a disaster or not.
* Filters out irrelevant messages.

### 2. Disaster Classification

* Identifies disaster types such as:

  * Flood
  * Earthquake
  * Cyclone
  * Wildfire
  * Tornado

### 3. Location Extraction

* Extracts affected locations from incoming messages.
* Displays disaster locations on an interactive map.

### 4. Severity Prediction

* Predicts severity levels:

  * Minor
  * Moderate
  * Severe
  * Catastrophic

### 5. Real-Time Dashboard

* Shows:

  * Recent disaster messages
  * Disaster type
  * Location
  * Severity
  * Map visualization with color-coded markers

### 6. Alert Notification System

* Sends alerts to registered users in affected areas.
* Supports:

  * SMS alerts 

### 7. Disaster Precaution Guidance

Provides safety instructions for:

* Before disaster
* During disaster
* After disaster

### 8. Rescue Team Monitoring

* Gives rescue teams region-wise disaster insights.
* Helps prioritize emergency response based on severity.

### 9. Simulation Mode

* Processes predefined disaster messages in batches.
* Useful when live API data is unavailable.

### 10. Integrated Chatbot

* A floating chatbot available on all pages.
* Answers disaster-related safety and awareness questions.

## 11. Mobile Application Support

Rakshak AI also includes a **mobile application** that allows users to stay informed about disasters and receive alerts directly on their smartphones.

### Mobile App Features

* User registration and login
* Real-time disaster alerts
* Location-based notifications
* View nearby disaster reports
* Safety precautions for disasters
* Chatbot support for emergency guidance
* Rescue alerts and emergency updates

The mobile application improves accessibility by ensuring that users receive **instant disaster warnings and precautionary guidance on the go**, helping them respond quickly during emergencies.

### Mobile Tech Stack

* React Native

The mobile app connects with the Rakshak AI backend to fetch:

* Disaster reports
* Alert notifications
* Safety guidelines
* User-specific location alerts

---

## Tech Stack

### Frontend

* HTML
* CSS
* JavaScript
* Bootstrap

### Backend

* Python
* Flask

### Database

* MySQL

### AI / ML / NLP

* Scikit-learn
* Pandas
* Natural Language Processing
* all-MiniLM-L6-v2 model+Logistic Regression

### APIs / Services

* Leaflet.js for map visualization
* Nominatim API for coordinates extraction of a location
* Overpass API to display nearby safe places
---

## System Workflow

1. User messages are collected from:

   * Simulation dataset
   * User reports
   * Twitter/X API *(future implementation)*

2. Messages are processed by the AI model to:

   * Detect disasters
   * Classify disaster type
   * Extract location
   * Estimate severity

3. Results are stored in the MySQL database.

4. Dashboard displays:

   * Processed messages
   * Disaster markers on the map
   * Severity indicators

5. If reports in the same region exceed a threshold:

   * Alerts are sent to nearby registered users

6. Users can access:

   * Safety precautions
   * Chatbot assistance

---

## Project Structure

Rakshak-AI/
│── static/
│   │── css/
│   │── js/
│   │── images/
│
│── templates/
│   │── index.html
│   │── dashboard.html
│   │── login.html
│   │── register.html
│   │── precautions.html
│
│── model/
│   │── disaster_model.pkl
│
│── app.py
│── requirements.txt
│── README.md


---

## Installation and Setup

### 1. Clone the Repository


git clone https://github.com/sohanasri1806/rakshak-ai.git
cd rakshak-ai


### 2. Create Virtual Environment

python -m venv venv


### 3. Activate Virtual Environment

**Windows**

venv\Scripts\activate

**Linux / Mac**

source venv/bin/activate


### 4. Install Dependencies


pip install -r requirements.txt


### 5. Configure Database

Create a MySQL database and update credentials in `app.py`.

CREATE DATABASE rakshak_ai;

### 6. Run the Application

python app.py


### 7. Open in Browser

http://127.0.0.1:5000

---

## Future Enhancements

* Live Twitter/X disaster message integration
* Real-time background processing
* WhatsApp emergency alerts
* Advanced location clustering
* Multi-language disaster alerts
* Voice based assistant
* AI-based rescue resource allocation

---

## Impact

Rakshak AI aims to:

* Improve disaster preparedness
* Enable faster emergency response
* Provide timely alerts to citizens
* Support rescue teams with actionable insights
* Reduce disaster-related risks and losses

---

## Contributors

**Project Name:** Rakshak AI
**Developed By:** 
K. Manya Sree
D. Shiva Sohanasri
G. Rishika

---

## Screenshots
<img width="574" height="237" alt="image" src="https://github.com/user-attachments/assets/83f009ad-a749-4112-a771-a340795ce6a4" />
<img width="332" height="265" alt="image" src="https://github.com/user-attachments/assets/eec070ed-1741-488c-a52c-7bfb32da1b35" />
<img width="563" height="278" alt="image" src="https://github.com/user-attachments/assets/fb7c37d2-79a6-4802-aea4-2b787a02051a" />
<img width="563" height="266" alt="image" src="https://github.com/user-attachments/assets/74750738-4338-4b97-b2df-580a91d5bcfd" />
<img width="555" height="258" alt="image" src="https://github.com/user-attachments/assets/db4b6eed-c117-4f88-b177-76a0de0ad9cc" />
<img width="284" height="416" alt="image" src="https://github.com/user-attachments/assets/8d0f1b6f-2035-489d-aaa7-a3446e0dc8db" />
<img width="564" height="283" alt="image" src="https://github.com/user-attachments/assets/5dcbce4c-f99b-435e-b20b-19ceb1482f50" />
<img width="394" height="563" alt="image" src="https://github.com/user-attachments/assets/d561e0e4-dfc5-46c4-9b3b-7c0b243cb1ac" />









