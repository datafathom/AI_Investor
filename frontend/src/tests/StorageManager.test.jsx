import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import StorageManager from '../pages/admin/StorageManager';
import apiClient from '../services/apiClient';
import { vi } from 'vitest';

// Mock apiClient
vi.mock('../services/apiClient', () => ({
    default: {
        get: vi.fn(),
        post: vi.fn(),
    }
}));

describe('StorageManager Component', () => {
    const mockPools = [
        {
            name: 'rpool',
            health: 'HEALTHY',
            status: 'ONLINE',
            capacity: '45%',
            scan: 'scrub repaired 0B in 00:03:12',
            vdevs: [{ name: 'sda1', status: 'ONLINE' }]
        }
    ];
    const mockSyncStatus = {
        last_sync: new Date().toISOString(),
        status: 'IDLE',
        next_scheduled: new Date().toISOString(),
        progress: 100
    };

    beforeEach(() => {
        vi.clearAllMocks();
        apiClient.get.mockImplementation((url) => {
            if (url === '/admin/storage/pools') return Promise.resolve(mockPools);
            if (url === '/admin/storage/sync-status') return Promise.resolve(mockSyncStatus);
            return Promise.resolve({});
        });
    });

    it('renders the storage manager header', async () => {
        render(<StorageManager />);
        await waitFor(() => {
            expect(screen.getByText(/PRIVATE_CLOUD_STORAGE/i)).toBeTruthy();
            expect(screen.getByText(/TRIGGER_OFFSITE_SYNC/i)).toBeTruthy();
        });
    });

    it('displays loading state initially', () => {
        apiClient.get.mockReturnValue(new Promise(() => {})); // Never resolves
        render(<StorageManager />);
        expect(screen.getByText(/QUERYING_ZFS_SUBSYSTEM/i)).toBeTruthy();
    });

    it('renders pools and sync status after loading', async () => {
        render(<StorageManager />);
        await waitFor(() => {
            expect(screen.getByText('rpool')).toBeTruthy();
            expect(screen.getByText('HEALTHY')).toBeTruthy();
            expect(screen.getByText('IDLE')).toBeTruthy();
        });
    });

    it('handles sync triggering', async () => {
        apiClient.post.mockResolvedValueOnce({});
        render(<StorageManager />);
        
        await waitFor(() => {
            const syncButton = screen.getByText(/TRIGGER_OFFSITE_SYNC/i);
            fireEvent.click(syncButton);
        });

        await waitFor(() => {
            expect(apiClient.post).toHaveBeenCalledWith('/admin/storage/sync/trigger');
        });
    });
});
