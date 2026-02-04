import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';
import GlassCard from '../Controls/GlassCard';
import Badge from '../Controls/Badge';

const OptionsFlowTable = ({ alerts = [] }) => {
    return (
        <GlassCard title="UNUSUAL OPTIONS FLOW" subTitle="Institutional Whale Tracking">
            <div className="overflow-x-auto mt-2">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="text-cyan-500/60 uppercase text-[10px] tracking-widest border-b border-cyan-500/20">
                            <th className="pb-2 px-2">Ticker</th>
                            <th className="pb-2 px-2">Type</th>
                            <th className="pb-2 px-2">Strike</th>
                            <th className="pb-2 px-2">Exp</th>
                            <th className="pb-2 px-2">Vol/OI</th>
                            <th className="pb-2 px-2">Alert</th>
                        </tr>
                    </thead>
                    <tbody className="text-xs">
                        {alerts.length === 0 ? (
                            <tr>
                                <td colSpan="6" className="py-4 text-center text-cyan-500/40 italic">
                                    Scanning for institutional sweeps...
                                </td>
                            </tr>
                        ) : (
                            alerts.map((alert, idx) => (
                                <tr
                                    key={idx}
                                    className="border-b border-cyan-500/10 hover:bg-cyan-500/5 transition-colors"
                                >
                                    <td className="py-2 px-2 font-bold text-cyan-400">{alert.symbol}</td>
                                    <td className="py-2 px-2">
                                        {alert.type.toUpperCase() === 'CALL' ? (
                                            <span className="flex items-center text-green-400">
                                                <TrendingUp size={12} className="mr-1" /> CALL
                                            </span>
                                        ) : (
                                            <span className="flex items-center text-red-400">
                                                <TrendingDown size={12} className="mr-1" /> PUT
                                            </span>
                                        )}
                                    </td>
                                    <td className="py-2 px-2 text-white/80">${alert.strike}</td>
                                    <td className="py-2 px-2 text-white/60">{alert.expiration}</td>
                                    <td className="py-2 px-2">
                                        <div className="flex flex-col">
                                            <span className="text-cyan-300">{alert.volume}</span>
                                            <span className="text-[10px] text-white/30">{alert.open_interest} OI</span>
                                        </div>
                                    </td>
                                    <td className="py-2 px-2">
                                        <Badge status={alert.alert_type === 'WHALE_FLOW' ? 'active' : 'bullish'}>
                                            {alert.alert_type.replace('_', ' ')}
                                        </Badge>
                                    </td>
                                </tr>
                            ))
                        )}
                    </tbody>
                </table>
            </div>
        </GlassCard>
    );
};

export default OptionsFlowTable;
