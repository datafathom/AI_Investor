import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { Activity, Zap, TrendingUp, AlertTriangle, Cpu } from 'lucide-react';

const MetaOptimizerDashboard = () => {
    const [performanceData, setPerformanceData] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const res = await apiClient.get('/meta/performance');
            if (res.data.success) {
                setPerformanceData(res.data.data);
            }
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    const triggerOptimization = async (agentId) => {
        try {
            await apiClient.post(`/meta/optimize/${agentId}`);
            alert(`Optimization loop started for ${agentId}`);
            // Optimistically update status
            setPerformanceData(prev => prev.map(p => 
                p.agent_id === agentId ? { ...p, opt_status: 'optimizing' } : p
            ));
        } catch (e) {
            console.error(e);
        }
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Cpu className="text-purple-500" /> Meta-Optimizer
                </h1>
                <p className="text-slate-500">Agent Performance Tracking & Self-Correction Loops</p>
            </header>

            <div className="grid grid-cols-1 gap-6">
                {/* Performance Grid */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                    <table className="w-full text-sm text-left">
                        <thead className="bg-slate-950 text-slate-500 uppercase text-xs">
                            <tr>
                                <th className="p-4">Agent ID</th>
                                <th className="p-4">Win Rate</th>
                                <th className="p-4">ROI (24h)</th>
                                <th className="p-4">Latency</th>
                                <th className="p-4">Status</th>
                                <th className="p-4 text-right">Actions</th>
                            </tr>
                        </thead>
                        <tbody>
                            {loading ? (
                                <tr><td colSpan="6" className="p-8 text-center">Analysing neural pathways...</td></tr>
                            ) : performanceData.map(agent => (
                                <tr key={agent.agent_id} className="border-t border-slate-800 hover:bg-slate-800/30">
                                    <td className="p-4 font-bold text-white">{agent.agent_id}</td>
                                    <td className="p-4 font-mono text-green-400">{(agent.win_rate * 100).toFixed(1)}%</td>
                                    <td className="p-4 font-mono text-blue-400">{(agent.roi * 100).toFixed(1)}%</td>
                                    <td className="p-4 font-mono text-slate-400">{agent.latency_ms}ms</td>
                                    <td className="p-4">
                                        <span className={`px-2 py-1 rounded text-xs font-bold uppercase ${
                                            agent.opt_status === 'optimized' ? 'bg-green-500/10 text-green-400' :
                                            agent.opt_status === 'optimizing' ? 'bg-blue-500/10 text-blue-400 animate-pulse' :
                                            'bg-yellow-500/10 text-yellow-400'
                                        }`}>
                                            {agent.opt_status}
                                        </span>
                                    </td>
                                    <td className="p-4 text-right">
                                        <button 
                                            onClick={() => triggerOptimization(agent.agent_id)}
                                            className="bg-purple-600 hover:bg-purple-500 text-white px-3 py-1 rounded text-xs font-bold transition-colors flex items-center gap-1 ml-auto"
                                        >
                                            <Zap size={12} /> OPTIMIZE
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                {/* Training Viz Placeholder */}
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 h-64 flex items-center justify-center text-slate-600">
                    [Real-time Gradient Descent Visualization Placeholder]
                </div>
            </div>
        </div>
    );
};

export default MetaOptimizerDashboard;
