import React, { useState, useEffect } from 'react';
import { pricingService } from '../../services/pricingService';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { Sigma, Gauge } from 'lucide-react';

export const ProbabilityConeWidget = ({ ticker = 'AAPL', currentPrice = 150, iv = 0.25 }) => {
    const [data, setData] = useState(null);
    const [expectedMove, setExpectedMove] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const load = async () => {
            try {
                const [coneRes, moveRes] = await Promise.all([
                    pricingService.getProbabilityCone(ticker, currentPrice, iv, 45),
                    pricingService.getExpectedMove(ticker, currentPrice, iv, 30)
                ]);
                setData(coneRes);
                setExpectedMove(moveRes);
            } catch (e) {
                console.error(e);
            } finally {
                setLoading(false);
            }
        };
        load();
    }, [ticker, currentPrice, iv]);

    if (loading) return <div className="animate-pulse h-64 bg-slate-900 rounded-xl"></div>;
    if (!data) return null;

    return (
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 h-full flex flex-col">
            <div className="flex justify-between items-center mb-6">
                 <h3 className="text-slate-400 font-bold text-xs uppercase tracking-wider flex items-center gap-2">
                    <Sigma size={16} /> Probability Cone (IV: {(iv * 100).toFixed(0)}%)
                </h3>
            </div>

            <div className="flex-1 min-h-[200px]">
                <ResponsiveContainer width="100%" height="100%">
                    <AreaChart data={data.data}>
                        <defs>
                            <linearGradient id="grad1sd" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.3}/>
                                <stop offset="95%" stopColor="#8b5cf6" stopOpacity={0}/>
                            </linearGradient>
                            <linearGradient id="grad2sd" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.1}/>
                                <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                            </linearGradient>
                        </defs>
                        <XAxis dataKey="date" hide />
                        <YAxis domain={['auto', 'auto']} stroke="#475569" fontSize={10} width={40} />
                        <Tooltip 
                            contentStyle={{backgroundColor: '#0f172a', borderColor: '#1e293b', color: '#f1f5f9'}}
                            labelFormatter={(label) => new Date(label).toLocaleDateString()}
                        />
                        <Area type="monotone" dataKey="upper_2sd" stackId="2" stroke="none" fill="url(#grad2sd)" />
                        <Area type="monotone" dataKey="lower_2sd" stackId="2" stroke="none" fill="url(#grad2sd)" />
                        <Area type="monotone" dataKey="upper_1sd" stackId="1" stroke="#8b5cf6" fill="url(#grad1sd)" strokeDasharray="3 3" />
                        <Area type="monotone" dataKey="lower_1sd" stackId="1" stroke="#8b5cf6" fill="url(#grad1sd)" strokeDasharray="3 3" />
                        <Area type="monotone" dataKey="price" stroke="#ffffff" strokeWidth={2} fill="none" />
                        
                        {expectedMove && (
                             <ReferenceLine x={expectedMove.dte} stroke="#f59e0b" label="Exp" />
                        )}
                    </AreaChart>
                </ResponsiveContainer>
            </div>

            {expectedMove && (
                <div className="mt-4 flex justify-between items-center bg-slate-950 p-3 rounded border border-slate-800">
                    <div className="flex items-center gap-2 text-slate-400 text-xs">
                        <Gauge size={14} /> Expected Move (30 Days)
                    </div>
                    <div className="text-amber-400 font-mono font-bold">
                        ±${expectedMove.expected_move}
                    </div>
                </div>
            )}
        </div>
    );
};
