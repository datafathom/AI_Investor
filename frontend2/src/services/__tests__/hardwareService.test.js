import { describe, it, expect, vi, beforeEach } from 'vitest';
import hardwareService from '../hardwareService';

describe('HardwareService', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        // Mock navigator.hid
        global.navigator.hid = {
            requestDevice: vi.fn(),
            getDevices: vi.fn()
        };
    });

    it('should identify as supported if hid is in navigator', () => {
        expect(hardwareService.isSupported).toBe(true);
    });

    it('should throw error if pairing fails', async () => {
        global.navigator.hid.requestDevice.mockRejectedValue(new Error('User cancelled'));
        
        await expect(hardwareService.pairDevice()).rejects.toThrow('User cancelled');
    });

    it('should return mock signature in development mode', async () => {
        // Mock process.env.NODE_ENV
        const originalEnv = process.env.NODE_ENV;
        process.env.NODE_ENV = 'development';
        
        const payload = { amount: 100, asset: 'BTC' };
        const signature = await hardwareService.signTransaction(payload);
        
        expect(signature).toContain('hw_sig_');
        
        process.env.NODE_ENV = originalEnv;
    });

    it('should throw error if signing without device in non-dev', async () => {
        const originalEnv = process.env.NODE_ENV;
        process.env.NODE_ENV = 'production';
        
        const payload = { amount: 100, asset: 'BTC' };
        await expect(hardwareService.signTransaction(payload)).rejects.toThrow('No hardware device paired');
        
        process.env.NODE_ENV = originalEnv;
    });

    it('should track status correctly', () => {
        const status = hardwareService.getStatus();
        expect(status.isSupported).toBe(true);
        expect(status.isConnected).toBe(false);
    });
});
