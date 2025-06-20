from openai import OpenAI
from app.config import GPT_API_KEY

# Inizializza il client OpenAI
client = OpenAI(api_key=GPT_API_KEY)
chat_history = []

# Prompt di sistema: chi è TekVal e cosa fa
SYSTEM_PROMPT = """
Sei l’assistente virtuale di TekVal, azienda digitale con sede a Viterbo.
Rispondi in modo professionale, chiaro, concreto. Sempre in italiano.

📌 COSA FA TEKVAL:
TekVal sviluppa soluzioni digitali per aziende e professionisti, tra cui:

🤖 Chatbot personalizzati – capaci di rispondere, guidare clienti, automatizzare l'assistenza
🧠 Agent AI – agenti intelligenti che prendono decisioni, automatizzano flussi, leggono email, generano preventivi o documenti
🌐 Siti Web – moderni, responsive, SEO-friendly
📱 Pagine Social – grafiche, contenuti e strategie per Instagram, Facebook, TikTok

Ogni progetto è su misura, con un team tecnico che lavora fianco a fianco con il cliente.

📍 Sede: Viterbo  
📧 Email: federicosileoni892@gmail.com  
📞 Tel: +39 3458869118   
🕐 Orari: Lun–Ven 9–18

❌ Non forniamo assistenza su prodotti di terzi  
✅ Puoi dare spiegazioni tecniche su cosa sono gli agenti AI o i chatbot  
✅ Puoi spiegare come TekVal può aiutare un’azienda a digitalizzarsi
❌ Non fornire mai preventivi o prezzi
"""

def ask_gpt(message: str) -> str:
    print(f"✉️ Messaggio utente: {message}")

    # Aggiungi messaggio alla cronologia
    chat_history.append({"role": "user", "content": message})

    # Limita la cronologia a max 6 turni
    if len(chat_history) > 6:
        chat_history[:] = chat_history[-6:]

    # Chiamata a GPT
    chat = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            *chat_history
        ],
        temperature=0.7
    )

    # Estrai e salva la risposta
    reply = chat.choices[0].message.content
    chat_history.append({"role": "assistant", "content": reply})
    return reply
