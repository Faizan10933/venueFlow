import PropTypes from 'prop-types';

const TIMELINE = [
  { time: '17:30', event: 'Gates Open', phase: 'pre_match' },
  { time: '18:00', event: 'Early Bird Entry Window', phase: 'pre_match' },
  { time: '18:30', event: 'Peak Entry Rush', phase: 'pre_match' },
  { time: '19:00', event: 'Toss', phase: 'pre_match' },
  { time: '19:30', event: 'First Innings Starts', phase: 'innings_1' },
  { time: '19:45', event: 'Powerplay Ends', phase: 'innings_1' },
  { time: '20:15', event: 'Strategic Timeout 1', phase: 'innings_1' },
  { time: '20:45', event: 'Strategic Timeout 2', phase: 'innings_1' },
  { time: '21:00', event: 'Innings Break — Grab food! 🍔', phase: 'innings_break' },
  { time: '21:20', event: 'Second Innings Starts', phase: 'innings_2' },
  { time: '21:35', event: 'Powerplay Ends', phase: 'innings_2' },
  { time: '22:05', event: 'Strategic Timeout 3', phase: 'innings_2' },
  { time: '22:35', event: 'Strategic Timeout 4', phase: 'innings_2' },
  { time: '22:50', event: 'Match Ends (approx)', phase: 'post_match' },
  { time: '22:55', event: 'Staggered Exit Begins', phase: 'post_match' },
  { time: '23:30', event: 'Venue Clears', phase: 'post_match' },
];

function getTimeMinutes(t) {
  const [h, m] = t.split(':').map(Number);
  return h * 60 + m;
}

export default function EventTimeline({ simTime }) {
  let currentMinutes = 17 * 60 + 30;
  if (simTime) {
    const [h, m] = simTime.split(':').map(Number);
    currentMinutes = h * 60 + m;
  }

  return (
    <div className="timeline-container glass-card">
      <h3>📅 Match Day Timeline</h3>
      <p style={{ fontSize: '0.82rem', color: 'var(--text-secondary)', marginBottom: '20px' }}>
        🏏 MI vs CSK • Wankhede Stadium, Mumbai • IPL 2026
      </p>
      <div className="timeline-list">
        {TIMELINE.map((item, i) => {
          const itemMin = getTimeMinutes(item.time);
          const nextMin = i < TIMELINE.length - 1 ? getTimeMinutes(TIMELINE[i + 1].time) : itemMin + 30;
          const isPast = currentMinutes > nextMin;
          const isActive = currentMinutes >= itemMin && currentMinutes <= nextMin;
          const status = isActive ? 'active' : isPast ? 'past' : '';

          return (
            <div key={i} className={`timeline-item ${status}`}>
              <div className="timeline-dot-col">
                <div className={`timeline-dot ${status}`} />
                {i < TIMELINE.length - 1 && <div className="timeline-line" />}
              </div>
              <div className="timeline-content">
                <div className="timeline-time">{item.time}</div>
                <div className="timeline-event">{item.event}</div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
    </div>
  );
}

EventTimeline.propTypes = {
  simTime: PropTypes.string,
};
