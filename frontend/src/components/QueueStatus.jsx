import PropTypes from 'prop-types';

function getBarColor(pct) {
  if (pct >= 0.8) return 'var(--accent-red)';
  if (pct >= 0.6) return 'var(--accent-amber)';
  if (pct >= 0.35) return '#eab308';
  return 'var(--accent-green)';
}

export default function QueueStatus({ zones, title, icon }) {
  if (!zones || zones.length === 0) return null;

  const sortedZones = zones
    .filter((z) => z.type === 'food_court' || z.type === 'restroom' || z.type === 'gate')
    .sort((a, b) => a.occupancy_pct - b.occupancy_pct);

  return (
    <section className="glass-card" aria-label={title}>
      <h3 className="section-header">{icon} {title}</h3>
      <div className="queue-grid">
        {sortedZones.map((zone) => {
          const pct = zone.occupancy_pct * 100;
          return (
            <article key={zone.id} className="glass-card queue-card" aria-label={`${zone.name}: ${zone.wait_time_min} minutes wait, ${Math.round(pct)}% full`}>
              <div className="queue-name">
                <span>{zone.name}</span>
                <span className={`trend-badge ${zone.trend}`} aria-hidden="true">
                  {zone.trend === 'rising' ? '↑' : zone.trend === 'falling' ? '↓' : '→'}
                </span>
              </div>
              <div className="queue-bar-bg" aria-hidden="true">
                <div 
                  className="queue-bar-fill" 
                  style={{ 
                    width: `${pct}%`,
                    background: pct > 80 ? 'var(--accent-red)' : pct > 50 ? 'var(--accent-amber)' : 'var(--accent-green)'
                  }}
                />
              </div>
              <div className="queue-wait">
                <span>{Math.round(zone.occupancy_pct * 100)}% full</span>
                {zone.wait_time_min > 0 && <span>~{zone.wait_time_min} min wait</span>}
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}

QueueStatus.propTypes = {
  zones: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.string.isRequired,
    type: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    occupancy_pct: PropTypes.number.isRequired,
    wait_time_min: PropTypes.number.isRequired,
    trend: PropTypes.string.isRequired,
  })),
  title: PropTypes.string.isRequired,
  icon: PropTypes.string,
};
