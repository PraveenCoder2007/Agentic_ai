import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

# Load environment variables
load_dotenv()
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])



def call_agent(query):
    """
    Helper function to call the agent with a query.
    """
    print(f"\n--- Running Query: {query} ---")
    
    # Try models in order of preference (lighter models first to save quota)
    models_to_try = [
        'models/gemini-2.5-flash-lite',
        'models/gemini-2.0-flash-lite',
        'models/gemini-flash-lite-latest',
        'models/gemini-2.5-flash',
        'models/gemini-2.0-flash'
    ]
    
    for model_name in models_to_try:
        try:
            print(f"Trying model: {model_name}")
            model = genai.GenerativeModel(model_name)
            
            response = model.generate_content(f"Answer this question: {query}")
            print("Agent Response:", response.text)
            return  # Success, exit function
            
        except ResourceExhausted as e:
            print(f"Quota exceeded for {model_name}: {e}")
            continue  # Try next model
            
        except Exception as e:
            print(f"Error with {model_name}: {e}")
            continue  # Try next model
    
    print("All models failed or quota exceeded. Please wait for quota reset or upgrade your plan.")
    print("-" * 50)

if __name__ == "__main__":
    call_agent("what's the latest ai news?")