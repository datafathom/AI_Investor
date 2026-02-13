import React from 'react';
import { render, screen } from '@testing-library/react';
import MiddlewarePipeline from '../pages/admin/MiddlewarePipeline';
import { vi } from 'vitest';

// Mock apiClient
vi.mock('../services/apiClient', () => ({
    default: {
        get: vi.fn(() => Promise.resolve([])),
    }
}));

describe('MiddlewarePipeline Component', () => {
    it('renders the middleware execution flow header', async () => {
        render(<MiddlewarePipeline />);
        expect(await screen.findByText(/MIDDLEWARE_EXECUTION_FLOW/i)).toBeTruthy();
    });
});
