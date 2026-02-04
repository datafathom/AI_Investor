/**
 * MobileDashboard Component Tests
 * Phase 65: Mobile Actions & Quick Emergency Protocols
 */

import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor } from '@testing-library/react';
import MobileDashboard from '../../src/pages/MobileDashboard';
import useMobileStore from '../../src/stores/mobileStore';

// Mock the store
vi.mock('../../src/stores/mobileStore', () => ({
  default: vi.fn(),
}));

describe('MobileDashboard', () => {
  const mockStore = {
    killSwitchActive: false,
    activateKillSwitch: vi.fn(),
    reset: vi.fn(),
  };

  beforeEach(() => {
    vi.clearAllMocks();
    useMobileStore.mockReturnValue(mockStore);
  });

  it('should render mobile dashboard with warden header', () => {
    render(<MobileDashboard />);
    expect(screen.getByText(/Warden: Mobile Quick-Actions/i)).toBeInTheDocument();
  });

  it('should show mobile simulator devices', () => {
    render(<MobileDashboard />);
    expect(screen.getByText(/Device 1: Kill Switch/i)).toBeInTheDocument();
    expect(screen.getByText(/Device 2: Trade Auth/i)).toBeInTheDocument();
    expect(screen.getByText(/Device 3: Alerts/i)).toBeInTheDocument();
  });
});
