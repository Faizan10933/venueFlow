export default function LiveStats({ summary }) {
  if (!summary) return null;
  const stats = [
    { label: 'Attendance', value: `${summary.attendance_pct}%`, detail: `${summary.total_attendance.toLocaleString()} fans`, color: 'blue' },
    { label: 'Avg Food Wait', value: `${summary.avg_food_wait}m`, detail: 'Across all courts', color: 'amber' },
    { label: 'Avg Restroom Wait', value: `${summary.avg_restroom_wait}m`, detail: 'Across all blocks', color: 'cyan' },
    { label: 'Busiest Zone', value: `${summary.busiest_zone_pct}%`, detail: summary.busiest_zone, color: 'red' },
  ];
  return (
    <div className="stats-grid">
      {stats.map((s) => (
        <div key={s.label} className="glass-card stat-card">
          <span className="stat-label">{s.label}</span>
          <span className={`stat-value ${s.color}`}>{s.value}</span>
          <span className="stat-detail">{s.detail}</span>
        </div>
      ))}
    </div>
  );
}
