
import React, { useEffect, useState } from 'react';
import { dashboardService } from '../services/dashboardService';

const MissionControl = () => {
    const [allocation, setAllocation] = useState(null);
    const [risk, setRisk] = useState(null);
    const [execution, setExecution] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            const allocData = await dashboardService.getAllocation(50);
            setAllocation(allocData);

            const riskData = await dashboardService.getRiskStatus();
            setRisk(riskData);

            const execData = await dashboardService.getExecutionStatus();
            setExecution(execData);
        };

        fetchData();
        const interval = setInterval(fetchData, 5000); // Live update every 5s
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="mission-control-container p-6 bg-slate-900 text-white min-h-screen font-mono">
            <h1 className="text-4xl mb-8 text-cyan-400 font-bold border-b border-cyan-800 pb-4">
                MISSION CONTROL V2 
            </h1>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">

                {/* STRATEGY MODULE */}
                <div className="card bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-lg glow-cyan">
                    <h2 className="text-xl text-cyan-300 mb-4 ">STRATEGY ENGINE</h2>
                    {allocation ? (
                        <div>
                            <div className="flex justify-between mb-2">
                                <span>Fear Index:</span>
                                <span className="font-bold">{allocation.fear_index}</span>
                            </div>
                            <div className="h-4 bg-slate-700 rounded-full overflow-hidden flex mb-4">
                                <div style={{ width: `${allocation.buckets.SHIELD * 100}%` }} className="bg-blue-500 h-full transition-all"></div>
                                <div style={{ width: `${allocation.buckets.ALPHA * 100}%` }} className="bg-red-500 h-full transition-all"></div>
                                <div style={{ width: `${allocation.buckets.CASH * 100}%` }} className="bg-green-500 h-full transition-all"></div>
                            </div>
                            <div className="text-xs flex justify-between">
                                <span className="text-blue-400">SHIELD: {(allocation.buckets.SHIELD * 100).toFixed(0)}%</span>
                                <span className="text-red-400">ALPHA: {(allocation.buckets.ALPHA * 100).toFixed(0)}%</span>
                                <span className="text-green-400">CASH: {(allocation.buckets.CASH * 100).toFixed(0)}%</span>
                            </div>
                        </div>
                    ) : (
                        <p className="text-slate-500 animate-pulse">Initializing Strategy Link...</p>
                    )}
                </div>

                {/* RISK MODULE */}
                <div className="card bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-lg glow-red">
                    <h2 className="text-xl text-red-300 mb-4">RISK GOVERNOR</h2>
                    {risk ? (
                        <div>
                            <div className="flex justify-between mb-2">
                                <span>Daily VaR (95%):</span>
                                <span className="font-bold text-orange-400">${risk.var_95_daily.toFixed(0)}</span>
                            </div>
                            <div className="flex justify-between mb-2">
                                <span>Circuit Breaker:</span>
                                <span className={`font-bold ${risk.portfolio_frozen ? 'text-red-500 blink' : 'text-green-500'}`}>
                                    {risk.portfolio_frozen ? 'FROZEN ' : 'ACTIVE '}
                                </span>
                            </div>
                            {risk.freeze_reason && (
                                <div className="bg-red-900/50 p-2 rounded text-xs text-red-200 mt-2 border border-red-500">
                                     {risk.freeze_reason}
                                </div>
                            )}
                        </div>
                    ) : (
                        <p className="text-slate-500 animate-pulse">Scanning Risk Metrics...</p>
                    )}
                </div>

                {/* EXECUTION MODULE */}
                <div className="card bg-slate-800 p-6 rounded-xl border border-slate-700 shadow-lg glow-green">
                    <h2 className="text-xl text-green-300 mb-4">EXECUTION (PAPER)</h2>
                    {execution ? (
                        <div>
                            <div className="text-3xl font-bold mb-4 text-white">
                                ${execution.balance.toLocaleString()}
                            </div>
                            <h3 className="text-sm text-slate-400 mb-2">Active Positions:</h3>
                            <ul className="space-y-2">
                                {Object.entries(execution.positions).map(([symbol, pos]) => (
                                    <li key={symbol} className="flex justify-between bg-slate-900 p-2 rounded border border-slate-700">
                                        <span className="font-bold text-cyan-200">{symbol}</span>
                                        <span>{pos.quantity} shares</span>
                                    </li>
                                ))}
                                {Object.keys(execution.positions).length === 0 && <li className="text-slate-500 italic">No active positions</li>}
                            </ul>
                        </div>
                    ) : (
                        <p className="text-slate-500 animate-pulse">Connecting to Exchange...</p>
                    )}
                </div>

            </div>
        </div>
    );
};

export default MissionControl;
