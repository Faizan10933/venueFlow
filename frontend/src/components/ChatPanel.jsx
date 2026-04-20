import { useState, useRef, useEffect } from 'react';
import DOMPurify from 'dompurify';

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
  const [language, setLanguage] = useState('English');
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

  const speakText = (text) => {
    // Strip markdown for speech
    const cleanText = text.replace(/[*_#~`]/g, '').replace(/[\u{1F300}-\u{1F9FF}]/gu, '');
    const utterance = new SpeechSynthesisUtterance(cleanText);
    if (language === 'Hindi') utterance.lang = 'hi-IN';
    else if (language === 'Marathi') utterance.lang = 'mr-IN';
    else utterance.lang = 'en-US';
    window.speechSynthesis.speak(utterance);
  };

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
        body: JSON.stringify({ message: msg, language }),
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
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px', borderBottom: '1px solid var(--border-glass)', paddingBottom: '8px' }}>
        <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
          Powered by Google Gemini 🌍
        </div>
        <select 
          value={language} 
          onChange={(e) => setLanguage(e.target.value)}
          style={{ background: 'rgba(255,255,255,0.1)', color: 'white', border: 'none', padding: '4px 8px', borderRadius: '4px', fontSize: '0.8rem' }}
          aria-label="Select Language"
        >
          <option value="English">🇬🇧 English</option>
          <option value="Hindi">🇮🇳 Hindi</option>
          <option value="Marathi">🚩 Marathi</option>
        </select>
      </div>

      <div className="chat-messages">
        {messages.map((msg, i) => (
          <div key={i} style={{ display: 'flex', flexDirection: 'column', alignItems: msg.role === 'user' ? 'flex-end' : 'flex-start' }}>
            <div
              className={`chat-bubble ${msg.role}`}
              dangerouslySetInnerHTML={{ __html: DOMPurify.sanitize(formatMessage(msg.content)) }}
            />
            {msg.role === 'assistant' && i > 0 && (
              <button 
                onClick={() => speakText(msg.content)}
                style={{ background: 'none', border: 'none', color: 'var(--accent-blue)', fontSize: '0.75rem', marginTop: '4px', cursor: 'pointer' }}
                aria-label="Read out loud (Google Text-to-Speech)"
              >
                🔊 Listen (TTS)
              </button>
            )}
          </div>
        ))}
        {loading && (
          <div className="chat-bubble assistant" style={{ opacity: 0.6 }} aria-busy="true" aria-live="polite">
            <span className="sr-only" style={{ position: 'absolute', width: '1px', height: '1px', padding: 0, margin: '-1px', overflow: 'hidden', clip: 'rect(0, 0, 0, 0)', whiteSpace: 'nowrap', borderWidth: 0 }}>MatchDay AI is typing...</span>
            <span style={{ display: 'inline-flex', gap: '4px' }} aria-hidden="true">
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
        <label htmlFor="chat-input-box" className="sr-only" style={{ position: 'absolute', width: '1px', height: '1px', padding: 0, margin: '-1px', overflow: 'hidden', clip: 'rect(0, 0, 0, 0)', whiteSpace: 'nowrap', borderWidth: 0 }}>Type your message for MatchDay AI</label>
        <input
          id="chat-input-box"
          className="chat-input"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Ask MatchDay AI anything..."
          disabled={loading}
          aria-disabled={loading}
          aria-label="Chat input message box"
        />
        <button 
          className="chat-send-btn" 
          onClick={() => sendMessage()} 
          disabled={loading || !input.trim()}
          aria-disabled={loading || !input.trim()}
          aria-label="Send message"
        >
          Send
        </button>
      </div>
    </div>
  );
}
