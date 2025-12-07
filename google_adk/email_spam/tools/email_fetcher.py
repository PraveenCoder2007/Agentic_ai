import typing
import os
import base64
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def authenticate_gmail():
    """Authenticate and return Gmail service."""
    creds = None
    # Token file stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # You need to create credentials.json from Google Cloud Console
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    return build('gmail', 'v1', credentials=creds)

@typing.no_type_check
def fetch_emails(max_results: int = 10) -> typing.List[typing.Dict[str, str]]:
    """
    Fetches real emails from Gmail account.
    
    Args:
        max_results: Maximum number of emails to fetch
    
    Returns:
        List of email dictionaries with subject and body
    """
    try:
        service = authenticate_gmail()
        
        # Get list of messages
        results = service.users().messages().list(
            userId='me', maxResults=max_results).execute()
        messages = results.get('messages', [])
        
        emails = []
        for message in messages:
            # Get full message
            msg = service.users().messages().get(
                userId='me', id=message['id']).execute()
            
            # Extract subject
            subject = ''
            for header in msg['payload'].get('headers', []):
                if header['name'] == 'Subject':
                    subject = header['value']
                    break
            
            # Extract body
            body = ''
            if 'parts' in msg['payload']:
                for part in msg['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        data = part['body']['data']
                        body = base64.urlsafe_b64decode(data).decode('utf-8')
                        break
            else:
                if msg['payload']['body'].get('data'):
                    data = msg['payload']['body']['data']
                    body = base64.urlsafe_b64decode(data).decode('utf-8')
            
            emails.append({
                'subject': subject,
                'body': body[:500]  # Limit body length
            })
        
        print(f"Fetched {len(emails)} emails from Gmail.")
        return emails
        
    except Exception as e:
        print(f"Error fetching emails: {e}")
        # Fallback to sample emails if Gmail API fails
        return [
            {
                "subject": "Gmail API Error",
                "body": f"Could not connect to Gmail: {e}. Please set up Gmail API credentials."
            }
        ]
