import google.generativeai as genai
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

# Load api_key
load_dotenv()
api_key = os.getenv('API_KEY')

# Check if api_key exists
if api_key is None:
    raise ValueError("API key not found. Please set the 'API_KEY' environment variable.")

# Configure gemini api and set up model
genai.configure(api_key=os.environ['API_KEY'])
model = genai.GenerativeModel("gemini-1.5-flash")

# Start chat with basic conversation prompts
chat = model.start_chat(
    history=[
        {"role": "user", "parts": "You are an academic advisor, and I am a student looking for academic career help. \
                    Please only respond to academically related messages, and do not respond to anything not related, such as homework support."},
        {"role": "model", "parts": "Great to meet you. What would you like to know?"},
    ]
)

# Flask app setup
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    message = data['message']

    response = chat.send_message(message)
    return jsonify({'response': response.text})

if __name__ == "__main__":
    app.run(debug=True)