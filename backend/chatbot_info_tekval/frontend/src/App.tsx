import React, { useState, useEffect, useRef } from "react";
import "./chat.css";
import logo from "./assets/logo.png";

interface Risposta {
  domanda?: string;
  risposta: string;
}

// ✅ Frasi di attesa dinamiche TekVal
const frasiAttesa = [
  "🤖 Sto elaborando la tua richiesta con i nostri agenti AI...",
  "💡 Un attimo, l’assistente digitale sta formulando la risposta...",
  "📊 Analizzo i tuoi bisogni per proporti la soluzione TekVal ideale...",
  "🧠 Il nostro sistema intelligente sta pensando alla risposta migliore...",
  "🔧 Genero una risposta basata sui nostri chatbot su misura...",
  "⌛ Un istante, sto preparando informazioni sui nostri servizi AI...",
  "💬 Il nostro cervello digitale è al lavoro per te...",
  "🌐 Sto connettendo i dati per fornirti un supporto smart e personalizzato...",
];


const App: React.FC = () => {
  const [domanda, setDomanda] = useState("");
  const [risposte, setRisposte] = useState<Risposta[]>([]);
  const [loading, setLoading] = useState(false);
  const [frasiAttesa, setFraseAttesa] = useState("");

  // ✅ Ref per scroll automatico
  const endOfChatRef = useRef<HTMLDivElement | null>(null);

  const scrollToBottom = () => {
    endOfChatRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [risposte]);

  const inviaDomanda = async () => {
    if (!domanda.trim()) return;

    const frase = frasiAttesa[Math.floor(Math.random() * frasiAttesa.length)];
    setRisposte((prev) => [...prev, { domanda, risposta: frase }]);
    setDomanda("");
    setFraseAttesa(frase);
    setLoading(true);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ message: domanda }),
      });

      if (!res.ok) {
        const errorText = await res.text();
        console.error("Errore backend:", res.status, errorText);
        alert(`Errore ${res.status}: ${errorText}`);
        setLoading(false);
        return;
      }

      const data = await res.json();

      setRisposte((prev) => {
        const ultime = [...prev];
        ultime[ultime.length - 1] = {
          domanda: ultime[ultime.length - 1].domanda,
          risposta: data.risposta,
        };
        return ultime;
      });

      setDomanda("");
    } catch (err) {
      alert("Errore nella richiesta");
      console.error(err);
    }

    setLoading(false);
    setFraseAttesa("");
  };

  useEffect(() => {
    const messaggioIniziale = {
      risposta: "Ciao! Sono l'assistente di TekVal. Se hai dubbi su quali sono i servizi che offriamo e come si possono integrare con il tuo settore/buisness ti aiuto volentieri a capire meglio.",
    };
    setRisposte([messaggioIniziale]);
  }, []);

  return (
    <div className="chat-container">
      <div className="header">
        <img src={logo} alt="TekVal Logo" className="logo" />
        <h1>Marinetti Edilizia – Assistente Virtuale</h1>
      </div>

      <div className="chat-box">
        {risposte.map((r, i) => (
          <div key={i} className="msg-block">
            {r.domanda && <div className="msg-user">🙋 {r.domanda}</div>}
            <div className="msg-bot">{r.risposta}</div>
          </div>
        ))}
        {/* 🔽 Punto di scroll automatico */}
        <div ref={endOfChatRef} />
      </div>

      <div className="input-row">
        <input
          type="text"
          placeholder="Scrivi la tua domanda..."
          value={domanda}
          onChange={(e) => setDomanda(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && inviaDomanda()}
          disabled={loading}
        />
        <button onClick={inviaDomanda} disabled={loading}>
          {loading ? "..." : "Invia"}
        </button>
      </div>
    </div>
  );
};

export default App;
