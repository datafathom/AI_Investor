import React, { useEffect, useRef } from 'react';
import './TerminalWidget.css';

const TerminalWidget = ({ logs = [], onClearHistory }) => {
    const outputRef = useRef(null);

    useEffect(() => {
        if (outputRef.current) {
            outputRef.current.scrollTop = outputRef.current.scrollHeight;
        }
    }, [logs]);

    return (
        <div className="terminal-widget-container">
            <div className="terminal-header">
                <div className="terminal-header-left">
                    <span className="terminal-title">SYSTEM EVENT LOG</span>
                    <span className="terminal-status-dot connected"></span>
                    <span className="terminal-status">LIVE</span>
                </div>
                <div className="terminal-header-right">
                    <button 
                        className="terminal-action-btn" 
                        onClick={onClearHistory}
                        title="Clear History"
                    >
                        CLEAR
                    </button>
                    <span className="terminal-version">v2.0.1</span>
                </div>
            </div>
            <div ref={outputRef} className="terminal-output custom-scrollbar">
                {logs.length === 0 ? (
                    <div className="terminal-empty">No system events logged.</div>
                ) : (
                    logs.map((log, i) => (
                        <div key={i} className={`terminal-line ${log.type || 'info'}`}>
                            <span className="timestamp">[{new Date(log.timestamp || Date.now()).toLocaleTimeString([], { hour12: false })}]</span>
                            <span className="level">[{ (log.type || 'info').toUpperCase() }]</span>
                            <span className="message">{log.message}</span>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default TerminalWidget;
