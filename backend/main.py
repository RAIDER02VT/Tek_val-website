from fastapi import FastAPI, Form
import smtplib
from email.message import EmailMessage
import os

email_user = os.getenv("EMAIL_USER")
email_pass = os.getenv("EMAIL_PASS")
email_to = os.getenv("EMAIL_TO")

app = FastAPI()

@app.post("/api/contact")
def parse_form(
    name: str = Form(...),
    email: str = Form(...),
    descrizione: str = Form(...)
):
    # Costruisci l'email
    msg = EmailMessage()
    msg["From"] = email_user
    msg["To"] = email_to
    msg["Subject"] = f"Nuovo messaggio dal sito da {email}"
    msg.set_content(f"{name}\n\nEmail: {email}\n\nMessaggio:\n{descrizione}")

    # Invia email (con SMTP SSL)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(email_user, email_pass)
        smtp.send_message(msg)

    return {"message": "Messaggio inviato con successo!"}
