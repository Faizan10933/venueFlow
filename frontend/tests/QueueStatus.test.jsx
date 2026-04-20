import { render, screen } from '@testing-library/react';
import { describe, it, expect } from 'vitest';
import QueueStatus from '../components/QueueStatus';

describe('QueueStatus', () => {
  const mockZones = [
    { id: 'z1', name: 'Gate 1', wait_time_min: 5, occupancy_pct: 0.4, trend: 'stable', type: 'gate' },
    { id: 'z2', name: 'Food Court A', wait_time_min: 15, occupancy_pct: 0.85, trend: 'rising', type: 'food_court' }
  ];

  it('renders nothing if zones array is empty', () => {
    const { container } = render(<QueueStatus zones={[]} title="Test" />);
    expect(container.firstChild).toBeNull();
  });

  it('renders zones correctly sorted by occupancy', () => {
    render(<QueueStatus zones={mockZones} title="Active Queues" icon="🚶‍♂️" />);
    
    // Check title renders
    expect(screen.getByText(/Active Queues/i)).toBeInTheDocument();
    
    // Check zone names render
    expect(screen.getByText('Gate 1')).toBeInTheDocument();
    expect(screen.getByText('Food Court A')).toBeInTheDocument();
    
    // Check wait times render
    expect(screen.getByText('5 min wait')).toBeInTheDocument();
    expect(screen.getByText('15 min wait')).toBeInTheDocument();
    
    // Check ARIA labels generated correctly
    const article1 = screen.getByLabelText(/Gate 1: 5 minutes wait/i);
    expect(article1).toBeInTheDocument();
  });
});
