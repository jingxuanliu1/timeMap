from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.template.loader import render_to_string
from django.conf import settings
import base64
import os

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    service = build('gmail', 'v1', credentials=creds)
    return service

def send_gmail(to_email, subject, body, html_body=None):
    service = get_gmail_service()

    message = MIMEMultipart("alternative")
    message["to"] = to_email
    message["subject"] = subject

    # Plain version
    part1 = MIMEText(body, "plain")
    message.attach(part1)

    # HTML version
    if html_body:
        part2 = MIMEText(html_body, "html")
        message.attach(part2)

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    message_body = {'raw': raw_message}
    service.users().messages().send(userId="me", body=message_body).execute()
