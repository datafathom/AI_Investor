import { useState, useEffect, useCallback } from 'react';
import { useToast } from '../context/ToastContext';

/**
 * useNotifications Hook
 * 
 * Manages OS-native desktop notifications and in-app alerts.
 * Supports sound profiles for industrial feedback.
 */
export const useNotifications = () => {
    const [permission, setPermission] = useState(typeof Notification !== 'undefined' && Notification.permission ? Notification.permission : 'denied');
    const { showToast } = useToast();

    useEffect(() => {
        console.log("[DEBUG] useNotifications: Initializing...");
        if (typeof Notification !== 'undefined' && Notification.permission === 'default') {
            Notification.requestPermission()
                .then(setPermission)
                .catch(e => console.warn('[DEBUG] Notification permission denied/blocked:', e));
        }
    }, []);

    const playSound = useCallback((type) => {
        if (typeof Audio === 'undefined') {
            console.log("[DEBUG] useNotifications: Audio not supported in this environment");
            return;
        }
        
        const sounds = {
            fill: 'https://assets.mixkit.co/active_storage/sfx/2358/2358-preview.mp3',
            alert: 'https://assets.mixkit.co/active_storage/sfx/2190/2190-preview.mp3',
            error: 'https://assets.mixkit.co/active_storage/sfx/2194/2194-preview.mp3',
        };

        try {
            const audio = new Audio(sounds[type] || sounds.alert);
            audio.volume = 0.4;
            audio.play().catch(e => console.log('[DEBUG] Audio playback blocked or failed:', e));
        } catch (e) {
            console.warn('[DEBUG] Failed to create Audio object:', e);
        }
    }, []);

    const notify = useCallback(({ title, body, icon, type = 'info', duration = null }) => {
        // Log only once per trigger
        console.log(`[DEBUG] useNotifications: Notify triggered - ${title}`);
        
        if (type === 'success' || type === 'info') playSound('fill');
        else if (type === 'error' || type === 'critical') playSound('error');
        else playSound('alert');

        // Check permission from state but don't let it re-trigger the effect that sets it
        if (permission === 'granted' && typeof Notification !== 'undefined') {
            try {
                new Notification(title, { body, icon: icon || '/favicon.ico' });
            } catch (e) {
                console.warn('[DEBUG] OS Notification construction failed:', e);
            }
        }

        if (showToast) {
            showToast(body || title, type, duration);
        }

        return { title, body, type };
    }, [permission, playSound, showToast]);

    return { notify, permission, playSound };
};

export default useNotifications;
