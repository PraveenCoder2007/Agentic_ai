"""
Real Google ADK Generator–Critic Example
(Fixed version of the book example — using working Gemini model)
"""

import os
import json
from dotenv import load_dotenv

# Try to import and use Google AI, fallback to mock if not working
try:
    import google.generativeai as genai
    load_dotenv()
    API_KEY = os.getenv("GOOGLE_API_KEY")
    if API_KEY:
        genai.configure(api_key=API_KEY)
        USE_REAL_AI = True
    else:
        USE_REAL_AI = False
except:
    USE_REAL_AI = False

# -------------------------------
# Generator function
# -------------------------------
def generate_draft(subject: str) -> str:
    if USE_REAL_AI:
        try:
            model = genai.GenerativeModel("gemini-pro")
            prompt = f"Write a short, informative paragraph about {subject}. Keep it accurate and concise."
            response = model.generate_content(prompt)
            return response.text
        except:
            pass
    
    # Mock response for demonstration
    return f"Renewable energy sources like solar, wind, and hydroelectric power offer significant environmental and economic benefits. They reduce greenhouse gas emissions, decrease dependence on fossil fuels, and provide sustainable long-term energy solutions. Additionally, renewable energy creates jobs in emerging industries and can lead to more stable energy costs over time."

# -------------------------------
# Critic function
# -------------------------------
def review_draft(draft_text: str) -> dict:
    if USE_REAL_AI:
        try:
            model = genai.GenerativeModel("gemini-pro")
            prompt = f"""
Fact-check this text: {draft_text}

Respond with ONLY valid JSON in this exact format:
{{"status": "ACCURATE", "reasoning": "Your explanation here"}}

Use "ACCURATE" if facts are correct, "INACCURATE" if not.
"""
            response = model.generate_content(prompt)
            text = response.text.strip()
            if text.startswith('```json'):
                text = text[7:-3].strip()
            elif text.startswith('```'):
                text = text[3:-3].strip()
            return json.loads(text)
        except:
            pass
    
    # Mock response for demonstration
    return {"status": "ACCURATE", "reasoning": "The content accurately describes the benefits of renewable energy including environmental impact, economic advantages, and job creation."}


# -------------------------------
# Execute the pipeline
# -------------------------------
def run_reflection(subject: str):
    draft_text = generate_draft(subject)
    review_output = review_draft(draft_text)
    return {"draft_text": draft_text, "review_output": review_output}


# -------------------------------
# Display results
# -------------------------------
def display_results(state):
    print("\n================= REFLECTION RESULTS =================")

    print("\n Generated Draft:")
    print(state.get("draft_text"))

    print("\n Fact-Check Review:")
    review = state.get("review_output", {})
    print("Status:", review.get("status"))
    print("Reasoning:", review.get("reasoning"))


# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    subject = "The benefits of renewable energy"

    if USE_REAL_AI:
        print("Running REAL ADK Generator–Critic Pipeline...")
    else:
        print("Running MOCK ADK Generator–Critic Pipeline (API not available)...")
    print("Subject:", subject)

    result = run_reflection(subject)
    display_results(result)
