import React, { useState, useEffect } from 'react';
import { Terminal, ChevronRight } from 'lucide-react';
import { telemetryService } from '../../services/telemetryService';
import './Widgets.css';

const CliHistoryWizard = () => {
    const [history, setHistory] = useState(telemetryService.getCliHistory());

    useEffect(() => {
        const unsubscribe = telemetryService.subscribe((metrics) => {
            setHistory([...metrics.cliHistory]);
        });
        return () => unsubscribe();
    }, []);

    return (
        <div className="widget cli-wizard animate-fade-in">
            <div className="widget__header">
                <Terminal size={16} className="widget__icon" />
                <span className="widget__title">Live System Feed</span>
            </div>

            <div className="cli-wizard__feed">
                {history.length > 0 ? history.map((log, idx) => (
                    <div key={idx} className="cli-wizard__line">
                        <ChevronRight size={10} className="line-arrow" />
                        <span className="line-timestamp">[{new Date(log.timestamp).toLocaleTimeString()}]</span>
                        <span className={`line-msg ${log.level || 'info'}`}>{log.message}</span>
                    </div>
                )) : (
                    <div className="cli-wizard__empty">Awaiting system events...</div>
                )}
            </div>

            <div className="widget__footer">
                <span>BUFFER: {history.length}/50</span>
                <span className="blink">LIVE</span>
            </div>
        </div>
    );
};

export default CliHistoryWizard;
