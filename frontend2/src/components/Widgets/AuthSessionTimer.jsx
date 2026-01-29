import React, { useState, useEffect } from 'react';
import { Clock, ShieldAlert } from 'lucide-react';
import { authService } from '../../utils/authService';
import './Widgets.css';

const AuthSessionTimer = () => {
    const [timeLeft, setTimeLeft] = useState(null);

    useEffect(() => {
        const calculateTL = () => {
            const token = authService.getToken();
            if (!token) {
                setTimeLeft(0);
                return;
            }

            try {
                // Basic JWT decode
                const base64Url = token.split('.')[1];
                const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
                const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
                    return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
                }).join(''));

                const { exp } = JSON.parse(jsonPayload);
                const remaining = exp * 1000 - Date.now();
                setTimeLeft(Math.max(0, remaining));
            } catch (e) {
                setTimeLeft(null);
            }
        };

        calculateTL();
        const interval = setInterval(calculateTL, 1000);
        return () => clearInterval(interval);
    }, []);

    if (timeLeft === null) return null;

    const formatTime = (ms) => {
        const totalSec = Math.floor(ms / 1000);
        const min = Math.floor(totalSec / 60);
        const sec = totalSec % 60;
        return `${min}:${sec.toString().padStart(2, '0')}`;
    };

    const isWarn = timeLeft < 5 * 60 * 1000; // 5 min
    const isCrit = timeLeft < 1 * 60 * 1000; // 1 min

    return (
        <div className="widget auth-timer animate-fade-in">
            <div className="widget__header">
                <Clock size={16} className={`widget__icon ${isCrit ? 'animate-pulse' : ''}`} />
                <span className="widget__title">Session Security</span>
                {isWarn && <ShieldAlert size={14} className="text-amber" />}
            </div>

            <div className="auth-timer__content">
                <div className={`time-display ${isCrit ? 'critical' : isWarn ? 'warning' : ''}`}>
                    {formatTime(timeLeft)}
                </div>
                <div className="time-label">REMAINING TTL</div>
            </div>

            <div className="widget__footer">
                <span>Refreshed: 1s ago</span>
                <span className="secure-text">ENCRYPTED</span>
            </div>
        </div>
    );
};

export default AuthSessionTimer;
