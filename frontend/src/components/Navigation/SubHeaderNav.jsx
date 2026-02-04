
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
    Layout,
    Bot,
    Wallet,
    ShieldCheck,
    Search
} from 'lucide-react';

const SubHeaderNav = () => {
    const navigate = useNavigate();
    const location = useLocation();

    const navItems = [
        { path: '/data-scientist/assistant', label: 'AI Colleague', icon: <Bot size={14} /> },
        { path: '/architect/admin', label: 'Admin', icon: <ShieldCheck size={14} /> },
        { path: '/strategist/net-worth', label: 'Net Worth', icon: <Wallet size={14} /> },
        { path: '/orchestrator/terminal', label: 'Terminal', icon: <Terminal size={14} /> },
        { path: '/orchestrator/mission-control', label: 'Mission Control', icon: <Activity size={14} /> },
        { path: '/trader/options-analytics', label: 'Options', icon: <PieChart size={14} /> },
        { path: '/strategist/backtest', label: 'Backtest', icon: <Zap size={14} /> },
        { path: '/analyst/strategy', label: 'Strategy', icon: <Cpu size={14} /> },
        { path: '/data-scientist/debate', label: 'Debate', icon: <MessageSquare size={14} /> },
        { path: '/data-scientist/autocoder', label: 'AutoCoder', icon: <Code size={14} /> },
        { path: '/trader/scanner', label: 'Scanner', icon: <Search size={14} /> },
        { path: '/strategist/brokerage', label: 'Brokerage', icon: <DollarSign size={14} /> },
        { path: '/analyst/political', label: 'Political Alpha', icon: <Globe size={14} /> },
        { path: '/data-scientist/vr', label: 'VR Cockpit', icon: <Layout size={14} /> },
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
