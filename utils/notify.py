import os
import streamlit as st 
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()
def send_completion_email(base_url, total_pages):
    sender_password = os.getenv("SENDER_PASSKEY")
    recipient_email = os.getenv("RECIPIENT_MAIL")
    sender_email = os.getenv("SENDER_MAIL")
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = recipient_email
    message["Subject"] = "Web Scraping Completed"

    body = f"The web scraping process for {base_url} has been completed. {total_pages} pages were scraped."
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())
        return True
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")
        return False