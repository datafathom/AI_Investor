import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Sigma, HelpCircle } from 'lucide-react';
import { ResponsiveContainer, LineChart, Line, XAxis, YAxis, Tooltip } from 'recharts';

const MonteCarloWidget = () => {
    const [sim, setSim] = useState(null);

    const runSim = async () => {
        try {
            const res = await apiClient.post('/simulation/monte-carlo');
            if (res.data.success) setSim(res.data.data);
        } catch (e) {
            console.error(e);
        }
    };

    return (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 h-full flex flex-col">
            <div className="flex justify-between items-start mb-4">
                <h3 className="text-white font-bold flex items-center gap-2">
                    <Sigma className="text-pink-500" /> Monte Carlo Simulation
                </h3>
                <button onClick={runSim} className="text-xs bg-slate-800 px-2 py-1 rounded text-white hover:bg-slate-700">RUN</button>
            </div>

            {sim ? (
                <>
                    <div className="flex-1 min-h-[150px]">
                         <ResponsiveContainer width="100%" height="100%">
                            <LineChart>
                                {sim.paths.slice(0, 20).map((path, i) => (
                                    <Line 
                                        key={i} 
                                        data={path.map((val, idx) => ({ idx, val }))} 
                                        type="monotone" 
                                        dataKey="val" 
                                        stroke="#ec4899" 
                                        strokeWidth={1} 
                                        dot={false}
                                        opacity={0.3}
                                    />
                                ))}
                            </LineChart>
                        </ResponsiveContainer>
                    </div>
                    <div className="grid grid-cols-2 gap-2 mt-4 text-center">
                        <div className="bg-slate-950 p-2 rounded">
                            <div className="text-[10px] uppercase text-slate-500">Median Wealth</div>
                            <div className="font-bold text-white">${sim.metrics.median_terminal_wealth.toFixed(0)}</div>
                        </div>
                        <div className="bg-slate-950 p-2 rounded">
                            <div className="text-[10px] uppercase text-slate-500">Ruin Prob</div>
                            <div className="font-bold text-red-400">{(sim.metrics.ruin_prob * 100).toFixed(1)}%</div>
                        </div>
                    </div>
                </>
            ) : (
                <div className="flex-1 flex items-center justify-center text-slate-500 text-sm">
                    Click RUN to simulate 1000 outcomes
                </div>
            )}
        </div>
    );
};

export default MonteCarloWidget;
