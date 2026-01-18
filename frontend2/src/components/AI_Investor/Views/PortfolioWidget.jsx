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
 * Positions Table Row with Accordion
 */
const PositionRow = ({ pos }) => {
    const [isExpanded, setIsExpanded] = useState(false);

    // Mock sparkline data
    const sparkData = Array.from({ length: 10 }, (_, i) => ({ value: pos.currentPrice * (1 + (Math.random() * 0.05 - 0.025)) }));
    const isProfit = pos.pl >= 0;

    return (
        <>
            <tr
                onClick={() => setIsExpanded(!isExpanded)}
                className={`border-b border-white/5 cursor-pointer transition-all duration-200 border-l-4 ${isExpanded ? 'bg-white/5 border-l-cyan-500 shadow-[inset_0_0_20px_rgba(6,182,212,0.1)]' : 'hover:bg-white/5 border-l-transparent hover:border-l-cyan-500/50'}`}
            >
                <td className="py-3 pl-4">
                    <div className="flex items-center gap-2">
                        {isExpanded ? <ChevronUp size={14} className="text-cyan-400" /> : <ChevronDown size={14} className="text-slate-500" />}
                        <span className="font-bold text-white font-mono group-hover:text-cyan-400 transition-colors">{pos.symbol}</span>
                    </div>
                </td>
                <td className="py-3 font-mono text-slate-300">{pos.qty}</td>
                <td className="py-3 font-mono text-slate-300 py-3">${pos.currentPrice.toFixed(2)}</td>
                <td className="py-3 hidden sm:table-cell">
                    <Sparkline data={sparkData} color={isProfit ? '#34d399' : '#fb7185'} />
                </td>
                <td className="py-3 text-right pr-4">
                    <div className={`inline-flex flex-col items-end ${isProfit ? 'text-emerald-400' : 'text-rose-400'}`}>
                        <span className="font-bold font-mono">{isProfit ? '+' : ''}{pos.pl.toFixed(2)}</span>
                        <span className="text-[10px] opacity-70">{(pos.pl / (pos.qty * pos.avgPrice) * 100).toFixed(2)}%</span>
                    </div>
                </td>
            </tr>
            {isExpanded && (
                <tr className="bg-black/20">
                    <td colSpan={5} className="p-4">
                        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs font-mono">
                            <div className="flex flex-col gap-1">
                                <span className="text-slate-500 uppercase text-[10px]">Delta</span>
                                <span className="text-slate-300">0.85</span>
                            </div>
                            <div className="flex flex-col gap-1">
                                <span className="text-slate-500 uppercase text-[10px]">Gamma</span>
                                <span className="text-slate-300">0.12</span>
                            </div>
                            <div className="flex flex-col gap-1">
                                <span className="text-slate-500 uppercase text-[10px]">Entry Reason</span>
                                <span className="text-cyan-400">MACD Crossover (15m)</span>
                            </div>
                            <div className="flex flex-col gap-1">
                                <span className="text-slate-500 uppercase text-[10px]">Conviction</span>
                                <span className="text-emerald-400 font-bold">HIGH</span>
                            </div>
                        </div>
                    </td>
                </tr>
            )}
        </>
    );
};

/**
 * Activity Log Item
 */
const ActivityItem = ({ trade }) => (
    <div className="relative pl-6 pb-6 border-l border-white/10 last:pb-0">
        <div className={`absolute top-0 left-[-5px] w-2.5 h-2.5 rounded-full ${trade.side === 'BUY' ? 'bg-emerald-500' : 'bg-rose-500'} ring-4 ring-black`} />
        <div className="flex flex-col gap-1 bg-white/5 p-3 rounded-lg border border-white/5 hover:border-cyan-500/30 transition-all hover:scale-[1.02] hover:shadow-lg">
            <div className="flex justify-between items-start">
                <div className="flex items-center gap-2">
                    <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded uppercase ${trade.side === 'BUY' ? 'bg-emerald-500/20 text-emerald-400' : 'bg-rose-500/20 text-rose-400'}`}>
                        {trade.side}
                    </span>
                    <span className="font-bold text-white font-mono">{trade.symbol}</span>
                </div>
                <span className="text-[10px] text-slate-500 font-mono">{trade.time}</span>
            </div>

            <div className="flex justify-between items-center text-xs mt-1">
                <span className="text-slate-300 font-mono">{trade.qty} @ ${trade.price}</span>
                <span className="text-slate-500 font-mono font-bold">${trade.total}</span>
            </div>

            <p className="text-[10px] text-slate-400 mt-2 border-t border-white/5 pt-2 flex items-center gap-1">
                <Zap size={10} className="text-yellow-500" />
                {trade.reason}
            </p>
        </div>
    </div>
);

/**
 * Main Widget Component
 */
const PortfolioWidget = () => {
    const [accountData, setAccountData] = useState(null);
    const [tradeHistory, setTradeHistory] = useState([]);
    const [activeTab, setActiveTab] = useState('positions'); // 'overview', 'positions', 'activity'

    useEffect(() => {
        // Initial data
        setAccountData(brokerageService.getAccountSummary());
        setTradeHistory(brokerageService.getTradeHistory());

        // Subscribe to updates
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

    if (!accountData) return <div className="p-8 text-center text-slate-500 animate-pulse uppercase tracking-widest text-xs">Initializing Portfolio Feed...</div>;

    const tabs = [
        { id: 'overview', label: 'Overview', icon: AlertCircle },
        { id: 'positions', label: 'Positions', icon: Briefcase },
        { id: 'activity', label: 'Activity Log', icon: Clock },
    ];

    return (
        <div className="flex flex-col h-full bg-[#0a0a0a]/80 backdrop-blur-xl rounded-xl border border-white/10 overflow-hidden shadow-2xl">
            <GlobalHeader
                equity={accountData.equity}
                dailyPL={accountData.dailyPL}
                buyingPower={accountData.buyingPower}
            />

            {/* Tab Navigation */}
            <div className="flex border-b border-white/5 bg-black/20">
                {tabs.map(tab => {
                    const Icon = tab.icon;
                    return (
                        <button
                            key={tab.id}
                            onClick={() => setActiveTab(tab.id)}
                            className={`flex items-center gap-2 px-6 py-3 text-xs font-bold uppercase tracking-wider transition-all relative ${activeTab === tab.id
                                ? 'text-white'
                                : 'text-slate-500 hover:text-slate-300 hover:bg-white/5'
                                }`}
                        >
                            <Icon size={14} />
                            {tab.label}
                            {activeTab === tab.id && (
                                <div className="absolute bottom-0 left-0 w-full h-[2px] bg-cyan-500 shadow-[0_0_10px_rgba(6,182,212,0.5)]"></div>
                            )}
                        </button>
                    );
                })}
            </div>

            {/* Main Content Area */}
            <div className="flex-1 overflow-y-auto custom-scrollbar p-0 bg-transparent relative">

                {/* POSITIONS TAB */}
                {activeTab === 'positions' && (
                    <div className="w-full">
                        <table className="w-full text-left border-collapse">
                            <thead className="sticky top-0 bg-[#0a0a0a] z-10 border-b border-white/10 shadow-lg">
                                <tr>
                                    <th className="py-3 pl-4 text-[10px] text-slate-500 uppercase tracking-wider font-bold">Asset</th>
                                    <th className="py-3 text-[10px] text-slate-500 uppercase tracking-wider font-bold">Qty</th>
                                    <th className="py-3 text-[10px] text-slate-500 uppercase tracking-wider font-bold">Price</th>
                                    <th className="py-3 hidden sm:table-cell text-[10px] text-slate-500 uppercase tracking-wider font-bold">24h Trend</th>
                                    <th className="py-3 pr-4 text-right text-[10px] text-slate-500 uppercase tracking-wider font-bold">P&L</th>
                                </tr>
                            </thead>
                            <tbody>
                                {accountData.positions.length > 0 ? (
                                    accountData.positions.map(pos => (
                                        <PositionRow key={pos.symbol} pos={pos} />
                                    ))
                                ) : (
                                    <tr>
                                        <td colSpan={5} className="py-12 text-center text-slate-600 italic">
                                            No open positions. Scanning market...
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                )}

                {/* ACTIVITY LOG TAB */}
                {activeTab === 'activity' && (
                    <div className="p-6">
                        <div className="max-w-xl mx-auto">
                            {tradeHistory.length > 0 ? (
                                tradeHistory.map(trade => (
                                    <ActivityItem key={trade.id} trade={trade} />
                                ))
                            ) : (
                                <div className="text-center text-slate-600 italic py-10">
                                    No recent activity recorded.
                                </div>
                            )}
                        </div>
                    </div>
                )}

                {/* OVERVIEW TAB (Placeholder for now, could act as charts) */}
                {activeTab === 'overview' && (
                    <div className="p-6 flex flex-col items-center justify-center h-full text-center">
                        <Wallet size={48} className="text-slate-700 mb-4" />
                        <h3 className="text-slate-400 font-bold uppercase tracking-widest text-sm mb-2">Portfolio Analytics</h3>
                        <p className="text-slate-600 text-xs max-w-md">
                            Detailed performance metrics, Sharpe ratio, and sector allocation breakdown will appear here.
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default PortfolioWidget;
