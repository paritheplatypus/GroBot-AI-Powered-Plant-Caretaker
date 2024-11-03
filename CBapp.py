from flask import Flask, request, jsonify
import google.generativeai as ai

app = Flask(__name__)

# Initialize your AI model (make sure to use your actual API key)
AI_API_KEY = 'YOUR_AI_API_KEY'
ai.configure(api_key=AI_API_KEY)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    response = ai.GenerativeModel(model_name="gemini-1.5-flash").start_chat().send_message(user_message)
    return jsonify({'response': response.text})

if __name__ == '__main__':
    app.run(debug=True)
