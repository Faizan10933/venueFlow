import EventTimeline from '../components/EventTimeline';
import PropTypes from 'prop-types';

export default function TimelinePage({ simTime, timeline, activeIdx }) {
  return (
    <section className="page-container" aria-label="Match Timeline">
      <h2 className="page-title">Match Timeline</h2>
      <div className="timeline-container">
        {timeline.map((event, idx) => {
          const isPast = idx < activeIdx;
          const isActive = idx === activeIdx;
          return (
            <article key={event.phase} className={`timeline-event ${isPast ? 'past' : ''} ${isActive ? 'active' : ''}`}>
              <div className="timeline-time">
                <time dateTime={event.time}>{event.time}</time>
              </div>
              <div className="timeline-dot"></div>
              <div className="timeline-content glass-card">
                <header>
                  <h3 className="timeline-title">{event.title}</h3>
                  <div className="timeline-status" aria-live="polite">
                    {isActive ? 'Current Phase' : isPast ? 'Completed' : 'Upcoming'}
                  </div>
                </header>
                <p className="timeline-desc">{event.description}</p>
                <div className="timeline-tip" aria-label="Pro Tip">
                  💡 {event.tip}
                </div>
              </div>
            </article>
          );
        })}
      </div>
    </section>
  );
}

TimelinePage.propTypes = {
  simTime: PropTypes.string,
  timeline: PropTypes.arrayOf(PropTypes.shape({
    phase: PropTypes.string.isRequired,
    time: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    description: PropTypes.string.isRequired,
    tip: PropTypes.string.isRequired,
  })).isRequired,
  activeIdx: PropTypes.number.isRequired,
};
