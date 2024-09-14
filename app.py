from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime

app = Flask(__name__)

# Set up SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///symptom_logs.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db = SQLAlchemy(app)

# Define the SymptomLog model
class SymptomLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    symptom = db.Column(db.String(100), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)

# Create the database and tables
with app.app_context():
    db.create_all()

symptom_logs = []

# Dictionary with all the required symptoms and their details
symptom_medicine = {
    "fever": {
        "medicines": [
            {"name": "Paracetamol", "course": "500mg, 3 times a day, after food"},
            {"name": "Ibuprofen", "course": "400mg, 2 times a day, after food"},
            {"name": "Aspirin", "course": "325mg, 2 times a day, after food"}
        ],
        "disease": "Viral Fever",
        "type": "Infectious",
        "cause": "Viral infection",
        "suggestion": "Rest, hydration, and medication",
        "doctor_consultation": "Consult a doctor if fever persists beyond 3 days"
    },
    "cough": {
        "medicines": [
            {"name": "Dextromethorphan", "course": "10ml, 3 times a day, after food"},
            {"name": "Guaifenesin", "course": "200mg, 3 times a day, after food"},
            {"name": "Bromhexine", "course": "8mg, 2 times a day, after food"}
        ],
        "disease": "Common Cold or Respiratory Infection",
        "type": "Viral or Allergic",
        "cause": "Viral infection or allergens",
        "suggestion": "Stay hydrated, avoid cold drinks, use a humidifier",
        "doctor_consultation": "Consult a doctor if cough lasts longer than 2 weeks"
    },
    "cold": {
        "medicines": [
            {"name": "Cetirizine", "course": "10mg, once a day, after food"},
            {"name": "Phenylephrine", "course": "10mg, 2 times a day, after food"},
            {"name": "Paracetamol", "course": "500mg, 3 times a day, after food"}
        ],
        "disease": "Common Cold",
        "type": "Viral",
        "cause": "Rhinovirus infection",
        "suggestion": "Drink warm fluids, rest, and take medications",
        "doctor_consultation": "Consult a doctor if cold symptoms worsen"
    },
    "headache": {
        "medicines": [
            {"name": "Ibuprofen", "course": "400mg, 2 times a day, after food"},
            {"name": "Acetaminophen", "course": "500mg, 3 times a day, after food"},
            {"name": "Aspirin", "course": "325mg, 2 times a day, after food"}
        ],
        "disease": "Tension Headache or Migraine",
        "type": "Neurological",
        "cause": "Stress, lack of sleep, or dehydration",
        "suggestion": "Rest in a quiet, dark room, stay hydrated",
        "doctor_consultation": "Consult a doctor if headaches are recurrent"
    },
    
    "fatigue": {
        "medicines": [
            {"name": "Iron supplements", "course": "325mg, once a day, after food"},
            {"name": "Vitamin D3", "course": "1000 IU, once a day, after food"},
            {"name": "Multivitamins", "course": "1 tablet, once a day, after food"}
        ],
        "disease": "Anemia or Vitamin Deficiency",
        "type": "Systemic",
        "cause": "Nutritional deficiency or chronic illness",
        "suggestion": "Rest, eat balanced meals, and consider supplements",
        "doctor_consultation": "Consult a doctor if fatigue persists for over a week"
    },
    
    "vomiting": {
        "medicines": [
            {"name": "Ondansetron", "course": "4mg, 3 times a day, before food"},
            {"name": "Domperidone", "course": "10mg, 3 times a day, before food"},
            {"name": "Metoclopramide", "course": "10mg, 3 times a day, before food"}
        ],
        "disease": "Food Poisoning or Gastroenteritis",
        "type": "Digestive",
        "cause": "Contaminated food or viral infection",
        "suggestion": "Stay hydrated, eat bland foods",
        "doctor_consultation": "Consult a doctor if vomiting persists beyond 24 hours"
    },
    "rash": {
        "medicines": [
            {"name": "Hydrocortisone Cream", "course": "Apply 2-3 times a day, after food"},
            {"name": "Cetirizine", "course": "10mg, once a day, after food"},
            {"name": "Diphenhydramine", "course": "25mg, 2 times a day, after food"}
        ],
        "disease": "Allergic Reaction or Dermatitis",
        "type": "Dermatological",
        "cause": "Allergens, contact with irritants",
        "suggestion": "Avoid known allergens, use anti-itch cream",
        "doctor_consultation": "Consult a doctor if rash worsens or persists"
    },
    
    "stomach_pain": {
        "medicines": [
            {"name": "Omeprazole", "course": "20mg, once a day, before food"},
            {"name": "Ranitidine", "course": "150mg, 2 times a day, after food"},
            {"name": "Dicyclomine", "course": "20mg, 3 times a day, after food"}
        ],
        "disease": "Gastritis or Indigestion",
        "type": "Digestive",
        "cause": "Acid reflux or stomach inflammation",
        "suggestion": "Eat small meals, avoid spicy foods, stay hydrated",
        "doctor_consultation": "Consult a doctor if pain persists for more than 3 days"
    },
    "diarrhea": {
        "medicines": [
            {"name": "Loperamide", "course": "2mg, after each loose stool, max 8mg per day"},
            {"name": "Oral Rehydration Solution (ORS)", "course": "As needed, after each episode of diarrhea"},
            {"name": "Probiotic", "course": "As recommended, once a day"}
        ],
        "disease": "Gastroenteritis or Food Poisoning",
        "type": "Infectious or Digestive",
        "cause": "Bacterial or viral infection, food contamination",
        "suggestion": "Stay hydrated with ORS, avoid solid foods initially",
        "doctor_consultation": "Consult a doctor if diarrhea lasts more than 2 days"
    },
    "sore_throat": {
        "medicines": [
            {"name": "Amoxicillin", "course": "500mg, 3 times a day, after food"},
            {"name": "Paracetamol", "course": "500mg, 3 times a day, after food"},
            {"name": "Throat Lozenges", "course": "As needed, throughout the day"}
        ],
        "disease": "Pharyngitis or Tonsillitis",
        "type": "Infectious",
        "cause": "Viral or bacterial infection",
        "suggestion": "Gargle with warm salt water, avoid cold drinks",
        "doctor_consultation": "Consult a doctor if symptoms worsen or if there’s difficulty swallowing"
    },
    "vomiting": {
        "medicines": [
            {"name": "Ondansetron", "course": "4mg, 2 times a day, after food"},
            {"name": "Domperidone", "course": "10mg, 3 times a day, before food"},
            {"name": "ORS", "course": "As needed, to prevent dehydration"}
        ],
        "disease": "Gastroenteritis or Motion Sickness",
        "type": "Digestive or Neurological",
        "cause": "Viral infection, food poisoning, or motion sickness",
        "suggestion": "Stay hydrated, eat small, bland meals",
        "doctor_consultation": "Consult a doctor if vomiting persists for more than 24 hours"
    },
    "allergy": {
        "medicines": [
            {"name": "Loratadine", "course": "10mg, once a day, after food"},
            {"name": "Cetirizine", "course": "10mg, once a day, after food"},
            {"name": "Hydrocortisone Cream", "course": "Apply to affected area, 2 times a day"}
        ],
        "disease": "Allergic Reaction",
        "type": "Immunological",
        "cause": "Exposure to allergens like pollen, dust, or pet dander",
        "suggestion": "Avoid allergens, use air purifiers, and take prescribed medication",
        "doctor_consultation": "Consult a doctor if symptoms persist or worsen"
    },
    "back_pain": {
        "medicines": [
            {"name": "Ibuprofen", "course": "400mg, 3 times a day, after food"},
            {"name": "Naproxen", "course": "250mg, 2 times a day, after food"},
            {"name": "Paracetamol", "course": "500mg, 3 times a day, after food"}
        ],
        "disease": "Muscle Strain or Disc Herniation",
        "type": "Musculoskeletal",
        "cause": "Poor posture, overuse, or injury",
        "suggestion": "Apply heat or cold, gentle stretching exercises",
        "doctor_consultation": "Consult a doctor if pain persists for more than a week"
    },
    "constipation": {
        "medicines": [
            {"name": "Psyllium Husk", "course": "5g, once a day, with water"},
            {"name": "Bisacodyl", "course": "5mg, once a day, before bed"},
            {"name": "Lactulose", "course": "15ml, once a day, after food"}
        ],
        "disease": "Chronic Constipation",
        "type": "Digestive",
        "cause": "Low fiber diet, dehydration, or lack of exercise",
        "suggestion": "Increase fiber intake, drink plenty of water, exercise regularly",
        "doctor_consultation": "Consult a doctor if constipation lasts more than 5 days"
    },
    "dizziness": {
        "medicines": [
            {"name": "Betahistine", "course": "16mg, 3 times a day, after food"},
            {"name": "Meclizine", "course": "25mg, 2 times a day, after food"},
            {"name": "Prochlorperazine", "course": "5mg, 3 times a day, after food"}
        ],
        "disease": "Vertigo or Low Blood Pressure",
        "type": "Neurological or Cardiovascular",
        "cause": "Inner ear issues, low blood pressure, dehydration",
        "suggestion": "Stay hydrated, avoid sudden movements",
        "doctor_consultation": "Consult a doctor if dizziness persists for more than 3 days"
    },
    


}

def identify_symptoms(user_input):
    symptoms = []
    for symptom in symptom_medicine.keys():
        if symptom in user_input:
            symptoms.append(symptom)
    return symptoms

def log_symptom_to_db(symptom):
    new_log = SymptomLog(symptom=symptom)
    db.session.add(new_log)
    db.session.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/medicine', methods=['POST'])
def symptom_medicine_route():
    user_input = request.json.get('symptom', "").lower()
    identified_symptoms = identify_symptoms(user_input)

    if identified_symptoms:
        responses = []
        for idx, symptom in enumerate(identified_symptoms, start=1):
            medicines = symptom_medicine[symptom]["medicines"]

            # Build the medicine table
            table = "<table border='1'><tr><th>S.No</th><th>Medicine Name</th><th>Course</th></tr>"
            for i, medicine in enumerate(medicines, start=1):
                table += f"<tr><td>{i}</td><td>{medicine['name']}</td><td>{medicine['course']}</td></tr>"
            table += "</table>"

            # Append the extra information about the symptom
            response = (
                f"<h3>Symptom: {symptom.capitalize()}</h3>{table}<br>"
                f"<b>Disease:</b> {symptom_medicine[symptom]['disease']}<br>"
                f"<b>Type:</b> {symptom_medicine[symptom]['type']}<br>"
                f"<b>Cause:</b> {symptom_medicine[symptom]['cause']}<br>"
                f"<b>Suggestion:</b> {symptom_medicine[symptom]['suggestion']}<br>"
                f"<b>Doctor Consultation:</b> {symptom_medicine[symptom]['doctor_consultation']}<br><br>"
            )
            responses.append(response)
            symptom_logs.append({"symptom": symptom, "time": datetime.now()})

            log_symptom_to_db(symptom)

        return jsonify({"response": " ".join(responses)})
    else:
        return jsonify({"response": "Please mention your symptoms (e.g., fever, cough, headache, etc.)."})

@app.route('/logs', methods=['GET'])
def get_logs():
    logs = SymptomLog.query.all()
    response = "<h3>Symptom Logs:</h3><ul>"
    for log in logs:
        response += f"<li>{log.symptom} logged at {log.time}</li>"
    response += "</ul>"
    return response

if __name__ == '__main__':
    app.run(debug=True)
