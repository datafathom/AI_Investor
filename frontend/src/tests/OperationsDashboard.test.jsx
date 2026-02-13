import React from 'react';
import { render, screen } from '@testing-library/react';
import OperationsDashboard from '../pages/admin/OperationsDashboard';
import { vi } from 'vitest';

// Mock sub-components
vi.mock('@/components/Admin/JobScheduleTable', () => ({ default: () => <div>Job Table</div> }));
vi.mock('@/components/Admin/JobRunHistory', () => ({ default: () => <div>Job History</div> }));
vi.mock('@/components/Widgets/DataQualityWidget', () => ({ default: () => <div>Quality Widget</div> }));

// Mock apiClient
vi.mock('../services/apiClient', () => ({
    default: {
        get: vi.fn((url) => {
            if (url.includes('/jobs')) return Promise.resolve([]);
            return Promise.resolve([]);
        }),
    }
}));

describe('OperationsDashboard Component', () => {
    it('renders the infrastructure operations header', async () => {
        render(<OperationsDashboard />);
        expect(await screen.findByText(/Infrastructure Operations/i)).toBeTruthy();
    });
});
