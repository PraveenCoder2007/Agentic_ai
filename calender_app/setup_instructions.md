# Google Calendar Integration Setup

## 1. Enable Google Calendar API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the Google Calendar API
4. Go to "Credentials" → "Create Credentials" → "OAuth 2.0 Client IDs"
5. Choose "Desktop application"
6. Download the credentials file as `credentials.json`
7. Place `credentials.json` in the `calender_app` folder

## 2. Install Dependencies

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

## 3. Run the Agent

```bash
python google_calendar_agent.py
```

On first run, it will open a browser for Google authentication.

## 4. Test Commands

- "book a meeting tomorrow at 6 pm"
- "create teacher meeting today at 2 pm"  
- "show my appointments"