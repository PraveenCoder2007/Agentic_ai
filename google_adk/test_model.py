import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)

# Try different model names
models_to_try = [
    "gemini-pro",
    "models/gemini-pro", 
    "gemini-1.5-pro",
    "models/gemini-1.5-pro",
    "gemini-1.5-flash",
    "models/gemini-1.5-flash"
]

for model_name in models_to_try:
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello")
        print(f"✅ Working model: {model_name}")
        print(f"Response: {response.text[:50]}...")
        break
    except Exception as e:
        print(f"❌ Failed model: {model_name} - {str(e)[:100]}")