/**
 * ==============================================================================
 * FILE: frontend2/src/stores/hardwareStore.js
 * ROLE: Hardware Wallet State Management
 * PURPOSE: Orchestrates signature requests between apiClient and the 
 *          HardwareSigModal UI.
 * ==============================================================================
 */

import { create } from 'zustand';
import hardwareService from '../services/hardwareService';

export const useHardwareStore = create((set, get) => ({
    // State
    isWaitingForSignature: false,
    currentPayload: null,
    error: null,
    signature: null,
    status: 'idle', // 'idle', 'requesting', 'signing', 'completed', 'failed'

    // Internal promise resolvers
    _resolve: null,
    _reject: null,

    /**
     * Entry point for requesting a hardware signature.
     * Returns a promise that resolves with the signature or rejects on cancel/error.
     */
    requestSignature: async (payload) => {
        set({ 
            isWaitingForSignature: true, 
            currentPayload: payload, 
            error: null, 
            status: 'requesting',
            signature: null 
        });

        return new Promise((resolve, reject) => {
            set({ _resolve: resolve, _reject: reject });
        });
    },

    /**
     * Called by the UI (HardwareSigModal) to initiate the physical signing.
     */
    executeSign: async () => {
        const { currentPayload, _resolve, _reject } = get();
        set({ status: 'signing' });

        try {
            const sig = await hardwareService.signTransaction(currentPayload);
            set({ status: 'completed', signature: sig, isWaitingForSignature: false });
            if (_resolve) _resolve(sig);
        } catch (err) {
            set({ status: 'failed', error: err.message });
            // We don't reject immediately to allow user to retry
        }
    },

    /**
     * Canceled by user in the UI.
     */
    cancelSignature: () => {
        const { _reject } = get();
        set({ 
            isWaitingForSignature: false, 
            currentPayload: null, 
            status: 'idle',
            _resolve: null,
            _reject: null
        });
        if (_reject) _reject(new Error('Signature request canceled by user'));
    },

    reset: () => set({
        isWaitingForSignature: false,
        currentPayload: null,
        error: null,
        status: 'idle',
        signature: null
    })
}));

export default useHardwareStore;
