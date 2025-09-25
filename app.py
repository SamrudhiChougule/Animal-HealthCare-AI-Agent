from flask import Flask, render_template, request, jsonify
from agent import get_healthcare_advice, suggest_care_tips, create_pet_profile, get_pet_profiles, save_chat_history, get_chat_history, get_chat_history_by_title, update_pet_profile, delete_pet_profile, delete_chat_history_by_title

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/advice', methods=['POST'])
def advice():
    data = request.json
    profile_name = data.get('profile_name')
    user_response = data.get('user_response')
    advice = get_healthcare_advice(profile_name, user_response)
    return jsonify({'advice': advice})


@app.route('/tips', methods=['POST'])
def tips():
    data = request.json
    animal_type = data.get('animal_type')
    tips = suggest_care_tips(animal_type)
    return jsonify({'tips': tips})

@app.route('/create_profile', methods=['POST'])
def create_profile():
    data = request.json
    profile = create_pet_profile(data)
    return jsonify({'profile': profile})

@app.route('/get_profiles', methods=['GET'])
def get_profiles():
    profiles = get_pet_profiles()
    return jsonify({'profiles': profiles})

@app.route('/save_history', methods=['POST'])
def save_history():
    data = request.json
    history = save_chat_history(data)
    return jsonify({'history': history})

@app.route('/get_history', methods=['GET'])
def get_history():
    history = get_chat_history()
    return jsonify({'history': history})

@app.route('/get_history/<title>', methods=['GET'])
def get_history_by_title(title):
    history = get_chat_history_by_title(title)
    return jsonify({'history': history})

@app.route('/edit_profile/<int:profile_id>', methods=['PUT'])
def edit_profile(profile_id):
    data = request.json
    profile = update_pet_profile(profile_id, data)
    return jsonify({'profile': profile})

@app.route('/delete_profile/<int:profile_id>', methods=['DELETE'])
def delete_profile(profile_id):
    delete_pet_profile(profile_id)
    return jsonify({'message': 'Profile deleted'})

@app.route('/delete_history/<title>', methods=['DELETE'])
def delete_history(title):
    delete_chat_history_by_title(title)
    return jsonify({'message': 'History deleted'})

if __name__ == '__main__':
    app.run(debug=True)
