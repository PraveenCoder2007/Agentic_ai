import google.generativeai as genai
import os

os.environ['GOOGLE_API_KEY'] = 'AIzaSyDbsn83vawtcSBBnmo1a1354rLQ2_RD-L4'
genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

print("Available models:")
for model in genai.list_models():
    if 'generateContent' in model.supported_generation_methods:
        print(f"- {model.name}")