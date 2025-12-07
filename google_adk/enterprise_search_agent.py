import asyncio
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

async def call_vsearch_agent_async(query: str):
    """Enterprise search agent using Google Generative AI."""
    print(f"User: {query}")
    print("Agent: ", end="", flush=True)
    
    # Try models in order of preference (lighter models first)
    models_to_try = [
        'models/gemini-2.5-flash-lite',
        'models/gemini-2.0-flash-lite',
        'models/gemini-flash-lite-latest',
        'models/gemini-2.5-flash'
    ]
    
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(model_name)
            prompt = f"""You are an enterprise search agent that answers questions about Q2 strategy documents.
            
Query: {query}
            
Please provide a comprehensive answer based on available information."""
            
            response = await model.generate_content_async(prompt)
            print(response.text)
            print("-" * 30)
            return  # Success, exit function
            
        except Exception as e:
            if "quota" in str(e).lower():
                continue  # Try next model
            else:
                print(f"\nError with {model_name}: {e}")
                continue
    
    print("\nAll models failed or quota exceeded. Please wait for quota reset.")
    print("-" * 30)

async def run_vsearch_example():
    await call_vsearch_agent_async("Summarize the main points about the Q2 strategy document.")
    await call_vsearch_agent_async("What safety procedures are mentioned for lab X?")

if __name__ == "__main__":
    try:
        asyncio.run(run_vsearch_example())
    except RuntimeError as e:
        if "cannot be called from a running event loop" in str(e):
            print("Skipping execution in a running event loop. Please run this script directly.")
        else:
            raise e