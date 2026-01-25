/**
 * Mobile Store - Zustand State Management for Mobile Actions
 * Phase 65: Manages biometric kill switch, trade authorization, and haptic alerts.
 */
import { create } from 'zustand';

const useMobileStore = create((set, get) => ({
    // State
    killSwitchActive: false,
    biometricEnabled: true,
    pendingAuthorizations: [],
    alerts: [],
    hapticPatterns: { trade: true, alert: true, emergency: true },
    deviceLinked: false,
    error: null,
    
    // Actions
    setKillSwitchActive: (active) => set({ killSwitchActive: active }),
    setBiometricEnabled: (enabled) => set({ biometricEnabled: enabled }),
    setPendingAuthorizations: (auths) => set({ pendingAuthorizations: auths }),
    addPendingAuth: (auth) => set((s) => ({ pendingAuthorizations: [...s.pendingAuthorizations, auth] })),
    removePendingAuth: (id) => set((s) => ({ pendingAuthorizations: s.pendingAuthorizations.filter(a => a.id !== id) })),
    setAlerts: (alerts) => set({ alerts }),
    setHapticPatterns: (patterns) => set((s) => ({ hapticPatterns: { ...s.hapticPatterns, ...patterns } })),
    setDeviceLinked: (linked) => set({ deviceLinked: linked }),
    setError: (error) => set({ error }),
    
    // Async: Activate kill switch
    activateKillSwitch: async (biometricToken) => {
        const { setKillSwitchActive, setError } = get();
        try {
            const response = await fetch('/api/v1/mobile/kill-switch', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ biometric_token: biometricToken })
            });
            if (!response.ok) throw new Error('Kill switch activation failed');
            setKillSwitchActive(true);
        } catch (error) {
            console.error('Kill switch error:', error);
            setError(error.message);
        }
    },
    
    // Async: Authorize trade
    authorizeTrade: async (authId, approve) => {
        const { removePendingAuth, setError } = get();
        try {
            await fetch(`/api/v1/mobile/authorize/${authId}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ approve })
            });
            removePendingAuth(authId);
        } catch (error) {
            console.error('Trade auth error:', error);
            setError(error.message);
        }
    },
    
    reset: () => set({
        killSwitchActive: false, biometricEnabled: true, pendingAuthorizations: [],
        alerts: [], hapticPatterns: { trade: true, alert: true, emergency: true },
        deviceLinked: false, error: null
    })
}));

export default useMobileStore;
