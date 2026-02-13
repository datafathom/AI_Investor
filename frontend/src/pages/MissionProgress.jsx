import React, { useState, useEffect } from 'react';
import apiClient from '../services/apiClient';
import { Flag, Trophy, TrendingUp, AlertTriangle } from 'lucide-react';
import { Responsive, WidthProvider } from 'react-grid-layout';

const ResponsiveGridLayout = WidthProvider(Responsive);

const MissionProgress = () => {
    const [missionData, setMissionData] = useState(null);

    useEffect(() => {
        loadProgress();
    }, []);

    const loadProgress = async () => {
        // Mock data tailored for Phase 12 verification
        setMissionData({
            overall_progress: 68,
            kpis: [
                { label: 'AUM Growth', value: '+12.5%', trend: 'up' },
                { label: 'Risk/Reward', value: '1.8', trend: 'stable' },
                { label: 'Active Agents', value: '42', trend: 'up' }
            ],
            timeline: [
                { date: '2026-01-01', event: 'Phase 1 Launch', completed: true },
                { date: '2026-03-15', event: 'Alpha Deployment', completed: true },
                { date: '2026-06-30', event: 'Series A Funding', completed: false }
            ]
        });
    };

    if (!missionData) return <div className="p-8 text-slate-500">Loading mission telemetry...</div>;

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
             <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <Flag className="text-blue-500" /> Mission Progress
                    </h1>
                    <p className="text-slate-500">Execution Velocity & KPI Tracking</p>
                </div>
                <div className="text-right">
                    <div className="text-4xl font-black text-blue-400">{missionData.overall_progress}%</div>
                    <div className="text-xs font-bold uppercase text-slate-500">Completion</div>
                </div>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
                {missionData.kpis.map((kpi, i) => (
                    <div key={i} className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex flex-col items-center justify-center">
                        <span className="text-slate-500 uppercase text-xs font-bold mb-2">{kpi.label}</span>
                        <span className="text-3xl font-mono font-bold text-white">{kpi.value}</span>
                        <span className={`text-xs mt-2 px-2 py-0.5 rounded ${kpi.trend === 'up' ? 'bg-green-500/20 text-green-400' : 'bg-slate-800 text-slate-400'}`}>
                            {kpi.trend.toUpperCase()}
                        </span>
                    </div>
                ))}
            </div>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                <h3 className="font-bold text-white mb-6 flex items-center gap-2">
                    <TrendingUp size={16} /> Strategic Timeline
                </h3>
                <div className="relative border-l border-slate-800 ml-4 space-y-8 pl-8">
                    {missionData.timeline.map((item, i) => (
                        <div key={i} className="relative">
                            <div className={`absolute -left-[37px] w-4 h-4 rounded-full border-2 ${item.completed ? 'bg-blue-500 border-blue-500' : 'bg-slate-900 border-slate-600'}`}></div>
                            <div className="flex justify-between items-center">
                                <div>
                                    <div className={`font-bold ${item.completed ? 'text-white' : 'text-slate-500'}`}>{item.event}</div>
                                    <div className="text-xs text-slate-600 font-mono">{item.date}</div>
                                </div>
                                {item.completed && <Trophy size={16} className="text-yellow-500" />}
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};

export default MissionProgress;
