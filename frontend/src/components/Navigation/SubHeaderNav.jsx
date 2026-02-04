
import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import './SubHeaderNav.css';
import {
    Terminal,
    Activity,
    Globe,
    Cpu,
    MessageSquare,
    Code,
    Zap,
    DollarSign,
    PieChart,
    Search,
    Layout
} from 'lucide-react';

const SubHeaderNav = () => {
    const navigate = useNavigate();
    const location = useLocation();

    const navItems = [
        { path: '/workspace/terminal', label: 'Terminal', icon: <Terminal size={14} /> },
        { path: '/workspace/mission-control', label: 'Mission Control', icon: <Activity size={14} /> },
        { path: '/analytics/options', label: 'Options', icon: <PieChart size={14} /> },
        { path: '/portfolio/backtest', label: 'Backtest', icon: <Zap size={14} /> },
        { path: '/analytics/political', label: 'Political Alpha', icon: <Globe size={14} /> },
        { path: '/analytics/strategy', label: 'Strategy', icon: <Cpu size={14} /> },
        { path: '/workspace/debate', label: 'Debate', icon: <MessageSquare size={14} /> },
        { path: '/workspace/autocoder', label: 'AutoCoder', icon: <Code size={14} /> },
        { path: '/scanner/global', label: 'Scanner', icon: <Search size={14} /> },
        { path: '/portfolio/brokerage', label: 'Brokerage', icon: <DollarSign size={14} /> },
        { path: '/workspace/vr', label: 'VR Cockpit', icon: <Layout size={14} /> },
    ];

    return (
        <nav className="sub-header-nav">
            <div className="nav-container">
                {navItems.map((item) => (
                    <button
                        key={item.path}
                        className={`nav-item ${location.pathname === item.path ? 'active' : ''}`}
                        onClick={() => navigate(item.path)}
                    >
                        {item.icon}
                        <span>{item.label}</span>
                    </button>
                ))}
            </div>
        </nav>
    );
};

export default SubHeaderNav;
