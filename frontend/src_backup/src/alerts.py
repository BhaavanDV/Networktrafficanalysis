# src/alerts.py
import smtplib
from email.message import EmailMessage

def alert_attack(row_index, label):
    print(f"ALERT: Row {row_index} detected as {label}!")

def send_email_alert(subject, body, to_email="you@example.com"):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = "network.alerts@example.com"
    msg["To"] = to_email

    # SMTP example (use Gmail/Outlook SMTP)
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login("your_email@gmail.com", "your_app_password")
            server.send_message(msg)
        print("Email alert sent!")
    except Exception as e:
        print("Email failed:", e)