import google.generativeai as genai
from config import get_settings

settings = get_settings()

genai.configure(api_key=settings.google_api_key.get_secret_value())

for model in genai.list_models():
    if "generateContent" in model.supported_generation_methods:
        print(model.name)