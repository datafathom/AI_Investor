import { useState, useEffect, useCallback } from 'react';
import { useToast } from '../context/ToastContext';

/**
 * useNotifications Hook
 * 
 * Manages OS-native desktop notifications and in-app alerts.
 * Supports sound profiles for industrial feedback.
 */
export const useNotifications = () => {
    const [permission, setPermission] = useState(Notification.permission);
    const { showToast } = useToast();

    useEffect(() => {
        if (Notification.permission === 'default') {
            Notification.requestPermission().then(setPermission);
        }
    }, []);

    /**
     * Play a feedback sound
     * @param {string} type - 'fill', 'alert', 'error'
     */
    const playSound = useCallback((type) => {
        // Sounds would ideally be in /public/sounds/
        const sounds = {
            fill: 'https://assets.mixkit.co/active_storage/sfx/2358/2358-preview.mp3', // Industrial ping
            alert: 'https://assets.mixkit.co/active_storage/sfx/2190/2190-preview.mp3', // Alert chime
            error: 'https://assets.mixkit.co/active_storage/sfx/2194/2194-preview.mp3', // Error buzzer
        };

        const audio = new Audio(sounds[type] || sounds.alert);
        audio.volume = 0.4;
        audio.play().catch(e => console.warn('Audio playback blocked:', e));
    }, []);

    /**
     * Send a notification
     */
    const notify = useCallback(({ title, body, icon, type = 'info', duration = null }) => {
        // Play contextual sound
        if (type === 'success' || type === 'info') playSound('fill');
        else if (type === 'error' || type === 'critical') playSound('error');
        else playSound('alert');

        // OS Notification
        if (permission === 'granted') {
            new Notification(title, {
                body,
                icon: icon || '/favicon.ico',
            });
        }

        // In-app Toast Integration
        showToast(body || title, type, duration);

        return { title, body, type };
    }, [permission, playSound, showToast]);

    return { notify, permission, playSound };
};

export default useNotifications;
