import { describe, it, expect, vi, beforeEach } from 'vitest';
import apiClient from './apiClient';
import axios from 'axios';
import { useStore } from '../store/store';

// Mock axios
vi.mock('axios', async () => {
    const actual = await vi.importActual('axios');
    return {
        default: {
            create: vi.fn(() => {
                const instance = vi.fn();
                instance.interceptors = {
                    request: { use: vi.fn(), eject: vi.fn() },
                    response: { use: vi.fn(), eject: vi.fn() }
                };
                instance.defaults = { headers: { common: {} } };
                return instance;
            }),
        }
    };
});

// Mock useStore
vi.mock('../store/store', () => ({
    useStore: {
        getState: vi.fn(() => ({
            setLoading: vi.fn()
        }))
    }
}));

describe('apiClient', () => {
    let mockRefresh;
    
    beforeEach(() => {
        vi.clearAllMocks();
        // Since apiClient is a singleton, we need to manually test the logic 
        // that would be passed to interceptors if we were able to access them easily.
        // For unit testing the INTERCEPTORS themselves, we'd ideally test the functions
        // passed to apiClient.interceptors.request.use and response.use.
    });

    it('should be defined', () => {
        expect(apiClient).toBeDefined();
    });

    // In a real scenario, we'd test the interceptor functions directly.
    // Since they are defined inside the module and not exported, 
    // we'll verify the structure and presence.
});
