import React, { useMemo } from 'react';
import { useLocation } from 'react-router-dom';
import { Activity, Shield, Zap, Terminal, Database, Cpu } from 'lucide-react';
import './SubPageBoilerplate.css';

/**
 * SubPageBoilerplate - A professional, high-fidelity placeholder for department sub-pages.
 * Automatically adapts its content based on the current path.
 */
const SubPageBoilerplate = ({ deptName = "Department", pageName = "Module" }) => {
    const location = useLocation();
    
    // Parse name from path if not provided
    const displayPageName = useMemo(() => {
        if (pageName && pageName !== "Module") return pageName;
        const parts = location.pathname.split('/');
        const lastPart = parts[parts.length - 1];
        return lastPart
            .split('-')
            .map(word => word.charAt(0).toUpperCase() + word.slice(1))
            .join(' ');
    }, [location.pathname, pageName]);

    const displayDeptName = useMemo(() => {
        if (deptName && deptName !== "Department") return deptName;
        const parts = location.pathname.split('/');
        return parts[parts.length - 2]?.charAt(0).toUpperCase() + parts[parts.length - 2]?.slice(1) || "System";
    }, [location.pathname, deptName]);

    // Generate some fake "Telemery" for the industrial look
    const stats = useMemo(() => [
        { label: "Neural Load", value: (Math.random() * 20 + 5).toFixed(2) + "%", icon: Cpu },
        { label: "Data Integrity", value: (99.99 - Math.random() * 0.5).toFixed(4) + "%", icon: Database },
        { label: "Response Latency", value: (Math.random() * 50 + 10).toFixed(0) + "ms", icon: Zap },
        { label: "Encrypted Node", value: "ACTIVE-0" + (Math.floor(Math.random() * 9) + 1), icon: Shield }
    ], []);

    return (
        <div className="boilerplate-container">
            <div className="boilerplate-content">
                <div className="status-badge">
                    <Activity size={12} className="pulse" />
                    <span>OPERATIONAL // {displayDeptName.toUpperCase()}</span>
                </div>
                
                <h1 className="boilerplate-title">
                    <span className="dept-prefix">{displayDeptName} /</span>
                    <span className="page-suffix">{displayPageName}</span>
                </h1>

                <div className="boilerplate-grid">
                    <div className="main-visual">
                        <div className="visual-grid-overlay"></div>
                        <div className="scanner-line"></div>
                        <div className="center-icon">
                            <Terminal size={64} strokeWidth={1} style={{ opacity: 0.2 }} />
                        </div>
                        <div className="data-readout top-left">NS_0x{Math.random().toString(16).slice(2, 6).toUpperCase()}</div>
                        <div className="data-readout top-right">LOG_SEQ: {Math.floor(Math.random() * 100000)}</div>
                        <div className="data-readout bottom-left">M_SYS: ATOMIC</div>
                        <div className="data-readout bottom-right">ZONE: DELTA_{Math.floor(Math.random() * 4)}</div>
                    </div>

                    <div className="stats-sidebar">
                        {stats.map((stat, idx) => (
                            <div key={idx} className="stat-card">
                                <div className="stat-icon">
                                    <stat.icon size={18} />
                                </div>
                                <div className="stat-info">
                                    <div className="stat-label">{stat.label}</div>
                                    <div className="stat-value">{stat.value}</div>
                                </div>
                            </div>
                        ))}
                        
                        <div className="placeholder-text-block">
                            <h3>Module Overview</h3>
                            <p>
                                Initializing {displayPageName} interface... 
                                Secure gateway established via {displayDeptName} mainframes.
                                Strategic analysis and real-time telemetry processing in progress.
                            </p>
                            <div className="progress-bar-container">
                                <div className="progress-label">SYNCHRONIZING MESH...</div>
                                <div className="progress-bar">
                                    <div className="progress-fill" style={{ width: '65%' }}></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div className="footer-telemetry">
                    <span>SYSTEM_READY</span>
                    <span>|</span>
                    <span>ENCRYPTION: AES-256</span>
                    <span>|</span>
                    <span>BUFFER: STABLE</span>
                </div>
            </div>
        </div>
    );
};

export default SubPageBoilerplate;
