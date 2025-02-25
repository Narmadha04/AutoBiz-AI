import os
import base64
import pickle
import pandas as pd
import google.generativeai as genai
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText

# Define constants for Google API authentication
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
TOKEN_FILE = 'token.pickle'  # Stores authentication tokens
CREDENTIALS_FILE = 'client_secret.json'  # Path to Google API credentials
CSV_FILE = 'reminders.csv'  # Path to the CSV file containing invoice details

# Configure Google AI Studio API with API key (replace with actual key)
genai.configure(api_key="YOUR_API_KEY")  # Replace with your API key


def authenticate_gmail():
    """
    Authenticate and return Gmail API credentials.
    - Checks for existing authentication tokens.
    - If expired, refreshes the token.
    - If no valid credentials are found, initiates OAuth flow.
    """
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Start OAuth authentication flow
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=8080)

        # Save the new authentication token for future use
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return creds


def generate_email_content(name, invoice_no, amount, due_date):
    """
    Generate AI-powered email content using Google Gemini API.
    - Takes customer details and invoice information.
    - Uses AI to generate a professional, polite payment reminder.
    """
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"Write a polite email reminder for {name} about an unpaid invoice {invoice_no} of ${amount} due on {due_date}."
    
    response = model.generate_content(prompt)
    return response.text.strip()


def create_message(to, subject, body):
    """
    Create an email message in MIME format.
    - Converts text content into a base64-encoded Gmail API-compatible format.
    """
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}


def send_email(service, to, subject, body):
    """
    Send an email via Gmail API.
    - Calls create_message() to format the email.
    - Sends the email using Gmail API's send() method.
    """
    message = create_message(to, subject, body)
    try:
        sent_message = service.users().messages().send(userId='me', body=message).execute()
        print(f"Email sent to {to}! Message ID: {sent_message['id']}")
    except Exception as e:
        print(f"Error sending email to {to}: {e}")


def main():
    """
    Main function to automate invoice reminders.
    - Authenticates Gmail API.
    - Reads invoice details from a CSV file.
    - Identifies unpaid invoices and sends AI-generated email reminders.
    """
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)

    # Load invoice data from CSV
    df = pd.read_csv(CSV_FILE)

    # Filter unpaid invoices (has_paid == 'no')
    unpaid_df = df[df['has_paid'].str.lower() == 'no']

    # Process each unpaid invoice
    for _, row in unpaid_df.iterrows():
        email = row['email']
        name = row['name']
        invoice_no = row['invoice_no']
        amount = row['amount']
        due_date = row['due_date']
        
        # Generate AI-powered email content
        body = generate_email_content(name, invoice_no, amount, due_date)
        subject = f"Payment Reminder: Invoice {invoice_no}"
        
        # Send email reminder
        send_email(service, email, subject, body)


if __name__ == '__main__':
    main()
