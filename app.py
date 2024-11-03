from flask import Flask, render_template, request, jsonify
import base64
import requests
import google.generativeai as ai

from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# API Keys
PLANT_API_KEY = 'DCvGCUOqBk0kSUmGMrJAKNDUQ95Uq5l1ajMbzFgVObOy8VXVEa'
AI_API_KEY = 'AIzaSyCHxyc0GymatR3WhS5OsC5VhgebOsamKC8'

# Configure AI
ai.configure(api_key=AI_API_KEY)
model = ai.GenerativeModel(model_name="gemini-1.5-flash").start_chat()

# Helper Functions
def encode_image(image):
    return base64.b64encode(image.read()).decode('ascii')

def plant_identification(image):
    images = [encode_image(image)]
    response = requests.post(
        'https://api.plant.id/v3/identification',
        params={'details': 'url,common_names'},
        headers={'Api-Key': PLANT_API_KEY},
        json={'images': images},
    )
    result = response.json()
    if result.get('is_plant', {}).get('binary'):
        suggestions = result['classification']['suggestions']
        return [{'name': s['name'], 'probability': s['probability']} for s in suggestions]
    else:
        return {"error": "This is not recognized as a plant."}

def plant_health_assessment(image):
    images = [encode_image(image)]
    response = requests.post(
        'https://api.plant.id/v3/health_assessment',
        headers={'Api-Key': PLANT_API_KEY},
        json={'images': images},
    )
    result = response.json()
    if result.get('is_healthy', {}).get('binary'):
        return {'status': 'healthy', 'message': "The plant appears healthy."}
    else:
        diseases = result.get('disease', {}).get('suggestions', [])
        if not diseases:
            return {'status': 'unhealthy', 'message': 'No diseases found or key error.'}
        return {
            'status': 'unhealthy',
            'diseases': [
                {
                    'disease_name': d['name'],
                    'probability': d['probability'],
                    'description': d['description'],
                    'treatment': d['treatment'],
                }
                for d in diseases
            ]
        }

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_with_bot():
    user_message = request.json.get('message', '')
    response = model.send_message(user_message)
    return jsonify({'response': response.text})

@app.route('/upload', methods=['POST'])
def upload_image():
    image = request.files['image']
    analysis_type = request.form.get('type')
    
    if analysis_type == 'identify':
        result = plant_identification(image)
    elif analysis_type == 'health':
        result = plant_health_assessment(image)
    else:
        result = {"error": "Invalid analysis type."}

    return jsonify(result)  # Return a complete JSON response

if __name__ == '__main__':
    app.run(debug=True)
