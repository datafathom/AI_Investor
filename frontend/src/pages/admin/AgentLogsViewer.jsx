import React, { useState, useEffect, useRef } from 'react';
import { agentService } from '../../services/agentService';
import { Terminal, RefreshCw, Filter, Search, Download } from 'lucide-react';
import { toast } from 'sonner';

const LogLevel = ({ level }) => {
    const styles = {
        INFO: 'text-blue-400',
        DEBUG: 'text-slate-500',
        WARNING: 'text-yellow-400',
        ERROR: 'text-red-400 font-bold',
    };
    return <span className={`w-16 ${styles[level] || 'text-white'}`}>{level}</span>;
};

const AgentLogsViewer = () => {
    const [agents, setAgents] = useState([]);
    const [selectedAgent, setSelectedAgent] = useState('');
    const [logs, setLogs] = useState([]);
    const [filter, setFilter] = useState('');
    const bottomRef = useRef(null);

    useEffect(() => {
        loadAgents();
    }, []);

    useEffect(() => {
        if (selectedAgent) {
            loadLogs(selectedAgent);
            const interval = setInterval(() => loadLogs(selectedAgent), 2000); // Live Stream
            return () => clearInterval(interval);
        }
    }, [selectedAgent]);

    const loadAgents = async () => {
        try {
            const res = await agentService.getFleetAgents();
            setAgents(res);
            if (res.length > 0) setSelectedAgent(res[0].id);
        } catch (e) {
            console.error("Failed to load agents");
        }
    };

    const loadLogs = async (agentId) => {
        try {
            const res = await agentService.getAgentLogs(agentId);
            setLogs(res);
            // scrollToBottom(); // Optional: Auto-scroll
        } catch (e) {
            console.error("Failed to load logs");
        }
    };

    const scrollToBottom = () => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    const filteredLogs = logs.filter(log => 
        log.message.toLowerCase().includes(filter.toLowerCase()) || 
        log.component.toLowerCase().includes(filter.toLowerCase())
    );

    return (
        <div className="h-full bg-slate-950 p-6 text-slate-200 flex flex-col">
            <div className="flex justify-between items-center mb-6">
                 <h1 className="text-2xl font-bold text-white flex items-center gap-3">
                    <Terminal className="text-emerald-500" /> Agent Live Logs
                </h1>

                <div className="flex items-center gap-3">
                    <select 
                        value={selectedAgent}
                        onChange={(e) => setSelectedAgent(e.target.value)}
                        className="bg-slate-900 border border-slate-800 rounded-lg py-2 px-3 text-sm focus:outline-none focus:border-emerald-500 w-64"
                    >
                        {agents.map(a => <option key={a.id} value={a.id}>{a.name} ({a.id})</option>)}
                    </select>

                    <div className="relative w-64">
                         <Search size={16} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
                        <input 
                            value={filter}
                            onChange={(e) => setFilter(e.target.value)}
                            placeholder="Filter logs..."
                            className="w-full bg-slate-900 border border-slate-800 rounded-lg py-2 pl-9 pr-4 text-sm focus:outline-none focus:border-emerald-500"
                        />
                    </div>
                </div>
            </div>

            <div className="flex-1 bg-slate-900 border border-slate-800 rounded-xl font-mono text-sm p-4 overflow-y-auto shadow-inner custom-scrollbar">
                {filteredLogs.length === 0 ? (
                    <div className="text-slate-600 text-center mt-20">No logs found</div>
                ) : (
                    <div className="space-y-1">
                        {filteredLogs.map((log, i) => (
                            <div key={i} className="flex hover:bg-slate-800/30 p-0.5 rounded">
                                <span className="text-slate-600 w-32 shrink-0 select-none">
                                    {new Date(log.timestamp).toLocaleTimeString()}
                                </span>
                                <LogLevel level={log.level} />
                                <span className="text-purple-400 w-32 shrink-0 select-none">[{log.component}]</span>
                                <span className="text-slate-300 break-all">{log.message}</span>
                            </div>
                        ))}
                        <div ref={bottomRef} />
                    </div>
                )}
            </div>
            
            <div className="mt-2 text-xs text-slate-500 flex justify-between">
                <span>Total Lines: {filteredLogs.length}</span>
                <span className="flex items-center gap-1"><div className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></div> Live Stream Active</span>
            </div>
        </div>
    );
};

export default AgentLogsViewer;
