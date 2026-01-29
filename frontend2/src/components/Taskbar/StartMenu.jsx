import React, { useState } from 'react';
import { Search, Terminal, Activity, TrendingUp, Shield, Grid, Settings, Database, Brain } from 'lucide-react';
import useTaskbarStore from '../../stores/taskbarStore';
import { useNavigate } from 'react-router-dom';
import './StartMenu.css';

const APP_REGISTRY = [
    { id: 'mission-control', name: 'Mission Control', route: '/', icon: Activity, category: 'Core' },
    { id: 'strategy', name: 'Strategy Distillery', route: '/analytics/strategy', icon: Brain, category: 'Strategy' },
    { id: 'scanner', name: 'Market Scanner', route: '/scanner', icon: Grid, category: 'Strategy' },
    { id: 'backtest', name: 'Backtest Engine', route: '/backtest', icon: TrendingUp, category: 'Strategy' },
    { id: 'political', name: 'Political Alpha', route: '/political', icon: Shield, category: 'Data' },
    { id: 'terminal', name: 'System Terminal', route: '/terminal', icon: Terminal, category: 'System' },
    { id: 'settings', name: 'Settings', route: '/options', icon: Settings, category: 'System' },
    { id: 'debate', name: 'Agent Debate', route: '/debate', icon: Database, category: 'Core' }
];

const StartMenu = () => {
    const { isStartMenuOpen, closeStartMenu } = useTaskbarStore();
    const navigate = useNavigate();
    const [searchTerm, setSearchTerm] = useState('');

    if (!isStartMenuOpen) return null;

    const filteredApps = APP_REGISTRY.filter(app => 
        app.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const categories = [...new Set(filteredApps.map(app => app.category))];

    const handleAppClick = (route) => {
        navigate(route);
        closeStartMenu();
    };

    return (
        <div className="start-menu-container">
            <div className="start-search-bar">
                <Search size={18} className="text-slate-400" />
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
                                    <div className="app-icon-wrapper">
                                        <app.icon size={20} />
                                    </div>
                                    <span>{app.name}</span>
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
                <button className="power-btn">
                    ⏻
                </button>
            </div>
        </div>
    );
};

export default StartMenu;
