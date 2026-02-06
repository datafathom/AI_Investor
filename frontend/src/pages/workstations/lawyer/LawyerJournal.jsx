import React from 'react';
import '../Workstation.css';

const LawyerJournal = () => {
    return (
        <div className="workstation-container">
            <header className="workstation-header">
                <div className="status-dot pulse"></div>
                <h1>Trade Journaling <span className="text-slate-500">//</span> WORKSTATION</h1>
                <div className="flex-1"></div>
                <div className="security-badge">SECURE_CHANNEL_v1.2</div>
            </header>

            <div className="workstation-grid">
                <div className="workstation-main bg-slate-900/50 border border-slate-800 rounded-lg p-6">
                    <h2 className="text-cyan-400 font-mono text-xs uppercase tracking-widest mb-4">Functional Module: Trade Journaling</h2>
                    <p className="text-slate-400 font-mono text-sm leading-relaxed mb-6">
                        Mandatory tagging for mental state and reasoning.
                    </p>
                    
                    <div className="terminal-box bg-black/80 rounded border border-slate-700 p-4 font-mono text-[10px] text-cyan-500/80">
                        <div className="mb-1">&gt; INITIALIZING LawyerJournal...</div>
                        <div className="mb-1">&gt; SYNCING NEURAL MESH...</div>
                        <div className="mb-1">&gt; ESTABLISHING HANDSHAKE WITH AGENTIC LAYER...</div>
                        <div className="text-green-500">&gt; READY.</div>
                    </div>
                </div>

                <div className="workstation-sidebar flex flex-col gap-4">
                    <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
                        <h3 className="text-slate-500 font-mono text-[10px] uppercase mb-2">Metrics</h3>
                        <div className="metric-row border-b border-slate-800/50 py-2">
                            <span className="text-slate-400 text-xs">Latency:</span>
                            <span className="text-cyan-400 text-xs float-right">12ms</span>
                        </div>
                        <div className="metric-row py-2">
                            <span className="text-slate-400 text-xs">Uptime:</span>
                            <span className="text-cyan-400 text-xs float-right">99.9%</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default LawyerJournal;
