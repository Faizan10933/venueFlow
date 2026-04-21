import React, { useMemo } from 'react';
import LiveStats from '../components/LiveStats';
import PropTypes from 'prop-types';
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

  const foodZones = useMemo(() => state.zones?.filter((z) => z.type === 'food_court') || [], [state.zones]);
  const restroomZones = useMemo(() => state.zones?.filter((z) => z.type === 'restroom') || [], [state.zones]);
  const gateZones = useMemo(() => state.zones?.filter((z) => z.type === 'gate') || [], [state.zones]);

  return (
    <div>
      <div className="top-bar">
        <h1>Live Dashboard</h1>
        <div className="live-badge">
          <span className="live-dot" />
          LIVE • {state.sim_time?.display}
        </div>
      </div>

      <LiveStats summary={state.summary} zones={state.zones} />

      <div className="dashboard-grid">
        <StadiumMap zones={state.zones} />
        <AlertsFeed alerts={state.alerts} />
      </div>

      <QueueStatus
        zones={foodZones}
        title="Food Court Status"
        icon="🍔"
      />

      <div style={{ marginTop: '24px' }}>
        <QueueStatus
          zones={restroomZones}
          title="Restroom Status"
          icon="🚻"
        />
      </div>

      <div style={{ marginTop: '24px' }}>
        <QueueStatus
          zones={gateZones}
          title="Gate Status"
          icon="🚪"
        />
      </div>

      <div style={{ marginTop: '24px' }} className="glass-card">
        <h3>📍 Google Maps: Wankhede Stadium Live Traffic</h3>
        <iframe
          title="Google Maps Wankhede Stadium"
          width="100%"
          height="300"
          style={{ border: 0, borderRadius: 'var(--radius-md)', marginTop: '12px' }}
          loading="lazy"
          allowFullScreen
          src="https://www.google.com/maps/embed/v1/place?key=AIzaSyB-xv5YIRnBO9GRMCqsc8GtpcEq0ZLf0wQ&q=Wankhede+Stadium,Mumbai"
        ></iframe>
      </div>
    </div>
  );
}

DashboardPage.propTypes = {
  state: PropTypes.shape({
    summary: PropTypes.object,
    zones: PropTypes.array,
  })
};
