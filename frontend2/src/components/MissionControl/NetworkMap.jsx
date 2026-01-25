import React, { useState } from 'react';
import { Server, Database, Cloud, Shield, Globe, Cpu, Activity, Zap } from 'lucide-react';
import './NetworkMap.css'; // Assume basic CSS for positioning

const NetworkMap = () => {
    const [selectedNode, setSelectedNode] = useState(null);

    const nodes = [
        { id: 'core', label: 'Core Brain', type: 'brain', x: 50, y: 50, status: 'active', load: 45 },
        { id: 'db1', label: 'Postgres', type: 'db', x: 20, y: 30, status: 'active', load: 12 },
        { id: 'db2', label: 'Neo4j', type: 'db', x: 80, y: 30, status: 'active', load: 28 },
        { id: 'api', label: 'External APIs', type: 'cloud', x: 50, y: 15, status: 'warning', load: 78 },
        { id: 'exec', label: 'Execution', type: 'server', x: 50, y: 85, status: 'active', load: 5 },
        { id: 'agent1', label: 'Analyst Alpha', type: 'agent', x: 20, y: 70, status: 'active', load: 60 },
        { id: 'agent2', label: 'Risk Guardian', type: 'agent', x: 80, y: 70, status: 'active', load: 20 },
    ];

    const links = [
        { from: 'core', to: 'db1' },
        { from: 'core', to: 'db2' },
        { from: 'core', to: 'api' },
        { from: 'core', to: 'exec' },
        { from: 'core', to: 'agent1' },
        { from: 'core', to: 'agent2' },
    ];

    const renderIcon = (type) => {
        switch (type) {
            case 'brain': return <Cpu size={24} className="text-cyan-400" />;
            case 'db': return <Database size={20} className="text-indigo-400" />;
            case 'cloud': return <Cloud size={20} className="text-blue-400" />;
            case 'server': return <Server size={20} className="text-green-400" />;
            case 'agent': return <Shield size={20} className="text-purple-400" />;
            default: return <Activity size={20} />;
        }
    };

    return (
        <div className="relative w-full h-full bg-slate-900/50 rounded-xl overflow-hidden border border-slate-800 flex items-center justify-center p-4">
            {/* Background Grid */}
            <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:40px_40px]"></div>

            {/* SVG Lines */}
            <svg className="absolute inset-0 w-full h-full pointer-events-none">
                {links.map((link, i) => {
                    const fromNode = nodes.find(n => n.id === link.from);
                    const toNode = nodes.find(n => n.id === link.to);
                    return (
                        <line
                            key={i}
                            x1={`${fromNode.x}%`} y1={`${fromNode.y}%`}
                            x2={`${toNode.x}%`} y2={`${toNode.y}%`}
                            stroke="#1e293b"
                            strokeWidth="2"
                            strokeDasharray="4"
                            className="animate-pulse"
                        />
                    );
                })}
            </svg>

            {/* Nodes */}
            {nodes.map(node => (
                <div
                    key={node.id}
                    onClick={() => setSelectedNode(node)}
                    className={`absolute transform -translate-x-1/2 -translate-y-1/2 cursor-pointer transition-all hover:scale-110 z-10 interact-hover`}
                    style={{ left: `${node.x}%`, top: `${node.y}%` }}
                >
                    <div className={`p-3 rounded-full bg-slate-900 border-2 shadow-2xl flex flex-col items-center justify-center w-16 h-16 glass-premium ${selectedNode?.id === node.id ? 'border-amber-400 shadow-[0_0_20px_rgba(251,191,36,0.5)]' :
                        node.status === 'warning' ? 'border-amber-500/50' : 'border-cyan-500/30'
                        }`}>
                        <div className={`${node.status === 'active' ? 'animate-neon-pulse' : ''}`}>
                            {renderIcon(node.type)}
                        </div>
                        {node.load > 70 && <span className="absolute -top-1 -right-1 flex h-3 w-3">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75"></span>
                            <span className="relative inline-flex rounded-full h-3 w-3 bg-amber-500"></span>
                        </span>}
                    </div>
                    <div className="absolute top-full mt-2 left-1/2 -translate-x-1/2 text-[10px] font-bold text-slate-400 uppercase tracking-widest whitespace-nowrap bg-black/80 px-2 py-0.5 rounded backdrop-blur-sm border border-white/10 group-hover:text-white transition-colors">
                        {node.label}
                    </div>
                </div>
            ))}


            {/* Inspector Modal / Panel */}
            {selectedNode && (
                <div className="absolute bottom-4 left-4 right-4 bg-slate-900/95 backdrop-blur-md border border-slate-700 p-4 rounded-lg shadow-xl animate-in slide-in-from-bottom-5 glass-premium animate-fade-in">
                    <div className="flex justify-between items-start">
                        <div className="flex items-center gap-3">
                            <div className="p-2 bg-slate-800 rounded-lg">{renderIcon(selectedNode.type)}</div>
                            <div>
                                <h3 className="text-white font-bold">{selectedNode.label}</h3>
                                <div className="flex items-center gap-2 text-xs text-slate-400">
                                    <span className={`w-2 h-2 rounded-full ${selectedNode.status === 'active' ? 'bg-green-500' : 'bg-amber-500'}`}></span>
                                    Status: {selectedNode.status.toUpperCase()}
                                </div>
                            </div>
                        </div>
                        <button onClick={() => setSelectedNode(null)} className="text-slate-500 hover:text-white">✕</button>
                    </div>

                    <div className="mt-4 grid grid-cols-3 gap-2 text-xs">
                        <div className="bg-slate-800 p-2 rounded">
                            <span className="block text-slate-500">CPU Load</span>
                            <span className="text-white font-mono">{selectedNode.load}%</span>
                        </div>
                        <div className="bg-slate-800 p-2 rounded">
                            <span className="block text-slate-500">Latency</span>
                            <span className="text-white font-mono">{Math.floor(Math.random() * 50) + 10}ms</span>
                        </div>
                        <div className="bg-slate-800 p-2 rounded">
                            <span className="block text-slate-500">Uptime</span>
                            <span className="text-white font-mono">24h 12m</span>
                        </div>
                    </div>

                    {selectedNode.type === 'agent' && (
                        <div className="mt-3 p-2 bg-black/40 rounded border border-slate-700 text-[10px] font-mono text-green-400 overflow-hidden">
                            &gt; Thinking: Analyzing market depth for SPY...<br />
                            &gt; Action: Adjusting risk parameters...
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default NetworkMap;
