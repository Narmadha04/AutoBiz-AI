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

# Define constants
SCOPES = ['https://www.googleapis.com/auth/gmail.send']
TOKEN_FILE = 'token.pickle'
CREDENTIALS_FILE = 'client_secret.json'  # Path to Google API credentials
CSV_FILE = 'reminders.csv'  # Path to your CSV file

# Configure Google AI Studio API
genai.configure(api_key="AIzaSyAfEF0sTg_NWTDxBhWb_qphGY1uwENp_1M")  # Replace with your API key

# Authenticate Gmail
def authenticate_gmail():
    creds = None
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=8080)

        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

# Generate email content using Google AI Studio (Gemini API)
def generate_email_content(name, invoice_no, amount, due_date):
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = f"Write a polite email reminder for {name} about an unpaid invoice {invoice_no} of ${amount} due on {due_date}."
    
    response = model.generate_content(prompt)
    return response.text.strip()

# Create MIME message
def create_message(to, subject, body):
    message = MIMEText(body)
    message['to'] = to
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

# Send email via Gmail API
def send_email(service, to, subject, body):
    message = create_message(to, subject, body)
    try:
        sent_message = service.users().messages().send(userId='me', body=message).execute()
        print(f"Email sent to {to}! Message ID: {sent_message['id']}")
    except Exception as e:
        print(f"Error sending email to {to}: {e}")

# Main function
def main():
    creds = authenticate_gmail()
    service = build('gmail', 'v1', credentials=creds)

    # Read CSV and filter unpaid invoices
    df = pd.read_csv(CSV_FILE)
    unpaid_df = df[df['has_paid'].str.lower() == 'no']

    for _, row in unpaid_df.iterrows():
        email = row['email']
        name = row['name']
        invoice_no = row['invoice_no']
        amount = row['amount']
        due_date = row['due_date']
        
        # Generate AI-powered email content
        body = generate_email_content(name, invoice_no, amount, due_date)
        subject = f"Payment Reminder: Invoice {invoice_no}"
        
        # Send email
        send_email(service, email, subject, body)

if __name__ == '__main__':
    main()
