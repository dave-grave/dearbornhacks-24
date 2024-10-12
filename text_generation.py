import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY')

if api_key is None:
    raise ValueError("API key not found. Please set the 'API_KEY' environment variable.")

genai.configure(api_key=os.environ['API_KEY'])


model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Write a story about a magic backpack.")
print(response.text)