import smtplib
from email.message import EmailMessage

from dotenv import load_dotenv
import os
load_dotenv()
app_password=os.environ["APP_PASSWORD"]
sender_email=os.environ["SENDER_EMAIL"]

def send_email(RECEIVER_EMAIL: str, subject: str, content: str) -> str:
    """ Send an email to the specified receiver."""
    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = RECEIVER_EMAIL
    msg["Subject"] = "Hello from Python 🐍"

    msg.set_content(content)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, app_password)
        server.send_message(msg)

    print("Email sent successfully!")
    return "Email sent successfully!"
