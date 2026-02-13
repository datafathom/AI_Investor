import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Target, PieChart, Info, DollarSign } from 'lucide-react';

const PositionGreeksAnalyzer = () => {
    const [portfolio, setPortfolio] = useState(null);

    useEffect(() => {
        const loadData = async () => {
            try {
                const res = await apiClient.get('/options/portfolio/greeks');
                if (res.data.success) setPortfolio(res.data.data);
            } catch (e) { console.error(e); }
        };
        loadData();
    }, []);

    if (!portfolio) return <div className="p-8 text-slate-500">Calculating Net Exposure...</div>;

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Target className="text-emerald-500" /> Position Greeks
                </h1>
                <p className="text-slate-500">Net Portfolio Exposure & Risk Attribution</p>
            </header>

            {/* Net Greeks Cards */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Net Delta</div>
                    <div className="text-2xl font-bold text-white">{portfolio.net_delta.toFixed(2)}</div>
                    <div className="text-xs text-slate-400 mt-1">Share Equivalents</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Net Gamma</div>
                    <div className="text-2xl font-bold text-purple-400">{portfolio.net_gamma.toFixed(2)}</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Net Theta</div>
                    <div className="text-2xl font-bold text-red-400">{portfolio.net_theta.toFixed(2)}</div>
                    <div className="text-xs text-slate-400 mt-1">Daily Decay</div>
                </div>
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="text-xs uppercase text-slate-500 font-bold mb-2">Net Vega</div>
                    <div className="text-2xl font-bold text-blue-400">{portfolio.net_vega.toFixed(2)}</div>
                    <div className="text-xs text-slate-400 mt-1">Exposure to 1% IV Move</div>
                </div>
            </div>

            {/* Position Attribution */}
            <div className="bg-slate-900 border border-slate-800 rounded-xl overflow-hidden">
                <div className="p-4 border-b border-slate-800 bg-slate-950 font-bold text-white">
                    Risk Attribution by Underlying
                </div>
                <table className="w-full text-sm text-left">
                    <thead className="bg-slate-950 text-slate-500 uppercase text-xs">
                        <tr>
                            <th className="p-4">Symbol</th>
                            <th className="p-4 text-right">Delta</th>
                            <th className="p-4 text-right">Gamma</th>
                            <th className="p-4 text-right">Theta</th>
                            <th className="p-4 text-right">Vega</th>
                        </tr>
                    </thead>
                    <tbody>
                        {portfolio.positions.map(pos => (
                            <tr key={pos.symbol} className="border-t border-slate-800 hover:bg-slate-800/50">
                                <td className="p-4 font-bold text-white">{pos.symbol}</td>
                                <td className="p-4 text-right font-mono text-slate-300">{pos.delta.toFixed(1)}</td>
                                <td className="p-4 text-right font-mono text-purple-300">{pos.gamma.toFixed(2)}</td>
                                <td className="p-4 text-right font-mono text-red-300">{pos.theta.toFixed(2)}</td>
                                <td className="p-4 text-right font-mono text-blue-300">{pos.vega.toFixed(1)}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
};

export default PositionGreeksAnalyzer;
