import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Network, Activity } from 'lucide-react';

const CorrelationRisk = () => {
    const [matrix, setMatrix] = useState([]);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/risk/correlations');
            if (res.data.success) setMatrix(res.data.data);
        };
        load();
    }, []);

    const getColor = (val) => {
        if (val >= 0.8) return 'bg-red-500/40 text-red-100';
        if (val >= 0.5) return 'bg-yellow-500/40 text-yellow-100';
        return 'bg-green-500/20 text-green-200';
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <Network className="text-pink-500" /> Correlation Risk Monitor
                </h1>
                <p className="text-slate-500">Asset Clustering & Diversification Analysis</p>
            </header>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-8 overflow-x-auto">
                <h3 className="font-bold text-white mb-6">Correlation Matrix</h3>
                {matrix.length > 0 && (
                    <table className="border-collapse">
                        <thead>
                            <tr>
                                <th className="p-2"></th>
                                {Object.keys(matrix[0].correlations).map(sym => (
                                    <th key={sym} className="p-2 text-xs uppercase text-slate-500 w-16 text-center">{sym}</th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {matrix.map(row => (
                                <tr key={row.symbol}>
                                    <td className="p-2 font-bold text-white text-right pr-4">{row.symbol}</td>
                                    {Object.entries(row.correlations).map(([sym, val]) => (
                                        <td key={sym} className="p-1">
                                            <div className={`w-16 h-10 flex items-center justify-center rounded text-xs font-bold ${getColor(val)}`}>
                                                {val.toFixed(2)}
                                            </div>
                                        </td>
                                    ))}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                )}
            </div>
            
            <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-2">Cluster Analysis</h3>
                    <p className="text-slate-500 text-sm">
                        High correlation detected between <strong>Tech</strong> and <strong>Crypto</strong> assets (0.85). 
                        Consider reducing exposure to improve diversification score.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default CorrelationRisk;
