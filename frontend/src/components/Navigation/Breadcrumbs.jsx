
import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { ChevronRight, Home } from 'lucide-react';
import './Breadcrumbs.css';

const Breadcrumbs = () => {
    const location = useLocation();
    
    const getBreadcrumbName = (segment) => {
        const map = {
            // Role names (Top segments)
            'orchestrator': 'Orchestrator',
            'architect': 'Architect',
            'analyst': 'Analyst',
            'trader': 'Trader',
            'strategist': 'Strategist',
            'marketing': 'Hunter',
            'hunter': 'Hunter',
            'legal': 'Legal',
            'guardian': 'Guardian',
            'pioneer': 'Data Scientist',

            // Orchestrator features
            'terminal': 'Terminal Workspace',
            'mission-control': 'Mission Control',
            'graph': 'Master Graph',
            'chat': 'Global Chat',
            'zen': 'Zen Mode',

            // Architect features
            'admin': 'Admin Center',
            'health': 'System Health',
            'api': 'API Dashboard',
            'integrations': 'Integrations',
            'dev-platform': 'Developer Platform',

            // Analyst features
            'predictions': 'AI Predictions',
            'training': 'ML Training',
            'political': 'Political Alpha',
            'strategy': 'Strategy Distillery',
            'macro': 'Macro Observer',
            'assistant': 'AI Colleague',

            // Trader features
            'scanner': 'Global Scanner',
            'options': 'Options Strategy',
            'options-analytics': 'Options Analytics',
            'advanced-orders': 'Advanced Orders',
            'algorithmic': 'Algo Trading',
            'paper': 'Paper Trading',
            'charting': 'Advanced Charting',

            // Strategist features
            'net-worth': 'Portfolio Net Worth',
            'analytics': 'Advanced Analytics',
            'optimization': 'Portfolio Optimization',
            'attribution': 'Portfolio Attribution',
            'backtest': 'Backtest Explorer',
            'brokerage': 'Virtual Brokerage',
            'crypto': 'Crypto & Web3',
            'fixed-income': 'Fixed Income',
            'assets': 'Assets & Illiquids',
            'estate': 'Estate Planning',
            'retirement': 'Retirement Planning',
            'budgeting': 'Budgeting',
            'financial': 'Financial Planning',

            // Marketing features
            'news': 'News & Sentiment',
            'social': 'Social Trading',
            'forums': 'Community Forums',
            'education': 'Education Platform',
            'marketplace': 'Marketplace',
            'reports': 'Research Reports',
            'alerts': 'Watchlists & Alerts',

            // Legal features
            'compliance': 'Compliance & KYC',
            'audit': 'Regulatory Audit',
            'scenarios': 'Stress Scenarios',
            'margin': 'Margin Management',
            'terms': 'Terms of Service',
            'privacy': 'Privacy Policy',

            // Guardian features
            'risk': 'Risk Management',
            'credit': 'Credit Monitoring',
            'institutional': 'Institutional Tools',
            'enterprise': 'Enterprise Features',
            'payments': 'Bill Payments',
            'cash-flow': 'Cash Flow Tracking',
            'tenants': 'Family Office',
            'mobile': 'Mobile Companion',

            // Data Scientist features
            'autocoder': 'Auto-Coder',
            'sandbox': 'Sandbox',
            'vr': 'VR Cockpit',
            'debate': 'Debate Chamber',

            // Account
            'settings': 'Settings',
            'profile': 'Profile',
            'keyboard': 'Shortcuts'
        };
        
        return map[segment] || segment.charAt(0).toUpperCase() + segment.slice(1).replace(/-/g, ' ');
    };

    const pathnames = location.pathname.split('/').filter((x) => x);

    // If we are at root/dashboard, don't show breadcrumbs
    if (pathnames.length === 0) return null;

    const breadcrumbs = [];
    
    // Always start with Home
    breadcrumbs.push({ label: 'Home', path: '/', isLink: true, isHome: true });

    // Handle legacy path mapping for breadcrumbs if needed, 
    // but with the new role-based structure, the URL itself is the hierarchy.
    
    pathnames.forEach((segment, index) => {
        const path = `/${pathnames.slice(0, index + 1).join('/')}`;
        
        // Avoid adding the same label twice (e.g. if a segment maps to the same name as current)
        const label = getBreadcrumbName(segment);
        
        breadcrumbs.push({ 
            label: label, 
            path: path, 
            isLink: index < pathnames.length - 1 
        });
    });

    return (
        <nav className="breadcrumbs-container">
            {breadcrumbs.map((crumb, index) => {
                const isLast = index === breadcrumbs.length - 1;
                
                return (
                    <React.Fragment key={crumb.path + index}>
                        {index > 0 && <ChevronRight size={14} className="breadcrumb-separator" />}
                        {crumb.isHome ? (
                            <Link to="/" className="breadcrumb-item home-link">
                                <Home size={16} />
                                <span>Home</span>
                            </Link>
                        ) : isLast ? (
                            <span className="breadcrumb-item active">{crumb.label}</span>
                        ) : (
                            <Link to={crumb.path} className="breadcrumb-item">
                                {crumb.label}
                            </Link>
                        )}
                    </React.Fragment>
                );
            })}
        </nav>
    );
};

export default Breadcrumbs;
