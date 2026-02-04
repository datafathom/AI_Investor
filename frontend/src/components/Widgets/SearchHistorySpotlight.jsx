import React, { useState, useEffect } from 'react';
import { History, ArrowRight, BarChart3, Bot, Users } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import './Widgets.css';

const SearchHistorySpotlight = () => {
    const [history, setHistory] = useState([]);
    const navigate = useNavigate();

    useEffect(() => {
        // Fetch from localStorage (this would be set by CommandPalette)
        const getHistory = () => {
            const saved = localStorage.getItem('search_history');
            if (saved) {
                setHistory(JSON.parse(saved).slice(0, 5));
            }
        };

        getHistory();
        window.addEventListener('storage', getHistory);
        return () => window.removeEventListener('storage', getHistory);
    }, []);

    const getIcon = (type) => {
        switch (type) {
            case 'ticker': return BarChart3;
            case 'agent': return Bot;
            case 'client': return Users;
            default: return History;
        }
    };

    if (history.length === 0) return null;

    return (
        <div className="widget search-history animate-fade-in">
            <div className="widget__header">
                <History size={16} className="widget__icon" />
                <span className="widget__title">Recent Spotlight</span>
            </div>

            <div className="search-history__list">
                {history.map((item, idx) => {
                    const Icon = getIcon(item.type);
                    return (
                        <div 
                            key={`${item.id}-${idx}`} 
                            className="search-history__item"
                            onClick={() => navigate(item.path || `/${item.type}/${item.id}`)}
                        >
                            <Icon size={14} className="item-icon" />
                            <span className="item-label">{item.label}</span>
                            <ArrowRight size={12} className="item-arrow" />
                        </div>
                    );
                })}
            </div>
        </div>
    );
};

export default SearchHistorySpotlight;
