import React from 'react';
import { ShieldCheck, Server, Cpu, Database, Activity, Globe } from 'lucide-react';

const AdminDashboard = () => {
    const services = [
        { name: 'Core API', status: 'Healthy', latency: '24ms', load: '12%' },
        { name: 'Data Ingestion', status: 'Healthy', latency: '142ms', load: '45%' },
        { name: 'Worker Fleet', status: 'Warning', latency: '850ms', load: '89%' },
        { name: 'Neo4j Graph', status: 'Healthy', latency: '12ms', load: '8%' },
    ];

    return (
        <div className="admin-dashboard glass-panel p-8 animate-fade-in">
             <header className="mb-10">
                <div className="flex items-center gap-4 mb-6">
                    <div className="p-3 bg-red-500/10 rounded-2xl text-red-400 border border-red-500/20 shadow-[0_0_15px_rgba(239,68,68,0.1)]">
                        <ShieldCheck size={28} />
                    </div>
                    <div>
                        <h1 className="text-4xl font-black text-white tracking-tight uppercase">Admin Control Center</h1>
                        <p className="text-zinc-500 font-medium">Agent and Cloud Infrastructure Health Monitoring</p>
                    </div>
                </div>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                <div className="md:col-span-2">
                    <h4 className="text-zinc-600 uppercase text-[10px] font-black tracking-[0.2em] mb-4">Service Status</h4>
                    <div className="space-y-4">
                        {services.map(s => (
                            <div key={s.name} className="bg-zinc-900/40 border border-zinc-800 p-4 rounded-xl flex items-center justify-between">
                                <div className="flex items-center gap-4">
                                    <div className={`w-2 h-2 rounded-full ${s.status === 'Healthy' ? 'bg-green-500' : 'bg-yellow-500'} animate-pulse`} />
                                    <span className="font-bold text-white">{s.name}</span>
                                </div>
                                <div className="flex gap-8 text-xs font-medium">
                                    <div className="flex flex-col">
                                        <span className="text-zinc-600 uppercase text-[8px] tracking-widest">Latency</span>
                                        <span className="text-zinc-300">{s.latency}</span>
                                    </div>
                                    <div className="flex flex-col">
                                        <span className="text-zinc-600 uppercase text-[8px] tracking-widest">Load</span>
                                        <span className="text-zinc-300">{s.load}</span>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="space-y-8">
                     <section>
                        <h4 className="text-zinc-600 uppercase text-[10px] font-black tracking-[0.2em] mb-4">Infrastucture Quick Stats</h4>
                        <div className="grid grid-cols-1 gap-4">
                            <div className="bg-zinc-800/30 p-4 rounded-xl border border-zinc-800">
                                <div className="text-zinc-500 text-[8px] uppercase font-bold tracking-[0.2em] mb-1">Total Servers</div>
                                <div className="text-2xl font-black text-white">42</div>
                            </div>
                            <div className="bg-zinc-800/30 p-4 rounded-xl border border-zinc-800">
                                <div className="text-zinc-500 text-[8px] uppercase font-bold tracking-[0.2em] mb-1">Active Agents</div>
                                <div className="text-2xl font-black text-white">128</div>
                            </div>
                        </div>
                    </section>
                </div>
            </div>
        </div>
    );
};

export default AdminDashboard;
