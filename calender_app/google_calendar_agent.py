import os
import json
from datetime import datetime, timedelta
from typing import Dict, Any
import google.generativeai as genai
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar']

class GoogleCalendarAgent:
    def __init__(self):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.calendar_service = self.authenticate_google_calendar()
        
    def authenticate_google_calendar(self):
        """Authenticate and return Google Calendar service"""
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if not os.path.exists('credentials.json'):
                    print("Please download credentials.json from Google Cloud Console")
                    return None
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        
        return build('calendar', 'v3', credentials=creds)
    
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
        
        user_lower = user_input.lower()
        if "teacher" in user_lower:
            title = "Teacher Meeting"
        elif "meeting" in user_lower:
            title = "Meeting"
        else:
            title = "Appointment"
            
        if any(time_str in user_lower for time_str in ["6 pm", "6.pm", "6pm", "18:00", "6 p.m"]):
            start_time = "18:00"
            end_time = "19:00"
        elif any(time_str in user_lower for time_str in ["2 pm", "2.pm", "2pm", "14:00", "2 p.m"]):
            start_time = "14:00"
            end_time = "15:00"
        else:
            return {"missing": ["time"]}
            
        if "tomorrow" in user_lower:
            date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        elif "today" in user_lower:
            date = today
        else:
            date = today
            
        return {
            "title": title,
            "date": date,
            "start_time": start_time,
            "end_time": end_time,
            "missing": []
        }
    
    def create_google_calendar_event(self, details: Dict[str, Any]) -> str:
        """Create actual Google Calendar event"""
        if not self.calendar_service:
            return "❌ Google Calendar authentication failed"
            
        start_datetime = f"{details['date']}T{details['start_time']}:00"
        end_datetime = f"{details['date']}T{details['end_time']}:00"
        
        event = {
            'summary': details['title'],
            'start': {
                'dateTime': start_datetime,
                'timeZone': 'Asia/Kolkata',
            },
            'end': {
                'dateTime': end_datetime,
                'timeZone': 'Asia/Kolkata',
            },
        }
        
        try:
            event = self.calendar_service.events().insert(calendarId='primary', body=event).execute()
            return f"✅ Event created in Google Calendar: '{details['title']}' on {details['date']} from {details['start_time']} to {details['end_time']}"
        except Exception as e:
            return f"❌ Failed to create event: {str(e)}"
    
    def view_google_calendar_events(self) -> str:
        """View upcoming Google Calendar events"""
        if not self.calendar_service:
            return "❌ Google Calendar authentication failed"
            
        now = datetime.utcnow().isoformat() + 'Z'
        
        try:
            events_result = self.calendar_service.events().list(
                calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
                orderBy='startTime').execute()
            events = events_result.get('items', [])
            
            if not events:
                return "📅 No upcoming events found."
            
            result = "📅 Your upcoming events:\n"
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                result += f"• {event['summary']} - {start}\n"
            
            return result
        except Exception as e:
            return f"❌ Failed to fetch events: {str(e)}"
    
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
            if details.get("missing"):
                missing_items = ", ".join(details["missing"])
                return f"I need more information: {missing_items}. Please specify the missing details."
            return self.create_google_calendar_event(details)
        elif intent == 'view':
            return self.view_google_calendar_events()
        else:
            return self.handle_chat(user_input)

def main():
    agent = GoogleCalendarAgent()
    
    print("Google Calendar AI Assistant - Type 'quit' to exit")
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