import os
from datetime import datetime, timedelta
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

class CalendarAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=os.getenv("GOOGLE_API_KEY")
        )
        
    def classify_intent(self, user_input: str) -> str:
        """Classify user intent for calendar operations"""
        system_prompt = """You are a calendar intent classifier. Classify the user's request into one of these categories:
        - 'create': User wants to schedule, book, or create an appointment
        - 'view': User wants to check, list, or see their appointments  
        - 'chat': General conversation or greeting
        
        Respond with only the category name."""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_input)
        ]
        
        response = self.llm.invoke(messages)
        return response.content.strip().lower()
    
    def extract_appointment_details(self, user_input: str) -> Dict[str, Any]:
        """Extract appointment details from user input"""
        system_prompt = """Extract appointment details from the user's request. Return a JSON object with:
        - title: appointment title/summary
        - date: date in YYYY-MM-DD format (if not provided, use today's date)
        - start_time: start time in HH:MM format
        - end_time: end time in HH:MM format (if not provided, add 1 hour to start_time)
        - missing: list of missing required information
        
        If critical information is missing, include it in the 'missing' array."""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_input)
        ]
        
        response = self.llm.invoke(messages)
        try:
            import json
            return json.loads(response.content)
        except:
            return {"missing": ["Could not parse appointment details"]}
    
    def create_appointment(self, details: Dict[str, Any]) -> str:
        """Simulate creating a calendar appointment"""
        if details.get("missing"):
            missing_items = ", ".join(details["missing"])
            return f"I need more information to create your appointment. Please provide: {missing_items}"
        
        # In a real implementation, this would integrate with Google Calendar API
        return f"✅ Appointment created: '{details['title']}' on {details['date']} from {details['start_time']} to {details['end_time']}"
    
    def view_appointments(self, user_input: str) -> str:
        """Simulate viewing calendar appointments"""
        # In a real implementation, this would fetch from Google Calendar API
        return "📅 Your upcoming appointments:\n• Meeting with team - Today 2:00 PM\n• Doctor appointment - Tomorrow 10:00 AM"
    
    def handle_chat(self, user_input: str) -> str:
        """Handle general conversation"""
        system_prompt = """You are a friendly calendar assistant. Respond to the user's message naturally and offer to help with scheduling if appropriate."""
        
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_input)
        ]
        
        response = self.llm.invoke(messages)
        return response.content
    
    def process_request(self, user_input: str) -> str:
        """Main method to process user requests"""
        intent = self.classify_intent(user_input)
        
        if intent == 'create':
            details = self.extract_appointment_details(user_input)
            return self.create_appointment(details)
        elif intent == 'view':
            return self.view_appointments(user_input)
        else:
            return self.handle_chat(user_input)

def main():
    agent = CalendarAgent()
    
    print("Calendar AI Assistant - Type 'quit' to exit")
    print("Try: 'Book a meeting tomorrow at 2 PM' or 'Show my appointments'")
    
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() == 'quit':
            break
            
        response = agent.process_request(user_input)
        print(f"Assistant: {response}")

if __name__ == "__main__":
    main()