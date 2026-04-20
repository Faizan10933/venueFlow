import { useState, memo, useCallback, useRef } from 'react';
import PropTypes from 'prop-types';

function getZoneColor(pct) {
  if (pct >= 0.85) return '#ef4444';
  if (pct >= 0.7) return '#f59e0b';
  if (pct >= 0.45) return '#eab308';
  if (pct >= 0.25) return '#22c55e';
  return '#10b981';
}

function getZoneOpacity(pct) {
  return 0.35 + pct * 0.55;
}

const StadiumMap = memo(function StadiumMap({ zones }) {
  const [hoveredZone, setHoveredZone] = useState(null);
  const [selectedZone, setSelectedZone] = useState(null);
  
  // Throttle hover events to ~30fps for extreme efficiency
  const throttleTimer = useRef(null);
  const handleMouseEnter = useCallback((zone) => {
    if (throttleTimer.current) return;
    throttleTimer.current = setTimeout(() => {
      setHoveredZone(zone);
      throttleTimer.current = null;
    }, 32);
  }, []);

  if (!zones || zones.length === 0) return null;

  const displayZone = selectedZone || hoveredZone;

  return (
    <div className="stadium-map-container glass-card" aria-label="Stadium Map View">
      <h3>🏟️ Live Crowd Heatmap</h3>
      <svg 
        viewBox="0 0 500 500" 
        className="stadium-svg"
        role="application"
        aria-label="Interactive map of Wankhede Stadium showing real-time crowd density"
      >
        <title>Stadium Crowd Density Heatmap</title>
        {/* Stadium outline */}
        <ellipse cx="250" cy="250" rx="220" ry="220" fill="none" stroke="rgba(255,255,255,0.08)" strokeWidth="2" />
        {/* Pitch */}
        <ellipse cx="250" cy="250" rx="70" ry="45" fill="rgba(16,185,129,0.12)" stroke="rgba(16,185,129,0.25)" strokeWidth="1" />
        <text x="250" y="253" textAnchor="middle" fill="rgba(16,185,129,0.4)" fontSize="8" fontWeight="600" aria-hidden="true">PITCH</text>

        {/* Zones */}
        {zones.map((zone) => {
          const color = getZoneColor(zone.occupancy_pct);
          const opacity = getZoneOpacity(zone.occupancy_pct);
          const isHovered = hoveredZone?.id === zone.id;
          const isSelected = selectedZone?.id === zone.id;
          const isHighlighted = isHovered || isSelected;

          return (
            <g key={zone.id}
              onMouseEnter={() => handleMouseEnter(zone)}
              onMouseLeave={() => setHoveredZone(null)}
              onClick={() => setSelectedZone(selectedZone?.id === zone.id ? null : zone)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                  e.preventDefault();
                  setSelectedZone(selectedZone?.id === zone.id ? null : zone);
                }
              }}
              tabIndex={0}
              role="button"
              aria-label={`${zone.name}, ${Math.round(zone.occupancy_pct * 100)}% full`}
              aria-pressed={isSelected}
            >
              <ellipse
                cx={zone.cx} cy={zone.cy}
                rx={zone.rx * (isHighlighted ? 1.1 : 1)}
                ry={zone.ry * (isHighlighted ? 1.1 : 1)}
                fill={color}
                opacity={opacity}
                className="zone-shape"
                style={{
                  filter: isHighlighted ? `drop-shadow(0 0 8px ${color})` : 'none',
                }}
              />
              <text x={zone.cx} y={zone.cy - 2} className="zone-label">
                {zone.name.length > 14 ? zone.name.slice(0, 12) + '…' : zone.name}
              </text>
              <text x={zone.cx} y={zone.cy + 8} className="zone-pct">
                {Math.round(zone.occupancy_pct * 100)}%
              </text>
            </g>
          );
        })}
      </svg>

      {/* Legend */}
      <div className="map-legend">
        <div className="legend-item">
          <div className="legend-dot" style={{ background: '#10b981' }} /> Low
        </div>
        <div className="legend-item">
          <div className="legend-dot" style={{ background: '#eab308' }} /> Medium
        </div>
        <div className="legend-item">
          <div className="legend-dot" style={{ background: '#f59e0b' }} /> High
        </div>
        <div className="legend-item">
          <div className="legend-dot" style={{ background: '#ef4444' }} /> Critical
        </div>
      </div>

      {/* Zone Detail Popup */}
      {displayZone && (
        <div 
          role="region"
          aria-live="polite"
          style={{
          marginTop: '16px',
          padding: '14px',
          background: 'rgba(255,255,255,0.05)',
          borderRadius: 'var(--radius-md)',
          border: '1px solid rgba(255,255,255,0.1)',
          animation: 'fadeUp 0.2s ease',
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '8px' }}>
            <strong style={{ fontSize: '0.9rem' }}>{displayZone.name}</strong>
            <span className={`trend-badge ${displayZone.trend}`}>
              {displayZone.trend === 'rising' ? '↑ Rising' : displayZone.trend === 'falling' ? '↓ Falling' : '→ Stable'}
            </span>
          </div>
          <div style={{ display: 'flex', gap: '20px', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
            <span>Occupancy: <strong style={{ color: getZoneColor(displayZone.occupancy_pct) }}>{Math.round(displayZone.occupancy_pct * 100)}%</strong></span>
            <span>Count: {displayZone.current_occupancy}/{displayZone.capacity}</span>
            {displayZone.wait_time_min > 0 && <span>Wait: ~{displayZone.wait_time_min} min</span>}
          </div>
        </div>
      )}
    </div>
  );
});

StadiumMap.propTypes = {
  zones: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.string.isRequired,
      name: PropTypes.string.isRequired,
      occupancy_pct: PropTypes.number.isRequired,
      current_occupancy: PropTypes.number.isRequired,
      capacity: PropTypes.number.isRequired,
      wait_time_min: PropTypes.number.isRequired,
      trend: PropTypes.string.isRequired,
      cx: PropTypes.number.isRequired,
      cy: PropTypes.number.isRequired,
      rx: PropTypes.number.isRequired,
      ry: PropTypes.number.isRequired,
    })
  ).isRequired,
};

export default StadiumMap;
