import React, { useState, useEffect } from 'react';
import { factorService } from '../../services/factorService';
import FactorHeatmap from '../../components/charts/FactorHeatmap';
import { toast } from 'sonner';
import { Layers, PieChart, TrendingUp, Activity } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Legend } from 'recharts';

const FactorAnalysisSuite = () => {
    const [portfolio, setPortfolio] = useState([
        { ticker: "AAPL", weight: 0.25 },
        { ticker: "MSFT", weight: 0.25 },
        { ticker: "JPM", weight: 0.20 },
        { ticker: "XOM", weight: 0.15 },
        { ticker: "JNJ", weight: 0.15 },
    ]);
    const [analysis, setAnalysis] = useState(null);
    const [returns, setReturns] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            setLoading(true);
            const [analRes, retRes] = await Promise.all([
                factorService.analyzePortfolio(portfolio),
                factorService.getFactorReturns(30)
            ]);
            setAnalysis(analRes);
            setReturns(retRes);
        } catch (e) {
            toast.error("Failed to analyze factors");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="p-6 h-full flex flex-col bg-slate-950 text-slate-200 overflow-y-auto">
             <div className="flex justify-between items-center mb-8">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-3">
                        <Layers className="text-cyan-500" /> Factor Analysis Suite
                    </h1>
                    <p className="text-slate-400 mt-2">Decompose portfolio returns into systematic risk drivers.</p>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-8">
                {/* Exposure Panel */}
                <div className="lg:col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="text-slate-400 uppercase tracking-wider text-xs font-bold mb-4 flex items-center gap-2">
                        <PieChart size={16} /> Portfolio Factor Exposures
                    </h3>
                    {loading ? (
                        <div className="animate-pulse h-64 bg-slate-800 rounded"></div>
                    ) : (
                        <div className="flex flex-col gap-6">
                             <div className="grid grid-cols-2 gap-4">
                                <div className="bg-slate-800/10 p-4 rounded border border-slate-800">
                                    <span className="text-slate-500 text-xs">Style Bias</span>
                                    <div className="text-xl font-bold text-white">{analysis?.style}</div>
                                </div>
                                <div className="bg-slate-800/10 p-4 rounded border border-slate-800">
                                    <span className="text-slate-500 text-xs">Active Share (Est)</span>
                                    <div className="text-xl font-bold text-white">78%</div>
                                </div>
                             </div>
                             <FactorHeatmap exposures={analysis?.exposures} />
                        </div>
                    )}
                </div>

                {/* Portfolio Input (Mock) */}
                <div className="lg:col-span-1 bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="text-slate-400 uppercase tracking-wider text-xs font-bold mb-4">Target Portfolio</h3>
                    <div className="space-y-2">
                        {portfolio.map((pos, idx) => (
                            <div key={idx} className="flex justify-between items-center p-2 bg-slate-800 rounded text-sm">
                                <span className="font-bold text-white">{pos.ticker}</span>
                                <span className="font-mono text-cyan-400">{(pos.weight * 100).toFixed(0)}%</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Factor Returns Chart */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 flex-1 min-h-[300px]">
                <h3 className="text-slate-400 uppercase tracking-wider text-xs font-bold mb-4 flex items-center gap-2">
                    <Activity size={16} /> 30-Day Factor Performance
                </h3>
                 <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={returns}>
                        <XAxis dataKey="date" tick={false} stroke="#475569" />
                        <YAxis stroke="#475569" fontSize={12} />
                        <Tooltip contentStyle={{backgroundColor: '#0f172a', borderColor: '#1e293b', color: '#f1f5f9'}} />
                        <Legend />
                        <Bar dataKey="Mkt-RF" fill="#3b82f6" stackId="a" />
                        <Bar dataKey="SMB" fill="#10b981" stackId="a" />
                        <Bar dataKey="HML" fill="#f59e0b" stackId="a" />
                        <Bar dataKey="RMW" fill="#8b5cf6" stackId="a" />
                        <Bar dataKey="CMA" fill="#ec4899" stackId="a" />
                    </BarChart>
                </ResponsiveContainer>
            </div>
        </div>
    );
};

export default FactorAnalysisSuite;
