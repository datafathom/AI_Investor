import React, { useState, useMemo } from 'react';
import { 
    Search, Terminal, Activity, TrendingUp, Shield, Grid, Settings, 
    Database, Brain, Cpu, Target, Crosshair, Home, ShieldCheck, 
    Scale, Users, Briefcase, Clock, Zap, Landmark, Layout, Atom
} from 'lucide-react';
import useTaskbarStore from '../../stores/taskbarStore';
import { useNavigate } from 'react-router-dom';
import { DEPT_REGISTRY } from '../../config/departmentRegistry';
import { getIcon } from '../../config/iconRegistry';
import './StartMenu.css';

// Remove local ICON_MAP, now handled by iconRegistry.js

const STATIC_APPS = [
    { id: 'mission-control', name: 'Mission Control', route: '/special/mission-control', icon: Activity, category: 'Core' },
    { id: 'brokerage', name: 'Brokerage Account', route: '/strategist/brokerage', icon: Landmark, category: 'Strategist' },
    { id: 'strategy', name: 'Strategy Distillery', route: '/special/strategy', icon: Brain, category: 'Strategy' },
    { id: 'scanner', name: 'Market Scanner', route: '/trader/scanner', icon: Grid, category: 'Strategy' },
    { id: 'backtest', name: 'Backtest Engine', route: '/strategist/backtest', icon: TrendingUp, category: 'Strategy' },
    { id: 'political', name: 'Political Alpha', route: '/special/political', icon: Shield, category: 'Data' },
    { id: 'terminal', name: 'System Terminal', route: '/special/terminal', icon: Terminal, category: 'System' },
    { id: 'settings', name: 'Settings', route: '/account/settings', icon: Settings, category: 'System' },
    { id: 'debate', name: 'Agent Debate', route: '/special/debate', icon: Database, category: 'Core' },
    { id: 'scrum', name: 'Scrum of Scrums', route: '/special/scrum', icon: Layout, category: 'AI Teams', aliases: ['scrum', 'team meeting', 'sos', 'department overview'] }
];

const StartMenu = () => {
    const { isStartMenuOpen, closeStartMenu } = useTaskbarStore();
    const navigate = useNavigate();
    const [searchTerm, setSearchTerm] = useState('');
    const menuRef = React.useRef(null);

    const allApps = useMemo(() => {
        const apps = [];
        
        // Convert DEPT_REGISTRY to app format and include sub-modules
        Object.values(DEPT_REGISTRY).forEach(dept => {
            // Main Department App
            const mainDeptName = dept.name.replace(/^The\s+/i, '');
            apps.push({
                id: `dept-${dept.id}`,
                name: mainDeptName,
                route: dept.route,
                icon: getIcon(dept.icon),
                color: dept.color,
                category: 'AI Teams',
                type: 'department'
            });

            // Flatten Sub-Modules
            if (dept.subModules) {
                dept.subModules.forEach((mod, idx) => {
                    apps.push({
                        id: `mod-${dept.id}-${idx}`,
                        name: mod.label,
                        route: mod.path,
                        icon: getIcon(dept.icon),
                        color: dept.color,
                        category: 'AI Teams',
                        type: 'module',
                        deptName: mainDeptName
                    });
                });
            }
        });

        return [...apps, ...STATIC_APPS];
    }, []);

    const filteredApps = useMemo(() => {
        const term = searchTerm.toLowerCase().trim();
        
        if (!term) {
            // Only show main departments and static apps when not searching
            return allApps.filter(app => app.type !== 'module');
        }
        
        return allApps
            .filter(app => {
                const nameMatch = app.name.toLowerCase().includes(term);
                const aliasMatch = app.aliases?.some(alias => alias.toLowerCase().includes(term));
                return nameMatch || aliasMatch;
            })
            .sort((a, b) => {
                // Prioritize modules over departments in search results
                if (a.type === 'module' && b.type !== 'module') return -1;
                if (a.type !== 'module' && b.type === 'module') return 1;
                return 0;
            });
    }, [allApps, searchTerm]);

    // Get unique categories and define order
    const categories = useMemo(() => {
        const cats = [...new Set(filteredApps.map(app => app.category))];
        const order = ['AI Teams', 'Strategist', 'Core', 'Strategy', 'Data', 'System'];
        
        return order.filter(c => cats.includes(c));
    }, [filteredApps]);

    // Close on outside click
    React.useEffect(() => {
        const handleClickOutside = (event) => {
            // Check if click is on the start button itself
            const isStartButton = event.target.closest('.taskbar-start-button');
            
            if (menuRef.current && !menuRef.current.contains(event.target) && !isStartButton) {
                closeStartMenu();
            }
        };

        if (isStartMenuOpen) {
            document.addEventListener('mousedown', handleClickOutside);
        }
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, [isStartMenuOpen, closeStartMenu]);

    if (!isStartMenuOpen) return null;

    const handleAppClick = (route) => {
        navigate(route);
        closeStartMenu();
    };

    return (
        <div className="start-menu-container" ref={menuRef}>
            <div className="start-search-bar">
                <Search size={16} className="text-slate-400" />
                <input 
                    type="text" 
                    placeholder="Search AI Investor..." 
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    autoFocus
                />
            </div>

            <div className="start-app-grid">
                {categories.map(category => (
                    <div key={category} className="app-category">
                        <h4>{category}</h4>
                        <div className="category-apps">
                            {filteredApps.filter(a => a.category === category).map(app => (
                                <div 
                                    key={app.id} 
                                    className="app-item"
                                    onClick={() => handleAppClick(app.route)}
                                >
                                    <div 
                                        className="app-icon-wrapper" 
                                        style={app.category === 'AI Teams' ? { background: app.color, boxShadow: `0 4px 10px ${app.color}44` } : {}}
                                    >
                                        <app.icon size={54} />
                                    </div>
                                    <span>{app.name}</span>
                                    {app.type === 'module' && (
                                        <span className="app-dept-hint">{app.deptName}</span>
                                    )}
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
                
                {filteredApps.length === 0 && (
                    <div className="no-results">No apps found.</div>
                )}
            </div>

            <div className="start-footer">
                <div className="user-profile">
                    <div className="avatar">AI</div>
                    <div className="user-info">
                        <span className="name">Admin User</span>
                        <span className="role">System Architect</span>
                    </div>
                </div>
                <button className="power-btn" onClick={closeStartMenu}>
                    <Activity size={16} />
                </button>
            </div>
        </div>
    );
};

export default StartMenu;
