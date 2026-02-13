import React, { useState, useEffect } from 'react';
import { sectorService } from '../../services/sectorService';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell, ReferenceLine } from 'recharts';
import { RefreshCw, TrendingUp, TrendingDown, ArrowRight, RotateCw } from 'lucide-react';

export const SectorRotationWidget = () => {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const load = async () => {
            try {
                const res = await sectorService.getRotation();
                setData(res);
            } catch (e) {
                console.error(e);
            } finally {
                setLoading(false);
            }
        };
        load();
    }, []);

    if (loading) return <div className="animate-pulse h-64 bg-slate-900 rounded-xl"></div>;
    if (!data) return null;

    const { performance, signals } = data;

    return (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 h-full flex flex-col">
            <div className="flex justify-between items-center mb-6">
                 <h3 className="text-slate-400 font-bold text-xs uppercase tracking-wider flex items-center gap-2">
                    <RotateCw size={16} /> Sector Rotation Model
                </h3>
                <span className={`px-3 py-1 rounded-full text-xs font-bold ${
                    signals.phase === 'Recession' ? 'bg-red-500/20 text-red-500' : 
                    signals.phase === 'Late Cycle' ? 'bg-amber-500/20 text-amber-500' : 
                    'bg-emerald-500/20 text-emerald-500'
                }`}>
                    {signals.phase}
                </span>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
                {/* Signals */}
                <div className="space-y-4">
                    <div className="bg-emerald-500/10 border border-emerald-500/20 rounded-lg p-4">
                        <div className="text-emerald-500 text-xs font-bold uppercase mb-2 flex items-center gap-1">
                            <TrendingUp size={14} /> Rotate Into
                        </div>
                        <div className="flex flex-wrap gap-2">
                            {signals.rotate_into.map(s => (
                                <span key={s} className="px-2 py-1 bg-emerald-500/20 text-emerald-400 rounded text-xs font-bold border border-emerald-500/30">
                                    {s}
                                </span>
                            ))}
                        </div>
                    </div>

                    <div className="bg-red-500/10 border border-red-500/20 rounded-lg p-4">
                        <div className="text-red-500 text-xs font-bold uppercase mb-2 flex items-center gap-1">
                            <TrendingDown size={14} /> Rotate Out Of
                        </div>
                        <div className="flex flex-wrap gap-2">
                             {signals.rotate_out_of.map(s => (
                                <span key={s} className="px-2 py-1 bg-red-500/20 text-red-400 rounded text-xs font-bold border border-red-500/30">
                                    {s}
                                </span>
                            ))}
                        </div>
                    </div>
                    
                    <p className="text-xs text-slate-500 italic mt-2">
                        "{signals.rationale}"
                    </p>
                </div>

                {/* Performance Chart */}
                <div className="h-48">
                    <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={performance.slice(0, 8)} layout="vertical">
                            <XAxis type="number" hide />
                            <YAxis dataKey="sector" type="category" width={100} tick={{fontSize: 10, fill: '#94a3b8'}} />
                            <Tooltip 
                                contentStyle={{backgroundColor: '#0f172a', borderColor: '#1e293b', color: '#f1f5f9'}}
                                formatter={(val) => [`${(val * 100).toFixed(2)}%`, '3M Return']}
                            />
                            <ReferenceLine x={0} stroke="#475569" />
                            <Bar dataKey="return_3m" radius={[0, 4, 4, 0]}>
                                {performance.slice(0, 8).map((entry, index) => (
                                    <Cell key={`cell-${index}`} fill={entry.return_3m > 0 ? '#10b981' : '#ef4444'} />
                                ))}
                            </Bar>
                        </BarChart>
                    </ResponsiveContainer>
                </div>
            </div>
            
             <div className="mt-auto border-t border-slate-800 pt-4 text-center">
                 <button className="text-cyan-400 text-xs flex items-center justify-center gap-1 hover:text-cyan-300">
                    View Full Strategy <ArrowRight size={12} />
                 </button>
            </div>
        </div>
    );
};
