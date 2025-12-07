import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
os.environ["GOOGLE_API_KEY"] = "AIzaSyDodXjHGfliBlLWCC2IVz7UD2LaYlDO2uQ"
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

def call_agent(query):
    """
    Simple agent that answers questions using Gemini.
    """
    print(f"\n--- Running Query: {query} ---")
    
    try:
        # List available models first
        print("Available models:")
        for model in genai.list_models():
            if 'generateContent' in model.supported_generation_methods:
                print(f"  - {model.name}")
        
        # Use the first available model
        available_models = [m for m in genai.list_models() 
                          if 'generateContent' in m.supported_generation_methods]
        
        if not available_models:
            print("No available models found!")
            return
            
        model_name = available_models[0].name
        print(f"\nUsing model: {model_name}")
        
        model = genai.GenerativeModel(model_name)
        response = model.generate_content(f"Answer this question: {query}")
        
        print("Agent Response:", response.text)
        
    except Exception as e:
        print(f"Error: {e}")
    
    print("-" * 50)

if __name__ == "__main__":
    call_agent("what's the latest ai news?")