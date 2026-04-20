import PropTypes from 'prop-types';

export default function LiveStats({ summary, zones }) {
  if (!summary) return null;

  return (
    <section className="stats-grid" aria-label="Key Stadium Statistics">
      <article className="stat-card glass-card">
        <div className="stat-label">Attendance</div>
        <div className="stat-value">{summary.attendance_pct}%</div>
        <div className="stat-sub">{summary.total_attendance.toLocaleString()} fans</div>
      </article>
      
      <article className="stat-card glass-card">
        <div className="stat-label">Avg Food Wait</div>
        <div className="stat-value">{summary.avg_food_wait}m</div>
        <div className="stat-sub">across {zones.filter(z => z.type === 'food_court').length} courts</div>
      </article>

      <article className="stat-card glass-card">
        <div className="stat-label">Avg Restroom Wait</div>
        <div className="stat-value">{summary.avg_restroom_wait}m</div>
        <div className="stat-sub">across {zones.filter(z => z.type === 'restroom').length} blocks</div>
      </article>

      <article className="stat-card glass-card">
        <div className="stat-label">Busiest Zone</div>
        <div className="stat-value" style={{ fontSize: '1.2rem', marginTop: '8px' }}>
          {summary.busiest_zone}
        </div>
        <div className="stat-sub">{summary.busiest_zone_pct}% capacity</div>
      </article>
    </section>
  );
}

LiveStats.propTypes = {
  summary: PropTypes.shape({
    attendance_pct: PropTypes.number,
    total_attendance: PropTypes.number,
    avg_food_wait: PropTypes.number,
    avg_restroom_wait: PropTypes.number,
    busiest_zone: PropTypes.string,
    busiest_zone_pct: PropTypes.number,
  }),
  zones: PropTypes.arrayOf(PropTypes.shape({
    type: PropTypes.string.isRequired,
  }))
};
