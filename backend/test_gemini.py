import google.generativeai as genai
from config import get_settings

settings = get_settings()

api_key = settings.google_api_key.get_secret_value()
print("Using key:", api_key[:10] + "...")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content("Say hello")

print(response.text)