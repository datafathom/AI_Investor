import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { LogOut, Calculator } from 'lucide-react';

const ExitPlanner = () => {
    const [strategies, setStrategies] = useState([]);
    const [simulation, setSimulation] = useState(null);

    useEffect(() => {
        const load = async () => {
            const res = await apiClient.get('/assets/exit-plans');
            if (res.data.success) setStrategies(res.data.data);
        };
        load();
    }, []);

    const simulate = async () => {
        const res = await apiClient.post('/assets/exit-plans/simulate', null, { params: { asset_id: "mock", discount_pct: 0.05 } });
        if (res.data.success) setSimulation(res.data.data);
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8">
                <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                    <LogOut className="text-red-400" /> Exit Strategy Planner
                </h1>
                <p className="text-slate-500">Liquidity Events & Tax Implications</p>
            </header>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <h3 className="font-bold text-white mb-6">Active Exit Plans</h3>
                    <div className="space-y-4">
                        {strategies.map((s, i) => (
                            <div key={i} className="p-4 bg-slate-950 rounded border border-slate-800">
                                <div className="flex justify-between mb-2">
                                    <span className="font-bold text-white">{s.asset}</span>
                                    <span className="text-xs bg-slate-800 text-slate-300 px-2 py-1 rounded">{s.probability * 100}% PROB</span>
                                </div>
                                <div className="text-sm text-slate-400">{s.strategy}</div>
                                <div className="text-sm text-emerald-400 mt-1">Target: ${s.target_price.toLocaleString()}</div>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="bg-slate-900 border border-slate-800 rounded-xl p-6">
                    <div className="flex justify-between items-center mb-6">
                        <h3 className="font-bold text-white flex items-center gap-2">
                            <Calculator size={18} /> Liquidation Simulator
                        </h3>
                        <button onClick={simulate} className="bg-slate-800 hover:bg-slate-700 text-white text-xs font-bold px-3 py-1 rounded">
                            RUN SIM
                        </button>
                    </div>

                    {simulation ? (
                        <div className="space-y-4">
                            <div className="flex justify-between items-center p-3 bg-slate-950 rounded">
                                <span className="text-slate-400 text-sm">Gross Proceeds</span>
                                <span className="text-white font-bold">${simulation.gross_proceeds.toLocaleString()}</span>
                            </div>
                            <div className="flex justify-between items-center p-3 bg-slate-950 rounded border border-red-900/30">
                                <span className="text-slate-400 text-sm">Est. Taxes</span>
                                <span className="text-red-400 font-bold">-${simulation.taxes.toLocaleString()}</span>
                            </div>
                            <div className="flex justify-between items-center p-3 bg-slate-950 rounded border border-red-900/30">
                                <span className="text-slate-400 text-sm">Fees/Commissions</span>
                                <span className="text-red-400 font-bold">-${simulation.fees.toLocaleString()}</span>
                            </div>
                            <div className="mt-4 pt-4 border-t border-slate-800 flex justify-between items-center">
                                <span className="text-slate-200 font-bold">NET PROCEEDS</span>
                                <span className="text-emerald-400 font-bold text-xl">${simulation.net_proceeds.toLocaleString()}</span>
                            </div>
                            <div className="text-xs text-center text-slate-500 mt-2">
                                Estimated Time to Close: {simulation.time_to_close}
                            </div>
                        </div>
                    ) : (
                        <div className="text-center text-slate-500 py-12">
                            Run simulation to see net proceeds breakdown.
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ExitPlanner;
