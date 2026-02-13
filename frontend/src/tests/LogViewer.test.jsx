import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import LogViewer from '../pages/admin/LogViewer';
import apiClient from '../services/apiClient';

// Mock apiClient
vi.mock('../services/apiClient', () => ({
    default: {
        get: vi.fn(),
    }
}));

describe('LogViewer Component', () => {
    const mockFiles = ['system.log', 'error.log', 'backend_debug.log'];
    const mockLogs = ['Log line 1', 'Log line 2', 'Log line 3'];

    beforeEach(() => {
        vi.clearAllMocks();
        apiClient.get.mockImplementation((url) => {
            if (url === '/admin/logs/files') {
                return Promise.resolve(mockFiles);
            }
            if (url.includes('/admin/logs/tail')) {
                return Promise.resolve(mockLogs);
            }
            return Promise.resolve([]);
        });
    });

    it('renders the log viewer header', async () => {
        render(<LogViewer />);
        expect(screen.getByText(/SYSTEM_LOG_VIEWER/i)).toBeTruthy();
        await waitFor(() => {
            expect(screen.getByPlaceholderText(/SEARCH_LOGS/i)).toBeTruthy();
        });
    });

    it('fetches and displays log files in selector', async () => {
        render(<LogViewer />);
        await waitFor(() => {
            mockFiles.forEach(file => {
                expect(screen.getByText(file)).toBeTruthy();
            });
        });
    });

    it('displays loading state initially', () => {
        apiClient.get.mockReturnValue(new Promise(() => {})); // Never resolves
        render(<LogViewer />);
        expect(screen.getByText(/STREAMING_LOG_BUFFER/i)).toBeTruthy();
    });

    it('renders log lines after loading', async () => {
        render(<LogViewer />);
        await waitFor(() => {
            mockLogs.forEach(log => {
                expect(screen.getByText(log)).toBeTruthy();
            });
        });
    });

    it('handles log searching', async () => {
        const searchResults = { results: [{ content: 'Search result line' }] };
        
        apiClient.get.mockImplementation((url) => {
            if (url === '/admin/logs/files') return Promise.resolve(mockFiles);
            if (url.includes('/admin/logs/search')) return Promise.resolve(searchResults);
            if (url.includes('/admin/logs/tail')) return Promise.resolve(mockLogs);
            return Promise.resolve([]);
        });

        render(<LogViewer />);
        
        const searchInput = screen.getByPlaceholderText(/SEARCH_LOGS/i);
        fireEvent.change(searchInput, { target: { value: 'error' } });

        await waitFor(() => {
            expect(apiClient.get).toHaveBeenCalledWith('/admin/logs/search?query=error');
            expect(screen.getByText('Search result line')).toBeTruthy();
        });
    });
});
