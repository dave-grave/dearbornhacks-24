import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY')

if api_key is None:
    raise ValueError("API key not found. Please set the 'API_KEY' environment variable.")

genai.configure(api_key=os.environ['API_KEY'])


model = genai.GenerativeModel("gemini-1.5-flash")
default_prompt = "You are a Michigan Engineering student. Weigh the options of your major choices for different career paths."
user_input = input("Enter prompt: ")
prompt = user_input if user_input.strip() else default_prompt
response = model.generate_content(prompt)
print(response.text)