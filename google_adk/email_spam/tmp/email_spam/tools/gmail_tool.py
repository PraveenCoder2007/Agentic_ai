import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def _get_gmail_service():
    """Helper function to authenticate and return the Gmail API service client."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Error refreshing credentials: {e}")
                return None
        else:
            if not os.path.exists("credentials.json"):
                print("Authentication error: 'credentials.json' not found.")
                return None
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("gmail", "v1", credentials=creds)
        return service
    except HttpError as error:
        print(f"An error occurred building the service: {error}")
        return None

def get_new_emails(max_results: int = 5):
    """
    Fetches and returns the most recent unread emails from a Gmail account.
    """
    service = _get_gmail_service()
    if not service:
        return "Authentication failed. Cannot connect to Gmail."

    try:
        results = (
            service.users()
            .messages()
            .list(userId="me", labelIds=["INBOX", "UNREAD"], maxResults=max_results)
            .execute()
        )
        messages = results.get("messages", [])

        if not messages:
            return "No new unread emails found."

        emails = []
        for message in messages:
            msg = (
                service.users()
                .messages()
                .get(userId="me", id=message["id"], format="metadata")
                .execute()
            )
            headers = msg.get("payload", {}).get("headers", [])
            subject = next(
                (h["value"] for h in headers if h["name"] == "Subject"), "No Subject"
            )
            sender = next(
                (h["value"] for h in headers if h["name"] == "From"), "No Sender"
            )
            emails.append({
                "sender": sender,
                "subject": subject,
                "snippet": msg.get("snippet", "No snippet available."),
            })
        return emails

    except HttpError as error:
        return f"An error occurred: {error}"


def get_spam_count():
    """
    Checks the number of messages in the SPAM folder.
    """
    service = _get_gmail_service()
    if not service:
        return "Authentication failed. Cannot connect to Gmail."

    try:
        results = service.users().labels().get(userId='me', id='SPAM').execute()
        count = results.get('messagesTotal', 0)
        return f"There are {count} messages in the spam folder."
    except HttpError as error:
        return f"An error occurred while checking spam: {error}"


def get_inbox_count():
    """
    Checks the total number of messages in the INBOX folder.
    """
    service = _get_gmail_service()
    if not service:
        return "Authentication failed. Cannot connect to Gmail."

    try:
        # Get the details for the INBOX label
        results = service.users().labels().get(userId='me', id='INBOX').execute()
        count = results.get('messagesTotal', 0)
        return f"There are {count} total messages in your inbox."
    except HttpError as error:
        return f"An error occurred while checking the inbox: {error}"
