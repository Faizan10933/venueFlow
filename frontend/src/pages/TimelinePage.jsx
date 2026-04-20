import EventTimeline from '../components/EventTimeline';

export default function TimelinePage({ simTime }) {
  return (
    <div>
      <div className="top-bar">
        <h1>📅 Match Timeline</h1>
        {simTime && (
          <div className="live-badge">
            <span className="live-dot" />
            {simTime}
          </div>
        )}
      </div>
      <EventTimeline simTime={simTime} />
    </div>
  );
}
