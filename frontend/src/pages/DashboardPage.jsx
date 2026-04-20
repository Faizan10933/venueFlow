import LiveStats from '../components/LiveStats';
import StadiumMap from '../components/StadiumMap';
import AlertsFeed from '../components/AlertsFeed';
import QueueStatus from '../components/QueueStatus';

export default function DashboardPage({ state }) {
  if (!state) {
    return (
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '60vh' }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{ fontSize: '2.5rem', marginBottom: '16px', animation: 'pulse-dot 2s infinite' }}>🏟️</div>
          <div style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>Connecting to stadium...</div>
        </div>
      </div>
    );
  }

  return (
    <div>
      <div className="top-bar">
        <h1>Live Dashboard</h1>
        <div className="live-badge">
          <span className="live-dot" />
          LIVE • {state.sim_time?.display}
        </div>
      </div>

      <LiveStats summary={state.summary} />

      <div className="dashboard-grid">
        <StadiumMap zones={state.zones} />
        <AlertsFeed alerts={state.alerts} />
      </div>

      <QueueStatus
        zones={state.zones?.filter((z) => z.type === 'food_court')}
        title="Food Court Status"
        icon="🍔"
      />

      <div style={{ marginTop: '24px' }}>
        <QueueStatus
          zones={state.zones?.filter((z) => z.type === 'restroom')}
          title="Restroom Status"
          icon="🚻"
        />
      </div>

      <div style={{ marginTop: '24px' }}>
        <QueueStatus
          zones={state.zones?.filter((z) => z.type === 'gate')}
          title="Gate Status"
          icon="🚪"
        />
      </div>
    </div>
  );
}
