import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import ChatPanel from '../components/ChatPanel';

// Mock fetch globally
global.fetch = vi.fn();

describe('ChatPanel', () => {
  it('renders initial welcome message', () => {
    render(<ChatPanel />);
    expect(screen.getByText(/Hey there! I'm MatchDay AI/i)).toBeInTheDocument();
  });

  it('allows user to type in input box', () => {
    render(<ChatPanel />);
    const input = screen.getByLabelText(/Chat input message box/i);
    fireEvent.change(input, { target: { value: 'Where is food?' } });
    expect(input.value).toBe('Where is food?');
  });

  it('disables send button when input is empty', () => {
    render(<ChatPanel />);
    const button = screen.getByLabelText(/Send message/i);
    expect(button).toBeDisabled();
  });

  it('enables send button when input has text', () => {
    render(<ChatPanel />);
    const input = screen.getByLabelText(/Chat input message box/i);
    const button = screen.getByLabelText(/Send message/i);
    
    fireEvent.change(input, { target: { value: 'Where is food?' } });
    expect(button).not.toBeDisabled();
  });

  it('calls fetch when sending a message', async () => {
    fetch.mockResolvedValueOnce({
      json: async () => ({ response: "Food is at Gate 2" })
    });

    render(<ChatPanel />);
    const input = screen.getByLabelText(/Chat input message box/i);
    const button = screen.getByLabelText(/Send message/i);
    
    fireEvent.change(input, { target: { value: 'Where is food?' } });
    fireEvent.click(button);
    
    expect(fetch).toHaveBeenCalledTimes(1);
    
    await waitFor(() => {
      expect(screen.getByText(/Food is at Gate 2/i)).toBeInTheDocument();
    });
  });
});
