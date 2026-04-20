import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import TimelinePage from '../pages/TimelinePage';

describe('TimelinePage', () => {
  const mockTimeline = [
    { phase: 'pre_match', time: '17:30', title: 'Gates Open', description: 'desc', tip: 'tip1' },
    { phase: 'innings_1', time: '19:30', title: 'First Ball', description: 'desc2', tip: 'tip2' }
  ];

  it('renders timeline events correctly', () => {
    render(<TimelinePage simTime="18:00" timeline={mockTimeline} activeIdx={0} />);
    
    expect(screen.getByText('Gates Open')).toBeInTheDocument();
    expect(screen.getByText('First Ball')).toBeInTheDocument();
  });

  it('marks active event with Current Phase', () => {
    render(<TimelinePage simTime="18:00" timeline={mockTimeline} activeIdx={0} />);
    
    const activeStatus = screen.getByText('Current Phase');
    expect(activeStatus).toBeInTheDocument();
    
    // The second event should be upcoming
    const upcomingStatus = screen.getByText('Upcoming');
    expect(upcomingStatus).toBeInTheDocument();
  });
});
