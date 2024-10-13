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
        with open('./course_data/ce_eng_info.txt', 'r') as f:
            ce_eng_info = f.read()
        with open('./course_data/ee_eng_info.txt', 'r') as f:
            ee_eng_info = f.read()
        with open('./course_data/ds_lsa_info.txt', 'r') as f:
            ds_lsa_info = f.read()
        with open('./course_data/ds_eng_info.txt', 'r') as f:
            ds_eng_info = f.read()
        with open('./course_data/eecs_courses_info.txt', 'r') as f:
            eecs_courses_info = f.read()
        return cs_lsa_info, cs_eng_info, ce_eng_info, ee_eng_info, ds_lsa_info, ds_eng_info, eecs_courses_info
    except Exception as e:
        logging.error(f"Error reading course files: {e}")
        return "", ""

# Initialize global variables for courses and year
current_courses = ""
current_year = ""

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
cs_lsa_info, cs_eng_info, ds_lsa_info, ee_eng_info, ce_eng_info, ds_eng_info, eecs_courses_info = read_info_files()

# Start chat with basic conversation prompts and program information
chat = model.start_chat(
    history=[
        {"role": "user", "parts": "You are an academic advisor, and I am a student looking for academic career help. \
                    Please only respond to academically related messages such as classwork and jobs, \
                    and do not respond to anything unrelated, such as video games and internet memes."},
        {"role": "model", "parts": "Great to meet you. What would you like to know?"},

        # read in course and major-specific information
        {"role": "user", "parts": f"Here's information about the CS-LSA program:\n\n{cs_lsa_info}"},
        {"role": "model", "parts": "I have read and understood the CS-LSA program information. How can I assist you with this program?"},
        {"role": "user", "parts": f"Here's information about the CS-ENG program:\n\n{cs_eng_info}"},
        {"role": "model", "parts": "I have also read and understood the CS-ENG program information. How can I assist you with this program?"},
         {"role": "user", "parts": f"Here's information about the CE-ENG program:\n\n{ce_eng_info}"},
        {"role": "model", "parts": "I have read and understood the CE-ENG program information. How can I assist you with this program?"},
         {"role": "user", "parts": f"Here's information about the EE-ENG program:\n\n{ee_eng_info}"},
        {"role": "model", "parts": "I have read and understood the EE-ENG program information. How can I assist you with this program?"},
         {"role": "user", "parts": f"Here's information about the DS-LSA program:\n\n{ds_lsa_info}"},
        {"role": "model", "parts": "I have read and understood the DS-LSA program information. How can I assist you with this program?"},
        {"role": "user", "parts": f"Here's information about the DS-ENG program:\n\n{ds_eng_info}"},
        {"role": "model", "parts": "I have read and understood the DS-ENG program information. How can I assist you with this program?"},
        {"role": "user", "parts": f"Here's information about the all the EECS courses:\n\n{eecs_courses_info}"},
        {"role": "model", "parts": "I have read and understood the EECS courses catalog. I will use this information when referencing courses in the future."},

        # tell AI to output supplmentary content in Mermaid flowchart
        {"role": "user", "parts": "Finally, as a supplement to the advice, please output a flowchart of a possible course selection in Mermaid code."},
        {"role": "model", "parts": "I will optionally output a flowchart to complement the advice I give to users."},
    ]
)

# Flask app setup
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Google Docs API setup
# def get_gdocs_service():
#     SCOPES = ['https://www.googleapis.com/auth/documents.readonly']
#     flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
#     creds = flow.run_local_server(port=0)
#     service = googleapiclient.discovery.build('docs', 'v1', credentials=creds)
#     return service

# def read_google_doc(doc_id):
#     service = get_gdocs_service()
#     document = service.documents().get(documentId=doc_id).execute()
#     doc_content = ""
#     for element in document.get('body').get('content'):
#         if 'paragraph' in element:
#             for text_run in element.get('paragraph').get('elements'):
#                 if 'textRun' in text_run:
#                     doc_content += text_run.get('textRun').get('content')
#     return doc_content

@app.route('/set_courses', methods=['POST'])
def set_courses():
    global current_courses
    data = request.json
    current_courses = data.get('courses', '')
    return jsonify({'status': 'Courses set successfully'})

@app.route('/set_year', methods=['POST'])
def set_year():
    global current_year
    data = request.json
    current_year = data.get('year', '')
    return jsonify({'status': 'Year set successfully'})

@app.route('/send_message', methods=['POST'])
def send_message():
    global current_courses, current_year
    data = request.json
    message = data.get('message', '')
    
    # Enrich the message with the current courses and year
    enriched_message = f"Message: {message}"
    if current_courses:
        enriched_message += f"\nCourses taken: {current_courses}"
    if current_year:
        enriched_message += f"\nGraduation year: {current_year}"

    # Generate response using Google Gemini
    response = chat.send_message(enriched_message)
    
    # Generate a simple mermaid flowchart as an example
    mermaid_code = '''
    graph TD;
        A[Start] --> B{Is the action correct?};
        B -- Yes --> C[Proceed];
        B -- No --> D[Stop];
        C --> E[End];
        D --> E;
    '''
    
    # Response JSON
    response_json = {
        'response': response.text,
        'mermaid': mermaid_code
    }
    
    return jsonify(response_json)

# @app.route('/send_message', methods=['POST'])
# def send_message():   
#     data = request.json
#     message = data.get('message', '')
#     doc_id = data.get('docId', '')

#     # Enrich the message with the current courses and year
#     enriched_message = f"Message: {message}"
#     if current_courses:
#         enriched_message += f"\nCourses taken: {current_courses}"
#     if current_year:
#         enriched_message += f"\nGraduation year: {current_year}"

#     response = chat.send_message(enriched_message)
#     return jsonify({'response': response.text})

if __name__ == "__main__":
    app.run(debug=True)