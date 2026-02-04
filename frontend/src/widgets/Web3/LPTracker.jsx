import React, { useEffect } from 'react';
import { Layers, AlertTriangle, TrendingUp, Info } from 'lucide-react';
import { useWeb3Store } from '../../stores/web3Store';

const LPTracker = () => {
    const { lpPositions, fetchLPPositions } = useWeb3Store();

    useEffect(() => {
        fetchLPPositions('default_user');
    }, []);

    // Helper to determine drain alert color. Using safe mock logic if drain_alert exists
    const getAlertColor = (severity) => {
        switch (severity) {
            case 'critical': return 'text-red-500 border-red-500/50 bg-red-500/10';
            case 'high': return 'text-orange-500 border-orange-500/50 bg-orange-500/10';
            case 'medium': return 'text-yellow-500 border-yellow-500/50 bg-yellow-500/10';
            default: return 'text-slate-500';
        }
    };

    return (
        <div className="lp-tracker h-full flex flex-col">
            <div className="flex-1 overflow-y-auto custom-scrollbar space-y-3 pr-1">
                {lpPositions.length === 0 ? (
                    <div className="text-center text-slate-500 py-8">No LP positions found.</div>
                ) : (
                    lpPositions.map((pos, idx) => (
                        <div key={idx} className="lp-card p-4 rounded-xl bg-slate-900/40 border border-slate-800 hover:border-slate-700 transition-all">
                            <div className="flex justify-between items-start mb-3">
                                <div className="flex items-center gap-2">
                                    <div className="flex -space-x-2">
                                        <div className="w-6 h-6 rounded-full bg-blue-500 flex items-center justify-center text-[10px] text-white font-bold border-2 border-slate-900">{pos.token0[0]}</div>
                                        <div className="w-6 h-6 rounded-full bg-purple-500 flex items-center justify-center text-[10px] text-white font-bold border-2 border-slate-900">{pos.token1[0]}</div>
                                    </div>
                                    <div>
                                        <h4 className="text-sm font-bold text-white">{pos.token0}-{pos.token1}</h4>
                                        <div className="text-[10px] text-slate-500 font-mono">{pos.pool_address.substring(0, 8)}...</div>
                                    </div>
                                </div>
                                <div className="text-right">
                                    <div className="text-xs text-slate-400">Pool Share</div>
                                    <div className="text-sm font-medium text-cyan-400">{(pos.pool_share * 100).toFixed(4)}%</div>
                                </div>
                            </div>

                            <div className="grid grid-cols-2 gap-2 mb-3">
                                <div className="bg-slate-950/50 p-2 rounded-lg border border-slate-800/50">
                                    <div className="text-[10px] text-slate-500 mb-1">Position Value</div>
                                    <div className="text-sm font-bold text-white">${pos.impermanent_loss.lp_value_usd.toLocaleString()}</div>
                                </div>
                                <div className="bg-slate-950/50 p-2 rounded-lg border border-slate-800/50">
                                    <div className="text-[10px] text-slate-500 mb-1">Fees Earned (30d)</div>
                                    <div className="text-sm font-bold text-emerald-400">+${pos.impermanent_loss.fees_earned_usd.toFixed(2)}</div>
                                </div>
                            </div>

                            {/* Impermanent Loss Section */}
                            <div className="mb-3">
                                <div className="flex justify-between text-xs mb-1">
                                    <span className="text-slate-400">Impermanent Loss</span>
                                    <span className="text-rose-400">-{pos.impermanent_loss.loss_percent.toFixed(2)}%</span>
                                </div>
                                <div className="w-full h-1.5 bg-slate-800 rounded-full overflow-hidden">
                                    <div 
                                        className="h-full bg-rose-500 rounded-full" 
                                        style={{ width: `${Math.min(Math.abs(pos.impermanent_loss.loss_percent) * 5, 100)}%` }} // Visual scale
                                    ></div>
                                </div>
                                <div className="flex justify-between text-[10px] text-slate-500 mt-1">
                                    <span>HODL: ${pos.impermanent_loss.hodl_value_usd.toLocaleString()}</span>
                                    <span>Loss: -${pos.impermanent_loss.loss_usd.toFixed(2)}</span>
                                </div>
                            </div>

                            {/* Drain Alert */}
                            {pos.drain_alert && (
                                <div className={`p-2 rounded-lg border ${getAlertColor(pos.drain_alert.severity)} flex gap-2 items-start`}>
                                    <AlertTriangle size={14} className="mt-0.5 shrink-0" />
                                    <div>
                                        <div className="text-xs font-bold uppercase tracking-wider">{pos.drain_alert.severity} DRAIN ALERT</div>
                                        <div className="text-[10px] leading-tight mt-0.5">{pos.drain_alert.recommendation}</div>
                                    </div>
                                </div>
                            )}

                             {!pos.drain_alert && (
                                <div className="text-[10px] text-center text-slate-600 flex items-center justify-center gap-1">
                                    <Layers size={10} /> Liquidity Health Normal
                                </div>
                            )}
                        </div>
                    ))
                )}
            </div>
        </div>
    );
};

export default LPTracker;
