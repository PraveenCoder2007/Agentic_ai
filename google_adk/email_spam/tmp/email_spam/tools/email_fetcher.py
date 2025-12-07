import typing

@typing.no_type_check
def fetch_emails() -> typing.List[typing.Dict[str, str]]:
  """
  Fetches a sample list of emails for spam analysis.

  This is a mock function. In a real application, this would connect to an
  email service like the Gmail API or Outlook API to retrieve actual emails.
  """
  emails = [
      {
          "subject": "Project Update Meeting",
          "body": "Hi Team, Let's sync up on the project status tomorrow at 10 AM. Please find the agenda attached. Best, Alice",
      },
      {
          "subject": "URGENT: Your Account Has Been Compromised!",
          "body": "DEAR CUSTOMER, we have detected suspicious activity on your account. CLICK HERE http://bit.ly/totally-not-a-scam to verify your details immediately or your account will be locked FOREVER.",
      },
      {
          "subject": "Congratulations! You've Won a $1,000,000 Prize",
          "body": "You have been selected as the lucky winner of our grand lottery! To claim your prize, please send your bank details and a $500 processing fee to winner@example.com.",
      },
      {
          "subject": "Weekly Newsletter",
          "body": "Hi there, check out our latest articles and updates for this week. We hope you enjoy the read!",
      },
  ]
  print("Fetched a sample list of emails.")
  return emails
