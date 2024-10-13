import google.generativeai as genai
import google_auth_oauthlib.flow
import googleapiclient.discovery
import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

# Setup logging
logging.basicConfig(level=logging.DEBUG)

# reads in information files
def read_info_files():
    try:
        with open('./course_data/cs_lsa_info.txt', 'r') as f:
            cs_lsa_info = f.read()
        with open('./course_data/cs_eng_info.txt', 'r') as f:
            cs_eng_info = f.read()
        return cs_lsa_info, cs_eng_info
    except Exception as e:
        logging.error(f"Error reading course files: {e}")
        return "", ""


# def read_course_data():
#     folder_path = 'course_data'
#     concatenated_content = ''
    
#     for filename in os.listdir(folder_path):
#         if filename.endswith('.txt'):
#             file_path = os.path.join(folder_path, filename)
#             with open(file_path, 'r', encoding='utf-8') as f:
#                 concatenated_content += f.read() + '\n'
    
#     return concatenated_content

# Load api_key
load_dotenv()
api_key = os.getenv('API_KEY')

# Check if api_key exists
if api_key is None:
    raise ValueError("API key not found. Please set the 'API_KEY' environment variable.")

# Configure gemini api and set up model
genai.configure(api_key=os.environ['API_KEY'])
model = genai.GenerativeModel("gemini-1.5-flash")

# Read program information
cs_lsa_info, cs_eng_info = read_info_files()

# Start chat with basic conversation prompts and program information
chat = model.start_chat(
    history=[
        {"role": "user", "parts": "You are an academic advisor, and I am a student looking for academic career help. \
                    Please only respond to academically related messages such as classwork and jobs, \
                    and do not respond to anything unrelated, such as video games and internet memes."},
        {"role": "model", "parts": "Great to meet you. What would you like to know?"},

        {"role": "user", "parts": f"Here's information about the CS-LSA program:\n\n{cs_lsa_info}"},
        {"role": "model", "parts": "I have read and understood the CS-LSA program information. How can I assist you with this program?"},
        {"role": "user", "parts": f"Here's information about the CS-ENG program:\n\n{cs_eng_info}"},
        {"role": "model", "parts": "I have also read and understood the CS-ENG program information. How can I help you with information from either of these programs?"},
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
    # course_data = read_course_data()

    # Enrich the message with the course data
    # enriched_message = f"Course data: {course_data}. Message: {message}"

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