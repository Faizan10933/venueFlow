import ChatPanel from '../components/ChatPanel';

export default function ChatPage() {
  return (
    <div>
      <div className="top-bar">
        <h1>🤖 MatchDay AI</h1>
        <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
          Your intelligent stadium assistant
        </div>
      </div>
      <ChatPanel />
    </div>
  );
}
