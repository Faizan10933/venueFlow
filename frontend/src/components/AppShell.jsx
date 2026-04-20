import { useState } from 'react';
import { NavLink } from 'react-router-dom';
import PropTypes from 'prop-types';

const NAV_ITEMS = [
  { path: '/', label: 'Dashboard', icon: '📊' },
  { path: '/chat', label: 'MatchDay AI', icon: '🤖' },
  { path: '/timeline', label: 'Timeline', icon: '📅' },
  { path: '/food', label: 'Food & Pre-Order', icon: '🍔' },
];

export default function AppShell({ children, simTime, phase }) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const phaseLabels = {
    pre_match: 'Pre-Match',
    innings_1: '1st Innings',
    innings_break: 'Innings Break',
    innings_2: '2nd Innings',
    post_match: 'Post-Match',
  };

  return (
    <div className="app-shell">
      <a href="#main-content" className="skip-to-content">
        Skip to main content
      </a>
      {sidebarOpen && <div className="mobile-overlay" onClick={() => setSidebarOpen(false)} />}
      <aside className={`sidebar ${sidebarOpen ? 'open' : ''}`} aria-label="Sidebar Navigation">
        <div className="sidebar-logo">VenueFlow</div>
        <div className="sidebar-subtitle">Smart Stadium Companion</div>
        <nav className="sidebar-nav" aria-label="Main Menu">
          {NAV_ITEMS.map((item) => (
            <NavLink
              key={item.path}
              to={item.path}
              end={item.path === '/'}
              className={({ isActive }) => `nav-item ${isActive ? 'active' : ''}`}
              onClick={() => setSidebarOpen(false)}
              aria-current={({ isActive }) => isActive ? 'page' : undefined}
            >
              <span aria-hidden="true">{item.icon}</span>
              <span>{item.label}</span>
            </NavLink>
          ))}
        </nav>
        <div style={{ borderTop: '1px solid var(--border-glass)', paddingTop: '16px', marginTop: '16px' }}>
          <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '1.5px', marginBottom: '6px' }}>
            Wankhede Stadium
          </div>
          <div style={{ fontSize: '0.82rem', color: 'var(--text-secondary)' }}>
            MI vs CSK • IPL 2026
          </div>
          {simTime && (
            <div style={{ fontSize: '1.2rem', fontFamily: 'var(--font-heading)', fontWeight: 700, color: 'var(--accent-cyan)', marginTop: '8px' }}>
              {simTime}
            </div>
          )}
          {phase && (
            <div style={{ fontSize: '0.72rem', color: 'var(--accent-amber)', marginTop: '4px', fontWeight: 600 }}>
              {phaseLabels[phase] || phase}
            </div>
          )}
        </div>
      </aside>
      <main id="main-content" className="main-content" role="main">
        <button 
          className="mobile-menu-btn" 
          onClick={() => setSidebarOpen(!sidebarOpen)}
          aria-label={sidebarOpen ? "Close menu" : "Open menu"}
          aria-expanded={sidebarOpen}
        >
          ☰
        </button>
        {children}
      </main>
    </div>
  );
}

AppShell.propTypes = {
  children: PropTypes.node.isRequired,
  simTime: PropTypes.string,
  phase: PropTypes.string,
};
