import React from 'react';
import { render, screen } from '@testing-library/react';
import DeploymentController from '../pages/admin/DeploymentController';
import { vi } from 'vitest';

// Mock sub-components
vi.mock('@/components/cards/EnvironmentCard', () => ({ default: () => <div>Env Card</div> }));
vi.mock('@/components/controls/TrafficSlider', () => ({ default: () => <div>Traffic Slider</div> }));
vi.mock('@/components/Admin/DeploymentTimeline', () => ({ default: () => <div>Timeline</div> }));
vi.mock('@/components/modals/RollbackConfirmModal', () => ({ default: () => <div>Rollback Modal</div> }));

// Mock apiClient
vi.mock('../services/apiClient', () => ({
    default: {
        get: vi.fn(() => Promise.resolve({
            environments: { blue: {}, green: {} },
            traffic_split: { blue: 50, green: 50 }
        })),
    }
}));

describe('DeploymentController Component', () => {
    it('renders the infrastructure operations header', async () => {
        render(<DeploymentController />);
        expect(await screen.findByText(/Infrastructure Operations/i)).toBeTruthy();
    });
});
