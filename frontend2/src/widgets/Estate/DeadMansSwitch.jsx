import React, { useEffect } from 'react';
import { Shield, Clock, Users, AlertTriangle, Lock, Loader2 } from 'lucide-react';
import useEstateStore from '../../stores/estateStore';
import './DeadMansSwitch.css';

/**
 * Dead Man's Switch Widget (Phase 15/58)
 */
const DeadMansSwitch = () => {
    const { 
        heartbeatStatus, 
        isHeartbeatEnabled, 
        isLoading, 
        confirmAlive, 
        fetchEstateData 
    } = useEstateStore();

    useEffect(() => {
        fetchEstateData();
    }, [fetchEstateData]);

    const handleCheckIn = async () => {
        await confirmAlive();
    };

    const formatDate = (isoStr) => {
        if (!isoStr) return 'Never';
        return new Date(isoStr).toLocaleString();
    };

    if (isLoading && !heartbeatStatus.lastCheck) {
        return (
            <div className="dead-mans-switch loading">
                <Loader2 className="animate-spin" size={24} />
                <span>Synchronizing Protocol...</span>
            </div>
        );
    }

    return (
        <div className="dead-mans-switch">
            <div className="widget-header">
                <Shield size={16} />
                <h3>Estate Protocol</h3>
                <div className={`status-badge ${heartbeatStatus.isAlive ? 'armed' : 'expired'}`}>
                    {heartbeatStatus.isAlive ? 'ARMED' : 'EXPIRED'}
                </div>
            </div>

            <div className="check-in-section">
                <div className="check-in-info">
                    <Clock size={14} />
                    <div>
                        <span className="label">Last Heartbeat</span>
                        <span className="value">{formatDate(heartbeatStatus.lastCheck)}</span>
                    </div>
                </div>
                <button 
                    className="check-in-btn" 
                    onClick={handleCheckIn}
                    disabled={isLoading}
                >
                    {isLoading ? <Loader2 className="animate-spin" size={14} /> : <Lock size={14} />}
                    Confirm Alive
                </button>
            </div>

            <div className="trigger-countdown">
                <div className="countdown-ring">
                    <span className="days">{heartbeatStatus.daysUntilTrigger}</span>
                    <span className="unit">days</span>
                </div>
                <div className="trigger-meta">
                    <span className="label">Next Trigger Date</span>
                    <span className="value">{new Date(heartbeatStatus.triggerDate).toLocaleDateString()}</span>
                </div>
            </div>

            <div className="warning-note">
                <AlertTriangle size={12} />
                <span>Protocol will execute automatically if countdown hits 0</span>
            </div>
        </div>
    );
};

export default DeadMansSwitch;
