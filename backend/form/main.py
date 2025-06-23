from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

# 🔁 Carica il file .env
load_dotenv()

# 🔐 Leggi le variabili di ambiente
email_user = os.getenv("EMAIL_USER")
email_pass = os.getenv("EMAIL_PASS")
email_to = os.getenv("EMAIL_TO")

# ✅ Inizializza l'app
app = FastAPI()

# 🌍 Abilita CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tekval.ai"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📬 API endpoint
@app.post("/api/contact")
def parse_form(
    name: str = Form(...),
    email: str = Form(...),
    message: str = Form(...)
):
    if not all([email_user, email_pass, email_to]):
        raise HTTPException(status_code=500, detail="Variabili di ambiente mancanti.")

    # 📝 Crea l'email
    msg = EmailMessage()
    msg["From"] = email_user
    msg["To"] = email_to
    msg["Subject"] = f"Nuovo messaggio dal sito da {email}"
    msg.set_content(f"{name}\n\nEmail: {email}\n\nMessaggio:\n{message}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(email_user, email_pass)
            smtp.send_message(msg)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Errore invio email: {str(e)}")

    return {"message": "Messaggio inviato con successo!"}
