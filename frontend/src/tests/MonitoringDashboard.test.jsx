import React from 'react';
import { render, screen } from '@testing-library/react';
import MonitoringDashboard from '../pages/admin/MonitoringDashboard';
import { vi } from 'vitest';

// Mock apiClient
vi.mock('../services/apiClient', () => ({
    default: {
        get: vi.fn(() => Promise.resolve([])),
    }
}));

describe('MonitoringDashboard Component', () => {
    it('renders the infrastructure metric dashboard header', async () => {
        render(<MonitoringDashboard />);
        expect(await screen.findByText(/INFRASTRUCTURE_METRIC_DASHBOARD/i)).toBeTruthy();
    });
});
