import React from 'react';
import { render, screen } from '@testing-library/react';
import GraphBrowser from '../pages/admin/GraphBrowser';
import { vi } from 'vitest';

// Mock apiClient
vi.mock('../services/apiClient', () => ({
    default: {
        get: vi.fn(() => Promise.resolve([])),
    }
}));

describe('GraphBrowser Component', () => {
    it('renders the system graph integrity header', async () => {
        render(<GraphBrowser />);
        expect(await screen.findByText(/SYSTEM_GRAPH_INTEGRITY/i)).toBeTruthy();
    });
});
