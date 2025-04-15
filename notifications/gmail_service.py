from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
import os

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('gmail', 'v1', credentials=creds)
    return service

def send_gmail(to_email, subject, body):
    service = get_gmail_service()

    message = MIMEText(body)
    message['to'] = to_email
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    message_body = {
        'raw': raw_message
    }

    send_message = service.users().messages().send(userId="me", body=message_body).execute()

    return send_message
