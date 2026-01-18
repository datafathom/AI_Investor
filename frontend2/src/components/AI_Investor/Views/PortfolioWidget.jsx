import React, { useEffect, useState } from 'react';
import {
    Wallet, Activity, TrendingUp, TrendingDown, DollarSign,
    ChevronDown, ChevronUp, Clock, AlertCircle, Briefcase, Zap
} from 'lucide-react';
import { brokerageService } from '../../../services/brokerageService';
import { AreaChart, Area, ResponsiveContainer, YAxis } from 'recharts';

/**
 * Mini-Sparkline Component for 24h Trend
 */
const Sparkline = ({ data, color }) => (
    <div className="h-8 w-24">
        <ResponsiveContainer width="100%" height="100%">
            <AreaChart data={data}>
                <defs>
                    <linearGradient id={`gradient-${color}`} x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor={color} stopOpacity={0.3} />
                        <stop offset="95%" stopColor={color} stopOpacity={0} />
                    </linearGradient>
                </defs>
                <Area
                    type="monotone"
                    dataKey="value"
                    stroke={color}
                    fillOpacity={1}
                    fill={`url(#gradient-${color})`}
                    strokeWidth={2}
                />
            </AreaChart>
        </ResponsiveContainer>
    </div>
);

/**
 * Global Header Component
 */
const GlobalHeader = ({ equity, dailyPL, buyingPower }) => (
    <div className="flex flex-col md:flex-row justify-between items-start md:items-center bg-black/40 backdrop-blur-md border-b border-white/5 p-4 rounded-t-lg">
        <div className="flex flex-col">
            <span className="text-[10px] text-slate-400 uppercase tracking-widest font-bold mb-1">Total Account Value</span>
            <div className="flex items-baseline gap-3">
                <span className="text-3xl font-mono font-bold text-white tracking-tight text-glow-cyan">
                    ${equity ? equity.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 }) : '0.00'}
                </span>
                <span className={`flex items-center text-sm font-mono font-bold ${dailyPL >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
                    {dailyPL >= 0 ? <TrendingUp size={14} className="mr-1" /> : <TrendingDown size={14} className="mr-1" />}
                    {dailyPL >= 0 ? '+' : ''}${Math.abs(dailyPL).toLocaleString(undefined, { minimumFractionDigits: 2 })}
                </span>
            </div>
        </div>
        <div className="mt-4 md:mt-0 flex gap-6">
            <div className="text-right">
                <span className="block text-[10px] text-slate-500 uppercase font-bold">Buying Power</span>
                <span className="font-mono text-cyan-400 font-bold">${buyingPower?.toLocaleString()}</span>
            </div>
            <div className="text-right">
                <span className="block text-[10px] text-slate-500 uppercase font-bold">Margin Usage</span>
                <span className="font-mono text-purple-400 font-bold">12%</span>
            </div>
        </div>
    </div>
);

/**
 * Positions Table Row with High-Density Design
 */
const PositionRow = ({ pos }) => {
    const [isExpanded, setIsExpanded] = useState(false);
    const sparkData = Array.from({ length: 10 }, (_, i) => ({ value: pos.currentPrice * (1 + (Math.random() * 0.05 - 0.025)) }));
    const isProfit = pos.pl >= 0;

    return (
        <>
            <tr
                onClick={() => setIsExpanded(!isExpanded)}
                className={`border-b border-white/5 cursor-pointer transition-all duration-100 hover:bg-white/5 active:bg-white/10 ${isExpanded ? 'bg-white/5' : ''}`}
            >
                <td className="py-2 pl-3">
                    <div className="flex items-center gap-1">
                        <span className="font-bold text-white font-mono text-sm">{pos.symbol}</span>
                    </div>
                </td>
                <td className="py-2 font-mono text-slate-300 text-xs text-right pr-4">{pos.qty}</td>
                <td className="py-2 font-mono text-slate-300 text-xs text-right pr-4">${pos.currentPrice.toFixed(2)}</td>
                <td className="py-2 hidden sm:table-cell px-4">
                    <Sparkline data={sparkData} color={isProfit ? '#34d399' : '#fb7185'} />
                </td>
                <td className="py-2 text-right pr-3">
                    <div className={`font-mono text-xs font-bold ${isProfit ? 'text-emerald-400' : 'text-rose-400'}`}>
                        {isProfit ? '+' : ''}{pos.pl.toFixed(2)}
                        <span className="ml-2 opacity-70 text-[10px]">({(pos.pl / (pos.qty * pos.avgPrice) * 100).toFixed(2)}%)</span>
                    </div>
                </td>
            </tr>
            {isExpanded && (
                <tr className="bg-black/40">
                    <td colSpan={5} className="p-3">
                        <div className="grid grid-cols-4 gap-4 text-[10px] font-mono">
                            <div className="flex flex-col"><span className="text-slate-500 uppercase">Avg Cost</span><span className="text-slate-300">${pos.avgPrice.toFixed(2)}</span></div>
                            <div className="flex flex-col"><span className="text-slate-500 uppercase">Market Value</span><span className="text-slate-300">${(pos.qty * pos.currentPrice).toFixed(2)}</span></div>
                            <div className="flex flex-col"><span className="text-slate-500 uppercase">Sentiment</span><span className="text-cyan-400">NEUTRAL</span></div>
                            <div className="flex flex-col"><span className="text-slate-500 uppercase">Risk Score</span><span className="text-amber-400">LOW</span></div>
                        </div>
                    </td>
                </tr>
            )}
        </>
    );
};

const PortfolioWidget = () => {
    const [accountData, setAccountData] = useState(null);
    const [tradeHistory, setTradeHistory] = useState([]);
    const [activeTab, setActiveTab] = useState('positions');

    useEffect(() => {
        setAccountData(brokerageService.getAccountSummary());
        setTradeHistory(brokerageService.getTradeHistory());
        const unsubscribe = brokerageService.subscribe((event) => {
            if (event.type === 'MARKET_UPDATE' || event.type === 'INIT') {
                setAccountData(event.data);
            }
            if (event.type === 'TRADE_FILL' || event.type === 'INIT') {
                setTradeHistory([...brokerageService.getTradeHistory()]);
            }
        });
        return () => unsubscribe();
    }, []);

    if (!accountData) return <div className="p-8 text-center text-slate-500 animate-pulse text-[10px] uppercase font-mono">Loading Portfolio...</div>;

    const tabs = [
        { id: 'positions', label: 'POSITIONS', icon: Briefcase },
        { id: 'activity', label: 'TAPE', icon: Clock },
        { id: 'overview', label: 'RISK', icon: AlertCircle },
    ];

    return (
        <div className="flex flex-col h-full bg-[#050505] text-white overflow-hidden">
            {/* High Density Header */}
            <div className="bg-[#111] border-b border-[#222] p-2 flex justify-between items-center text-[10px] font-mono">
                <div className="flex gap-4">
                    <div><span className="text-slate-500 mr-2">EQUITY:</span><span className="text-cyan-400 font-bold">${accountData.equity.toLocaleString(undefined, { minimumFractionDigits: 2 })}</span></div>
                    <div><span className="text-slate-500 mr-2">DAY P/L:</span><span className={`font-bold ${accountData.dailyPL >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>${accountData.dailyPL >= 0 ? '+' : ''}{accountData.dailyPL.toFixed(2)}</span></div>
                </div>
                <div className="flex gap-4">
                    <div><span className="text-slate-500 mr-2">CASH:</span><span className="text-white">${accountData.liquidity.toLocaleString(undefined, { minimumFractionDigits: 2 })}</span></div>
                </div>
            </div>

            {/* Micro Tabs */}
            <div className="flex bg-[#0a0a0a] border-b border-[#222]">
                {tabs.map(tab => (
                    <button
                        key={tab.id}
                        onClick={() => setActiveTab(tab.id)}
                        className={`px-4 py-1.5 text-[10px] font-bold tracking-tighter border-r border-[#222] transition-colors ${activeTab === tab.id ? 'bg-[#222] text-cyan-400' : 'text-slate-500 hover:bg-[#111]'}`}
                    >
                        {tab.label}
                    </button>
                ))}
            </div>

            <div className="flex-1 overflow-y-auto custom-scrollbar">
                {activeTab === 'positions' && (
                    <table className="w-full text-left border-collapse">
                        <thead className="sticky top-0 bg-[#050505] z-10 border-b border-[#222]">
                            <tr className="text-[9px] text-slate-500 uppercase font-mono">
                                <th className="py-1.5 pl-3">Asset</th>
                                <th className="py-1.5 text-right pr-4">Qty</th>
                                <th className="py-1.5 text-right pr-4">Price</th>
                                <th className="py-1.5 hidden sm:table-cell px-4">Trend</th>
                                <th className="py-1.5 text-right pr-3">P&L</th>
                            </tr>
                        </thead>
                        <tbody>
                            {accountData.positions.map(pos => <PositionRow key={pos.symbol} pos={pos} />)}
                            {accountData.positions.length === 0 && (
                                <tr><td colSpan={5} className="py-8 text-center text-slate-600 font-mono text-[10px] uppercase">No Active Exposure</td></tr>
                            )}
                        </tbody>
                    </table>
                )}

                {activeTab === 'activity' && (
                    <div className="p-2 space-y-1">
                        {tradeHistory.map(trade => (
                            <div key={trade.id} className="flex justify-between items-center bg-[#0a0a0a] p-2 border-l-2 border-[#222] text-[10px] font-mono hover:bg-[#111]">
                                <div className="flex gap-2 items-center">
                                    <span className={trade.side === 'BUY' ? 'text-emerald-400' : 'text-rose-400'}>{trade.side}</span>
                                    <span className="font-bold">{trade.symbol}</span>
                                    <span className="text-slate-500">{trade.qty} @ ${trade.price}</span>
                                </div>
                                <span className="text-slate-600">{trade.time}</span>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        </div>
    );
};

export default PortfolioWidget;
