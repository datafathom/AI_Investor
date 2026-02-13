import React from 'react';
import { render, screen } from '@testing-library/react';
import ServiceHealthGrid from '../pages/admin/ServiceHealthGrid';
import { vi } from 'vitest';

// Mock apiClient
vi.mock('../services/apiClient', () => ({
    default: {
        get: vi.fn(() => Promise.resolve([])),
    }
}));

describe('ServiceHealthGrid Component', () => {
    it('renders the system health grid header', async () => {
        render(<ServiceHealthGrid />);
        expect(await screen.findByText(/SYSTEM_HEALTH_GRID/i)).toBeTruthy();
    });
});
