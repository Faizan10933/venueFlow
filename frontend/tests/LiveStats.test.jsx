import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import LiveStats from '../src/components/LiveStats';

describe('LiveStats Component', () => {
  it('renders nothing if no summary is provided', () => {
    const { container } = render(<LiveStats />);
    expect(container.firstChild).toBeNull();
  });

  it('renders all 4 stat cards when summary is provided', () => {
    const mockSummary = {
      attendance_pct: 75,
      total_attendance: 25000,
      avg_food_wait: 5,
      avg_restroom_wait: 2,
      busiest_zone_pct: 90,
      busiest_zone: 'North Stand'
    };

    render(<LiveStats summary={mockSummary} />);
    
    // Check if labels exist
    expect(screen.getByText('Attendance')).toBeInTheDocument();
    expect(screen.getByText('Avg Food Wait')).toBeInTheDocument();
    expect(screen.getByText('Avg Restroom Wait')).toBeInTheDocument();
    expect(screen.getByText('Busiest Zone')).toBeInTheDocument();

    // Check if values exist
    expect(screen.getByText('75%')).toBeInTheDocument();
    expect(screen.getByText('25,000 fans')).toBeInTheDocument();
    expect(screen.getByText('5m')).toBeInTheDocument();
    expect(screen.getByText('North Stand')).toBeInTheDocument();
  });
});
