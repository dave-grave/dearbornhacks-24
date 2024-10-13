import google.generativeai as genai
import google_auth_oauthlib.flow
import googleapiclient.discovery
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
                    Please only respond to academically related messages, and do not respond to anything unrelated, \
                    such as video games and internet memes."},
        {"role": "model", "parts": "Great to meet you. What would you like to know?"},
    ]
)

# Flask app setup
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Google Docs API setup
def get_gdocs_service():
    SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=0)
    service = googleapiclient.discovery.build('docs', 'v1', credentials=creds)
    return service

def read_google_doc(doc_id):
    service = get_gdocs_service()
    document = service.documents().get(documentId=doc_id).execute()
    doc_content = ""
    for element in document.get('body').get('content'):
        if 'paragraph' in element:
            for text_run in element.get('paragraph').get('elements'):
                if 'textRun' in text_run:
                    doc_content += text_run.get('textRun').get('content')
    return doc_content

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message', '')
    doc_id = data.get('docId', '')

    if doc_id:
        try:
            doc_content = read_google_doc(doc_id)
            enriched_message = f"Document content: {doc_content}. Message: {message}"
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        enriched_message = message

    response = chat.send_message(enriched_message)
    return jsonify({'response': response.text})

if __name__ == "__main__":
    app.run(debug=True)