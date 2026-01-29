import React, { useEffect } from 'react';
import useSystemHealthStore from '../../stores/systemHealthStore';
import { Activity, Cpu } from 'lucide-react';

const SystemHealthMeters = () => {
    const { kafkaHealth, postgresHealth, refreshHealth } = useSystemHealthStore();

    useEffect(() => {
        // Initial refresh
        refreshHealth();
        // Poll health every 15 seconds (slightly slower to save cycles)
        const healthTimer = setInterval(refreshHealth, 15000);
        return () => clearInterval(healthTimer);
    }, [refreshHealth]);

    return (
        <div className="system-meters">
            <div className="meter-item" title="Kafka Throughput">
                <Activity size={14} className="text-cyan-400" />
                <span className="text-xs text-slate-400">{kafkaHealth.messagesPerSecond?.toLocaleString() || 0}/s</span>
            </div>
            <div className="meter-item" title="DB Connections">
                <Cpu size={14} className="text-blue-400" />
                <span className="text-xs text-slate-400">{postgresHealth.connections || 0} conn</span>
            </div>
        </div>
    );
};

export default React.memo(SystemHealthMeters);
