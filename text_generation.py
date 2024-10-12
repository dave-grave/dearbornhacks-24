import google.generativeai as genai
import os
from dotenv import load_dotenv

# load api_key
load_dotenv()
api_key = os.getenv('API_KEY')

# check if api_key exists
if api_key is None:
    raise ValueError("API key not found. Please set the 'API_KEY' environment variable.")

# configure gemini api and set up model
genai.configure(api_key=os.environ['API_KEY'])
model = genai.GenerativeModel("gemini-1.5-flash")

# start chat with basic conversation prompts
chat = model.start_chat(
            history=[
                {"role": "user", "parts": "Hello"},
                {"role": "model", "parts": "Great to meet you. What would you like to know?"},
            ]
        )

# take in input as long as user doesn't reply with 'q'
while(True):
    prompt = input('Enter a reply: ')
    if prompt == 'q':
        break

    response = chat.send_message(prompt)
    print(response.text)

# PROMPTS TESTING
# default_prompt = "You are a Michigan Engineering student. Weigh the options of your major choices for different career paths."
# user_input = input("Enter prompt: ")
# prompt = user_input if user_input.strip() else default_prompt
# response = model.generate_content(f"""Given a definition, return the word it defines.
#                                         Definition: When you're happy that other people are also sad.
#                                         Word: schadenfreude
#                                         Definition: existing purely in the mind, but not in physical reality
#                                         Word: abstract
#                                         Definition: ${prompt}
#                                         Word:""")
# print(response.text)