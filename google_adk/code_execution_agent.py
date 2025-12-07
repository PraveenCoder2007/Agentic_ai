import os
import asyncio
import nest_asyncio
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# Define variables required for Session setup and Agent execution
APP_NAME = "calculator"
USER_ID = "user1234"
SESSION_ID = "session_code_exec_async"

# Agent Interaction (Async)
async def call_agent_async(query):
    """
    Calculator agent that executes Python code for mathematical calculations.
    """
    print(f"\n--- Running Query: {query} ---")
    
    # Try models in order of preference
    models_to_try = [
        'models/gemini-2.5-flash-lite',
        'models/gemini-2.0-flash-lite', 
        'models/gemini-2.5-flash'
    ]
    
    for model_name in models_to_try:
        try:
            model = genai.GenerativeModel(
                model_name,
                tools='code_execution'
            )
            
            prompt = f"""You are a calculator agent.
When given a mathematical expression, write and execute Python code to calculate the result.
Return only the final numerical result as plain text, without markdown or code blocks.

Query: {query}"""
            
            response = await model.generate_content_async(prompt)
            print(f"==> Final Agent Response: {response.text}")
            return  # Success, exit function
            
        except Exception as e:
            if "quota" in str(e).lower():
                continue  # Try next model
            else:
                print(f"ERROR with {model_name}: {e}")
                continue
    
    print("All models failed or quota exceeded. Please wait for quota reset.")
    print("-" * 30)

# Main async function to run the examples
async def main():
    await call_agent_async("Calculate the value of (5 + 7) * 3")
    await call_agent_async("What is 10 factorial?")

if __name__ == "__main__":
    try:
        nest_asyncio.apply()
        asyncio.run(main())
    except RuntimeError as e:
        if "cannot be called from a running event loop" in str(e):
            print("\nRunning in an existing event loop (like Colab/Jupyter).")
            print("Please run `await main()` in a notebook cell instead.")
        else:
            raise e