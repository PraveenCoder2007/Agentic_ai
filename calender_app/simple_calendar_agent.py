import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

class CalendarAgent:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        
    def classify_intent(self, user_input: str) -> str:
        """Classify user intent for calendar operations"""
        prompt = f"""Classify this request into one category: 'create', 'view', or 'chat'
        - 'create': User wants to schedule, book, or create an appointment
        - 'view': User wants to check, list, or see their appointments  
        - 'chat': General conversation or greeting
        
        User input: {user_input}
        
        Respond with only the category name."""
        
        response = self.model.generate_content(prompt)
        return response.text.strip().lower()
    
    def extract_appointment_details(self, user_input: str) -> Dict[str, Any]:
        """Extract appointment details from user input"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        # Simple pattern matching for common cases
        user_lower = user_input.lower()
        if "teacher" in user_lower:
            title = "Teacher Meeting"
        elif "meeting" in user_lower:
            title = "Meeting"
        else:
            title = "Appointment"
            
        user_lower = user_input.lower()
        if any(time_str in user_lower for time_str in ["6 pm", "6.pm", "6pm", "18:00", "6 p.m"]):
            start_time = "18:00"
            end_time = "19:00"
        elif any(time_str in user_lower for time_str in ["2 pm", "2.pm", "2pm", "14:00", "2 p.m"]):
            start_time = "14:00"
            end_time = "15:00"
        else:
            return {"missing": ["time"]}
            
        if "tomorrow" in user_input.lower():
            date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        elif "today" in user_input.lower():
            date = today
        else:
            date = today  # Default to today
            
        return {
            "title": title,
            "date": date,
            "start_time": start_time,
            "end_time": end_time,
            "missing": []
        }
    
    def create_appointment(self, details: Dict[str, Any]) -> str:
        """Simulate creating a calendar appointment"""
        if details.get("missing"):
            missing_items = ", ".join(details["missing"])
            return f"I need more information: {missing_items}. Please specify the missing details."
        
        return f"✅ Appointment created: '{details['title']}' on {details['date']} from {details['start_time']} to {details['end_time']}"
    
    def view_appointments(self, user_input: str) -> str:
        """Simulate viewing calendar appointments"""
        return "📅 Your upcoming appointments:\n• Meeting with team - Today 2:00 PM\n• Doctor appointment - Tomorrow 10:00 AM"
    
    def handle_chat(self, user_input: str) -> str:
        """Handle general conversation"""
        prompt = f"You are a friendly calendar assistant. Respond naturally to: {user_input}"
        response = self.model.generate_content(prompt)
        return response.text
    
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
            
        try:
            response = agent.process_request(user_input)
            print(f"Assistant: {response}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()