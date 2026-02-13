import React, { useState, useEffect } from 'react';
import { agentService } from '../../services/agentService';
import { AgentCard } from '../../components/cards/AgentCard';
import { HeartbeatWidget } from '../../components/widgets/HeartbeatWidget';
import { Search, Filter, RefreshCw, Cpu } from 'lucide-react';
import { toast } from 'sonner';

const AgentFleetOverview = () => {
    const [agents, setAgents] = useState([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState('');
    const [deptFilter, setDeptFilter] = useState('All');

    useEffect(() => {
        loadAgents();
        // Poll every 5s
        const interval = setInterval(loadAgents, 5000);
        return () => clearInterval(interval);
    }, []);
// ... (keep existing loadAgents, handleRestart, filters)

    // Reconstruct the layout to sidebar/main or grid
    const departments = ['All', ...new Set(agents.map(a => a.department))];

    const filteredAgents = agents.filter(a => {
        const matchesSearch = a.name.toLowerCase().includes(filter.toLowerCase()) || 
                              a.id.toLowerCase().includes(filter.toLowerCase());
        const matchesDept = deptFilter === 'All' || a.department === deptFilter;
        return matchesSearch && matchesDept;
    });

    return (
        <div className="h-full bg-slate-950 p-6 text-slate-200 overflow-y-auto">
            <div className="flex flex-col xl:flex-row gap-6 h-full">
                {/* Main Content */}
                <div className="flex-1 flex flex-col">
                    <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
                        <div>
                             <h1 className="text-2xl font-bold bg-gradient-to-r from-purple-400 to-pink-500 bg-clip-text text-transparent flex items-center gap-3">
                                <Cpu className="text-purple-500" /> Agent Fleet Command
                            </h1>
                            <p className="text-slate-500 text-sm mt-1">
                                Monitoring {agents.length} autonomous agents across {departments.length - 1} departments
                            </p>
                        </div>

                        <div className="flex items-center gap-3 w-full md:w-auto">
                            <div className="relative flex-1 md:w-64">
                                <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
                                <input 
                                    value={filter}
                                    onChange={(e) => setFilter(e.target.value)}
                                    placeholder="Find agent..."
                                    className="w-full bg-slate-900 border border-slate-800 rounded-lg py-2 pl-9 pr-4 text-sm focus:outline-none focus:border-purple-500"
                                />
                            </div>
                            
                            <select 
                                value={deptFilter}
                                onChange={(e) => setDeptFilter(e.target.value)}
                                className="bg-slate-900 border border-slate-800 rounded-lg py-2 px-3 text-sm focus:outline-none focus:border-purple-500"
                            >
                                {departments.map(d => <option key={d} value={d}>{d}</option>)}
                            </select>

                            <button 
                                onClick={loadAgents}
                                className="p-2 bg-slate-900 border border-slate-800 rounded-lg hover:bg-slate-800 transition-colors"
                            >
                                <RefreshCw size={18} className={loading ? "animate-spin" : ""} />
                            </button>
                        </div>
                    </div>

                    {loading && agents.length === 0 ? (
                        <div className="flex items-center justify-center h-64">
                            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-purple-500"></div>
                        </div>
                    ) : (
                        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-3 gap-4 pb-6">
                            {filteredAgents.map(agent => (
                                <AgentCard key={agent.id} agent={agent} onRestart={handleRestart} />
                            ))}
                        </div>
                    )}
                </div>

                {/* Sidebar Widgets */}
                <div className="w-full xl:w-80 flex flex-col gap-4">
                    <HeartbeatWidget />
                    <RogueDetectorWidget />
                </div>
            </div>
        </div>
    );
};

export default AgentFleetOverview;
