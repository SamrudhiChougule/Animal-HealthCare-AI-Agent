import google.generativeai as genai
import os
import sqlite3
import json
from datetime import datetime

# Configure your Gemini API key
genai.configure(api_key=os.getenv('GEMINI_API_KEY', 'AIzaSyC1DizIWFjdlJBx1rc8p89FHv7WhxwGlx8'))

# Initialize model once
model = genai.GenerativeModel("gemini-1.5-flash")

# SQLite database setup
DB_FILE = 'pet_health.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS pet_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        type TEXT NOT NULL,
        age TEXT NOT NULL,
        breed TEXT NOT NULL,
        gender TEXT NOT NULL,
        profile_pic TEXT,
        medical_history TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        messages TEXT NOT NULL,
        date TEXT NOT NULL
    )''')
    conn.commit()
    conn.close()

# Initialize database on import
init_db()

# Conversation state per pet profile
conversation_states = {}

# Vet-style questions
vet_questions = [
    "What symptoms is your pet showing?",
    "How long have the symptoms been present?",
    "Has your pet eaten and drunk normally?",
    "Any past medical conditions or medications?"
]

# Initialize conversation state
def init_conversation(profile_name):
    conversation_states[profile_name] = {
        "asked_questions": [],
        "user_responses": {}
    }

# Step-by-step healthcare advice
def get_healthcare_advice(profile_name, user_response=None):
    # Get or init conversation state
    state = conversation_states.get(profile_name)
    if not state:
        init_conversation(profile_name)
        state = conversation_states[profile_name]

    # Save the previous response
    if user_response and state["asked_questions"]:
        last_q = state["asked_questions"][-1]
        state["user_responses"][last_q] = user_response

    # Ask next question
    for q in vet_questions:
        if q not in state["asked_questions"]:
            state["asked_questions"].append(q)
            return q  # Ask the next question

    # All questions answered → generate final advice
    profiles = get_pet_profiles()
    profile = next((p for p in profiles if p['name'] == profile_name), None)
    if not profile:
        return "⚠️ Pet profile not found."

    prompt = f"""
    You are a professional veterinarian AI assistant.
    Provide short, structured, and safe advice for the pet in clear chunks.
    Pet Profile: {profile}
    User responses to vet questions: {state['user_responses']}
    Structure your response with these sections:
    **Immediate Observations:** What to watch for right now.
    **Emergency Signs:** Red flags that require urgent vet attention.
    **Home Care Tips:** Supportive care you can provide at home.
    **When to See a Vet:** Recommendations for professional help.
    Keep each section concise, use bullet points, and be easy to understand.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating advice: {str(e)}"

# Suggest general care tips
def suggest_care_tips(animal_type):
    prompt = f"Provide short, practical general care tips for {animal_type}."
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error getting tips: {str(e)}"

# Pet profile management
def create_pet_profile(data):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''INSERT INTO pet_profiles (name, type, age, breed, gender, profile_pic, medical_history)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (data.get('name', 'Unknown'),
               data.get('type', 'Unknown'),
               data.get('age', 'Unknown'),
               data.get('breed', 'Unknown'),
               data.get('gender', 'Unknown'),
               data.get('profile_pic', ''),
               json.dumps(data.get('medical_history', []))))
    profile_id = c.lastrowid
    conn.commit()
    conn.close()
    profile = {
        'id': profile_id,
        'name': data.get('name', 'Unknown'),
        'type': data.get('type', 'Unknown'),
        'age': data.get('age', 'Unknown'),
        'breed': data.get('breed', 'Unknown'),
        'gender': data.get('gender', 'Unknown'),
        'profile_pic': data.get('profile_pic', ''),
        'medical_history': data.get('medical_history', [])
    }
    return profile

def get_pet_profiles():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id, name, type, age, breed, gender, profile_pic, medical_history FROM pet_profiles')
    rows = c.fetchall()
    conn.close()
    profiles = []
    for row in rows:
        profiles.append({
            'id': row[0],
            'name': row[1],
            'type': row[2],
            'age': row[3],
            'breed': row[4],
            'gender': row[5],
            'profile_pic': row[6],
            'medical_history': json.loads(row[7]) if row[7] else []
        })
    return profiles

# Chat history management
def save_chat_history(data):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Use profile_name as title if title is not provided
    title = data.get('title') or data.get('profile_name') or 'Untitled Chat'
    c.execute('''INSERT INTO chat_history (title, messages, date)
                 VALUES (?, ?, ?)''',
              (title,
               json.dumps(data.get('messages', [])),
               datetime.now().isoformat()))
    history_id = c.lastrowid
    conn.commit()
    conn.close()
    history = {
        'id': history_id,
        'title': title,
        'messages': data.get('messages', []),
        'date': datetime.now().isoformat()
    }
    return history

def get_chat_history():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id, title, messages, date FROM chat_history ORDER BY date DESC')
    rows = c.fetchall()
    conn.close()
    history = []
    for row in rows:
        history.append({
            'id': row[0],
            'title': row[1],
            'messages': json.loads(row[2]) if row[2] else [],
            'date': row[3]
        })
    return history

def get_chat_history_by_title(title):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id, title, messages, date FROM chat_history WHERE title = ? ORDER BY date DESC', (title,))
    rows = c.fetchall()
    conn.close()
    history = []
    for row in rows:
        history.append({
            'id': row[0],
            'title': row[1],
            'messages': json.loads(row[2]) if row[2] else [],
            'date': row[3]
        })
    return history

def update_pet_profile(profile_id, data):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''UPDATE pet_profiles SET name=?, type=?, age=?, breed=?, gender=?, profile_pic=?, medical_history=? WHERE id=?''',
              (data.get('name', 'Unknown'),
               data.get('type', 'Unknown'),
               data.get('age', 'Unknown'),
               data.get('breed', 'Unknown'),
               data.get('gender', 'Unknown'),
               data.get('profile_pic', ''),
               json.dumps(data.get('medical_history', [])),
               profile_id))
    conn.commit()
    conn.close()
    # Return updated profile
    profiles = get_pet_profiles()
    return next((p for p in profiles if p['id'] == profile_id), None)

def delete_pet_profile(profile_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('DELETE FROM pet_profiles WHERE id=?', (profile_id,))
    conn.commit()
    conn.close()

def delete_chat_history_by_title(title):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('DELETE FROM chat_history WHERE title=?', (title,))
    conn.commit()
    conn.close()
