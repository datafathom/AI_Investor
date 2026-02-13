import React from 'react';
import { render, screen } from '@testing-library/react';
import AlertConfigPage from '../pages/admin/AlertConfigPage';
import { vi } from 'vitest';

// Mock apiClient
vi.mock('../services/apiClient', () => ({
    default: {
        get: vi.fn(() => Promise.resolve([])),
    }
}));

describe('AlertConfigPage Component', () => {
    it('renders the alert criteria management header', async () => {
        render(<AlertConfigPage />);
        expect(await screen.findByText(/ALERT_CRITERIA_MANAGEMENT/i)).toBeTruthy();
    });
});
