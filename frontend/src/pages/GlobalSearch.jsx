import React, { useState, useMemo } from 'react';
import { Search, Folder, Cpu, Shield, TrendingUp, Cpu as OrchestratorIcon } from 'lucide-react';
import { getAllDepartments } from '../config/departmentRegistry';
import './GlobalSearch.css';

const GlobalSearch = () => {
    const [query, setQuery] = useState('');
    const [activeFilter, setActiveFilter] = useState('all');

    const departments = useMemo(() => getAllDepartments(), []);
    
    // Flatten all submodules for searching
    const allModules = useMemo(() => {
        return departments.flatMap(dept => 
            (dept.subModules || []).map(sub => ({
                ...sub,
                deptName: dept.name,
                deptColor: dept.color,
                deptIcon: dept.icon
            }))
        );
    }, [departments]);

    const filteredResults = useMemo(() => {
        if (!query && activeFilter === 'all') return [];
        
        return allModules.filter(m => {
            const matchesQuery = !query || 
                               m.label.toLowerCase().includes(query.toLowerCase()) || 
                               m.description.toLowerCase().includes(query.toLowerCase()) ||
                               m.deptName.toLowerCase().includes(query.toLowerCase());
                               
            if (activeFilter === 'all') return matchesQuery;
            // Add more specific filtering if needed
            return matchesQuery;
        }).slice(0, 10);
    }, [allModules, query, activeFilter]);

    return (
        <div className="search-page">
            <div className="search-container">
                <div className="search-input-wrapper">
                    <Search className="search-icon" size={32} />
                    <input 
                        type="text" 
                        placeholder="Search assets, strategies, or agents..." 
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        autoFocus
                    />
                </div>

                <div className="search-filters">
                    {['all', 'departments', 'strategies', 'orders', 'documents'].map(filter => (
                        <div 
                            key={filter} 
                            className={`filter-chip ${activeFilter === filter ? 'active' : ''}`}
                            onClick={() => setActiveFilter(filter)}
                        >
                            {filter.toUpperCase()}
                        </div>
                    ))}
                </div>

                <div className="search-results">
                    {filteredResults.length > 0 ? (
                        filteredResults.map((result, idx) => (
                            <div key={idx} className="search-result-item" onClick={() => window.location.href = result.path}>
                                <div className="result-icon" style={{ backgroundColor: `${result.deptColor}22`, color: result.deptColor }}>
                                    <Folder size={20} />
                                </div>
                                <div className="result-info">
                                    <h4>{result.label}</h4>
                                    <p>{result.deptName} • {result.description}</p>
                                </div>
                                <TrendingUp size={16} className="ml-auto opacity-30" />
                            </div>
                        ))
                    ) : query && (
                        <div className="p-8 text-center text-gray-500">
                            No matching nodes found in the current namespace.
                        </div>
                    )}
                </div>

                {!query && (
                    <div className="mt-8 text-gray-500 text-sm">
                        <h5 className="text-gray-400 mb-4 uppercase tracking-widest">Suggested Command Nodes</h5>
                        <div className="grid grid-cols-2 gap-4">
                            <div className="p-4 bg-white/5 border border-white/10 rounded hover:bg-white/10 cursor-pointer">
                                <strong>/TERMINAL</strong>
                                <p className="text-xs opacity-50">Global command workspace</p>
                            </div>
                            <div className="p-4 bg-white/5 border border-white/10 rounded hover:bg-white/10 cursor-pointer">
                                <strong>/HOMEOSTASIS</strong>
                                <p className="text-xs opacity-50">Liquidity vs Debt equilibrium</p>
                            </div>
                        </div>
                    </div>
                )}
            </div>
            
            {/* Force Scroll Buffer */}
            <div style={{ height: '150px', width: '100%', flexShrink: 0 }} />
        </div>
    );
};

export default GlobalSearch;
