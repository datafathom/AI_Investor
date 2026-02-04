import React, { useState, useEffect } from 'react';
import { Activity, Database, Cpu, Zap } from 'lucide-react';

const Neo4jHealthVitals = () => {
    const [stats, setStats] = useState({
        nodes: 1248,
        relationships: 4521,
        queryLatency: 12,
        memoryUsage: 450, // MB
        throughput: 85
    });

    useEffect(() => {
        const interval = setInterval(() => {
            setStats(prev => ({
                ...prev,
                queryLatency: Math.max(5, prev.queryLatency + (Math.random() - 0.5) * 2),
                memoryUsage: Math.max(400, prev.memoryUsage + (Math.random() - 0.5) * 5),
                throughput: Math.max(70, prev.throughput + (Math.random() - 0.5) * 4)
            }));
        }, 3000);
        return () => clearInterval(interval);
    }, []);

    const Metric = ({ icon: Icon, label, value, unit, color }) => (
        <div className="flex items-center justify-between p-2.5 bg-white/5 rounded-lg border border-white/5">
            <div className="flex items-center gap-3">
                <div className={`p-1.5 rounded bg-${color}-500/10 border border-${color}-500/20`}>
                    <Icon size={14} className={`text-${color}-400`} />
                </div>
                <span className="text-zinc-400 text-xs font-semibold">{label}</span>
            </div>
            <div className="flex items-baseline gap-1">
                <span className="text-white text-sm font-mono font-bold">{Math.round(value)}</span>
                <span className="text-zinc-500 text-[10px] uppercase font-bold">{unit}</span>
            </div>
        </div>
    );

    return (
        <div className="w-full h-full flex flex-col p-4 space-y-2">
            <Metric icon={Database} label="Knowledge Nodes" value={stats.nodes} unit="nodes" color="blue" />
            <Metric icon={Zap} label="Relationships" value={stats.relationships} unit="edges" color="purple" />
            <Metric icon={Cpu} label="Memory allocation" value={stats.memoryUsage} unit="mb" color="cyan" />
            <Metric icon={Activity} label="avg latency" value={stats.queryLatency} unit="ms" color="emerald" />
            
            <div className="mt-4 pt-4 border-t border-white/5">
                <div className="flex justify-between items-center mb-2">
                    <span className="text-zinc-500 text-[10px] uppercase font-black tracking-widest">Bolt Throughput</span>
                    <span className="text-emerald-400 text-[10px] font-mono">{Math.round(stats.throughput)}%</span>
                </div>
                <div className="h-1 w-full bg-zinc-800 rounded-full overflow-hidden">
                    <div 
                        className="h-full bg-emerald-500 animate-pulse"
                        style={{ width: `${stats.throughput}%` }}
                    />
                </div>
            </div>
        </div>
    );
};

export default Neo4jHealthVitals;
