import os
import google.generativeai as genai
from dotenv import load_dotenv

def setup_environment():
    """Configure Google Gemini API."""
    load_dotenv()
    google_api_key = "AIzaSyDbsn83vawtcSBBnmo1a1354rLQ2_RD-L4"
    genai.configure(api_key=google_api_key)
    
    
    return genai.GenerativeModel('gemini-2.5-flash')

def research_agent(model):
    """Senior Research Analyst agent."""
    prompt = """
    You are a Senior Research Analyst with expertise in identifying key trends and synthesizing information.
    
    Task: Research the top 3 emerging trends in Artificial Intelligence in 2024-2025. Focus on practical applications and potential impact.
    
    Provide a detailed summary of the top 3 AI trends, including key points and sources.
    """
    
    response = model.generate_content(prompt)
    return response.text

def writer_agent(model, research_content):
    """Technical Content Writer agent."""
    prompt = f"""
    You are a Technical Content Writer who can translate complex technical topics into accessible content.
    
    Task: Write a 500-word blog post based on the following research findings. The post should be engaging and easy for a general audience to understand.
    
    Research findings:
    {research_content}
    
    Write a complete 500-word blog post about the latest AI trends.
    """
    
    response = model.generate_content(prompt)
    return response.text

def main():
    """Multi-agent collaboration using Google Gemini."""
    print("## Running blog creation crew with Google Gemini... ##")
    
    # Setup Gemini model
    model = setup_environment()
    
    # Execute research task
    print("\n🔍 Research Agent: Analyzing AI trends...")
    research_results = research_agent(model)
    print("✅ Research completed!")
    
    # Execute writing task
    print("\n✍️ Writer Agent: Creating blog post...")
    blog_post = writer_agent(model, research_results)
    print("✅ Writing completed!")
    
    # Display results
    print("\n" + "="*50)
    print("## RESEARCH FINDINGS ##")
    print("="*50)
    print(research_results)
    
    print("\n" + "="*50)
    print("## FINAL BLOG POST ##")
    print("="*50)
    print(blog_post)

if __name__ == "__main__":
    main()