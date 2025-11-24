from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from .email_fetcher import fetch_emails

# Create tool from the email fetcher function
email_tool = FunctionTool(fetch_emails)

# Create the root agent
root_agent = Agent(
    name="EmailSpamDetector",
    model="gemini-2.0-flash",
    description="An agent that fetches emails and analyzes them for spam",
    tools=[email_tool]
)