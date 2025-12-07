import os
import asyncio
from typing import Dict, Any
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

# --- Parallel Processing Functions ---
async def summarize_topic(topic: str) -> str:
    """Summarize the topic concisely."""
    prompt = f"Summarize the following topic concisely: {topic}"
    response = await model.generate_content_async(prompt)
    return response.text

async def generate_questions(topic: str) -> str:
    """Generate three interesting questions about the topic."""
    prompt = f"Generate three interesting questions about the following topic: {topic}"
    response = await model.generate_content_async(prompt)
    return response.text

async def extract_key_terms(topic: str) -> str:
    """Identify 5-10 key terms from the topic."""
    prompt = f"Identify 5-10 key terms from the following topic, separated by commas: {topic}"
    response = await model.generate_content_async(prompt)
    return response.text

async def synthesize_results(topic: str, summary: str, questions: str, key_terms: str) -> str:
    """Synthesize all results into a comprehensive answer."""
    prompt = f"""Based on the following information:
    Summary: {summary}
    Related Questions: {questions}
    Key Terms: {key_terms}
    
    Synthesize a comprehensive answer about: {topic}"""
    
    response = await model.generate_content_async(prompt)
    return response.text

# --- Run Parallel Processing ---
async def run_parallel_example(topic: str) -> None:
    """
    Run parallel processing tasks and synthesize results.
    Args:
        topic: The input topic to be processed.
    """
    print(f"\n--- Running Parallel Processing for Topic: '{topic}' ---")
    
    try:
        print("🔄 Running parallel tasks...")
        
        # Run three tasks in parallel using asyncio.gather
        summary, questions, key_terms = await asyncio.gather(
            summarize_topic(topic),
            generate_questions(topic),
            extract_key_terms(topic)
        )
        
        print("✅ Parallel tasks completed. Synthesizing results...")
        
        # Synthesize the results
        final_result = await synthesize_results(topic, summary, questions, key_terms)
        
        print("\n--- Final Response ---")
        print(final_result)
        
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    test_topic = "The history of space exploration"
    # In Python 3.7+, asyncio.run is the standard way to run an async function.
    asyncio.run(run_parallel_example(test_topic))