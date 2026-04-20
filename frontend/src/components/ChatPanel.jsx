import { useState, useRef, useEffect } from 'react';

const API_BASE = '';

const SUGGESTIONS = [
  "Where should I eat?",
  "Nearest restroom with no line?",
  "Which gate should I use?",
  "When is the innings break?",
  "How crowded is it right now?",
  "I need medical help",
];

export default function ChatPanel() {
  const [messages, setMessages] = useState([
    {
      role: 'assistant',
      content: `👋 **Hey there! I'm MatchDay AI**\n\nI can help you with:\n• 🍔 **Food** — "Where should I eat?"\n• 🚻 **Restrooms** — "Nearest low-wait restroom"\n• 🚪 **Gates** — "Which gate should I use?"\n• 📅 **Schedule** — "When is the innings break?"\n• 📊 **Crowd** — "How crowded is it?"\n• 🆘 **Emergency** — "I need medical help"\n\nJust type your question! I have real-time stadium data. 🏟️`,
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const sendMessage = async (text) => {
    const msg = text || input.trim();
    if (!msg || loading) return;
    setInput('');
    setMessages((prev) => [...prev, { role: 'user', content: msg }]);
    setLoading(true);

    try {
      const res = await fetch(`${API_BASE}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: msg }),
      });
      const data = await res.json();
      setMessages((prev) => [...prev, { role: 'assistant', content: data.response }]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: 'assistant', content: '⚠️ Unable to connect to the server. Please make sure the backend is running on port 8000.' },
      ]);
    }
    setLoading(false);
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const formatMessage = (text) => {
    return text
      .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
      .replace(/\n/g, '<br/>');
  };

  return (
    <div className="glass-card chat-container">
      <div className="chat-messages">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`chat-bubble ${msg.role}`}
            dangerouslySetInnerHTML={{ __html: formatMessage(msg.content) }}
          />
        ))}
        {loading && (
          <div className="chat-bubble assistant" style={{ opacity: 0.6 }}>
            <span style={{ display: 'inline-flex', gap: '4px' }}>
              <span style={{ animation: 'pulse-dot 1s infinite 0s' }}>●</span>
              <span style={{ animation: 'pulse-dot 1s infinite 0.2s' }}>●</span>
              <span style={{ animation: 'pulse-dot 1s infinite 0.4s' }}>●</span>
            </span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      {messages.length <= 1 && (
        <div className="chat-suggestions">
          {SUGGESTIONS.map((s) => (
            <button key={s} className="suggestion-chip" onClick={() => sendMessage(s)}>
              {s}
            </button>
          ))}
        </div>
      )}
      <div className="chat-input-area">
        <input
          className="chat-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask MatchDay AI anything..."
          disabled={loading}
        />
        <button className="chat-send-btn" onClick={() => sendMessage()} disabled={loading || !input.trim()}>
          Send
        </button>
      </div>
    </div>
  );
}
