export default function AlertsFeed({ alerts }) {
  if (!alerts || alerts.length === 0) {
    return (
      <div className="alerts-container glass-card">
        <h3>🔔 Live Alerts</h3>
        <div style={{ color: 'var(--text-muted)', fontSize: '0.85rem', textAlign: 'center', padding: '40px 0' }}>
          No alerts yet. Monitoring stadium...
        </div>
      </div>
    );
  }

  return (
    <div className="alerts-container glass-card">
      <h3>🔔 Live Alerts <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', fontWeight: 400 }}>({alerts.length})</span></h3>
      <div className="alerts-list" role="status" aria-live="polite">
        {alerts.map((alert) => (
          <div key={alert.id} className={`alert-item ${alert.type}`}>
            <div>{alert.message}</div>
            <div className="alert-time">{alert.time}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
