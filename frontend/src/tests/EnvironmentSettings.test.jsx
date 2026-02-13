import React from 'react';
import { render, screen } from '@testing-library/react';
import EnvironmentSettings from '../pages/admin/EnvironmentSettings';
import { vi } from 'vitest';

// Mock sub-components
vi.mock('@/components/Admin/EnvVarTable', () => ({ default: () => <div>Env Table</div> }));
vi.mock('@/components/Admin/EnvHistoryLog', () => ({ default: () => <div>Env History</div> }));

// Mock apiClient
vi.mock('../services/apiClient', () => ({
    default: {
        get: vi.fn((url) => {
            if (url.includes('/history')) return Promise.resolve([]);
            return Promise.resolve([]);
        }),
    }
}));

describe('EnvironmentSettings Component', () => {
    it('renders the system configuration header', async () => {
        render(<EnvironmentSettings />);
        expect(await screen.findByText(/System Configuration/i)).toBeTruthy();
    });
});
