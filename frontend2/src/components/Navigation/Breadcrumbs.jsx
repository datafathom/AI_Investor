
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { ChevronRight, Home } from 'lucide-react';
import './Breadcrumbs.css';

const Breadcrumbs = () => {
    const location = useLocation();
    
    // Manual Route Map to match MenuBar.jsx structure (Single Source of Truth ideally, but mapping here for speed)
    const getBreadcrumbName = (path) => {
        const map = {
            // Core Workspaces
            'workspace': 'Core Workspaces',
            'terminal': 'Terminal Workspace',
            'mission-control': 'Mission Control',
            'autocoder': 'Auto-Coder Dashboard',
            'auto-coder': 'Auto-Coder Sandbox',
            'vr': 'VR Cockpit',
            
            // Analysis & Logic
            'analytics': 'Analysis & Logic',
            'political': 'Political Alpha',
            'strategy': 'Strategy Distillery',
            'debate': 'Debate Chamber',
            
            // Portfolio
            'portfolio': 'Portfolio Management',
            'brokerage': 'Virtual Brokerage',
            'attribution': 'Portfolio Attribution',
            'fixed-income': 'Fixed Income',
            'crypto': 'Crypto & Web3',
            'tax': 'Tax Optimization',
            'cash-flow': 'Cash Flow',
            
            // Other Top Levels
            'scanner': 'Global Scanner',
            'assets': 'Assets & Illiquid',
            'tenant': 'Family Office (Tenants)',
            
            // Trading
            'trading': 'Trading & Execution',
            'options': 'Options Strategy',
            'paper': 'Paper Trading',
            'algorithmic': 'Algorithmic Trading',
            'advanced-orders': 'Advanced Orders',

            // Planning
            'planning': 'Financial Planning',
            'retirement': 'Retirement Planning',
            'estate': 'Estate Planning',
            'budgeting': 'Budgeting',
            'billing': 'Bill Payment',
            'credit': 'Credit Monitoring',
            
            // Roles
            'guardian': 'Role: The Guardian',
            'compliance': 'Compliance & KYC',
            'audit': 'Regulatory Audit',
            'scenarios': 'Stress Scenarios',
            'margin': 'Margin Management',
            
            'strategist': 'Role: The Strategist',
            'impact': 'Philanthropy & Impact',
            'corporate': 'Corporate Actions',
            'currency': 'Currency & Cash',
            
            'architect': 'Role: The Architect',
            'system': 'System Health',
            'api': 'API Dashboard',
            
            'observer': 'Role: The Observer',
            'macro': 'Macro Observer',
            
            'zen': 'Zen Mode',
            'mobile': 'Mobile Dashboard'
        };
        return map[path] || path.charAt(0).toUpperCase() + path.slice(1).replace(/-/g, ' ');
    };

    const pathnames = location.pathname.split('/').filter((x) => x);

    // If we are at root/dashboard, don't show breadcrumbs or just Home
    if (pathnames.length === 0) return null;

    return (
        <nav className="breadcrumbs-container">
            <Link to="/" className="breadcrumb-item home-link">
                <Home size={16} />
                <span>Home</span>
            </Link>

            {pathnames.map((value, index) => {
                const last = index === pathnames.length - 1;
                const to = `/${pathnames.slice(0, index + 1).join('/')}`;
                const displayName = getBreadcrumbName(value);

                return (
                    <React.Fragment key={to}>
                        <ChevronRight size={14} className="breadcrumb-separator" />
                        {last ? (
                            <span className="breadcrumb-item active">{displayName}</span>
                        ) : (
                            <Link to={to} className="breadcrumb-item">
                                {displayName}
                            </Link>
                        )}
                    </React.Fragment>
                );
            })}
        </nav>
    );
};

export default Breadcrumbs;
