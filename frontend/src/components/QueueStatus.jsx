function getBarColor(pct) {
  if (pct >= 0.8) return 'var(--accent-red)';
  if (pct >= 0.6) return 'var(--accent-amber)';
  if (pct >= 0.35) return '#eab308';
  return 'var(--accent-green)';
}

export default function QueueStatus({ zones, title, icon }) {
  if (!zones || zones.length === 0) return null;

  const filtered = zones
    .filter((z) => z.type === 'food_court' || z.type === 'restroom' || z.type === 'gate')
    .sort((a, b) => a.occupancy_pct - b.occupancy_pct);

  return (
    <div>
      <div className="section-header">{icon} {title}</div>
      <div className="queue-grid">
        {filtered.map((zone) => (
          <div key={zone.id} className="glass-card queue-card">
            <div className="queue-name">
              <span>{zone.name}</span>
              <span className={`trend-badge ${zone.trend}`}>
                {zone.trend === 'rising' ? '↑' : zone.trend === 'falling' ? '↓' : '→'}
              </span>
            </div>
            <div className="queue-bar-bg">
              <div
                className="queue-bar-fill"
                style={{
                  width: `${Math.round(zone.occupancy_pct * 100)}%`,
                  background: getBarColor(zone.occupancy_pct),
                }}
              />
            </div>
            <div className="queue-wait">
              <span>{Math.round(zone.occupancy_pct * 100)}% full</span>
              {zone.wait_time_min > 0 && <span>~{zone.wait_time_min} min wait</span>}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
