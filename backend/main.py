from fastapi import FastAPI, Form
import smtplib
from email.message import EmailMessage

app = FastAPI()

@app.post("/api/contact")
def parse_form(
    name: str = Form(...),
    email: str = Form(...),
    descrizione: str = Form(...)
):
    # Costruisci l'email
    msg = EmailMessage()
    msg["From"] = "federicosileoni892@gmail.com"
    msg["To"] = "destinatario@tekval.it"
    msg["Subject"] = f"Nuovo messaggio dal sito da {email}"
    msg.set_content(f"{name}\n\nEmail: {email}\n\nMessaggio:\n{descrizione}")

    # Invia email (con SMTP SSL)
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login("federicosileoni892@gmail.com", "la-tua-password-app")
        smtp.send_message(msg)

    return {"message": "Messaggio inviato con successo!"}
