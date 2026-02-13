import React from 'react';
import { render, screen } from '@testing-library/react';
import WorkspaceManager from '../pages/admin/WorkspaceManager';
import { vi } from 'vitest';

// Mock hook
vi.mock('../../hooks/useWidgetLayout', () => ({
    useWidgetLayout: () => ({
        saveWorkspace: vi.fn(),
        loadWorkspace: vi.fn(),
        activeWorkspace: null
    })
}));

// Mock apiClient
vi.mock('../services/apiClient', () => ({
    default: {
        get: vi.fn(() => Promise.resolve([])),
    }
}));

describe('WorkspaceManager Component', () => {
    it('renders the workspace orchestration header', async () => {
        render(<WorkspaceManager />);
        expect(await screen.findByText(/Workspace Orchestration/i)).toBeTruthy();
    });
});
