import React, { useState, useEffect } from 'react';
import { politicsService } from '../services/politicsService';
import { Landmark, Gavel, TrendingUp, AlertTriangle, FileText, DollarSign, Activity, Eye, PieChart } from 'lucide-react';
import './PoliticalAlpha.css';
import SenatorModal from '../components/Political/SenatorModal';
import SectorImpactChart from '../components/Political/SectorImpactChart';
import NewsTicker from '../components/Political/NewsTicker';

/**
 * Political Alpha Dashboard Page
 * Theme: Capitol Hill meets Matrix (Dark Blue, Muted Gold, Data Streams)
 */
const PoliticalAlpha = () => {
    const [disclosures, setDisclosures] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedSenator, setSelectedSenator] = useState(null);

    // Mock Data for "Matrix" elements (Heatmap & Bills) since backend might not have them yet
    const [bills] = useState([
        { id: 'HR-5521', name: 'AI Regulation Act of 2026', status: 'In Committee', impact: 'HIGH', impactScore: 88, sector: 'TECH' },
        { id: 'S-229', name: 'Quantum Computing Authorization', status: 'Passed Senate', impact: 'POSITIVE', impactScore: 92, sector: 'DEFENSE' },
        { id: 'HR-104', name: 'Green Energy Subsidies Revamp', status: 'Introduced', impact: 'MIXED', impactScore: 45, sector: 'ENERGY' },
        { id: 'S-881', name: 'Digital Asset Framework', status: 'Vetoed', impact: 'NEGATIVE', impactScore: 12, sector: 'FINANCE' },
    ]);

    const [senateHeatmap] = useState(Array.from({ length: 100 }, (_, i) => ({
        id: i + 1,
        party: i % 2 === 0 ? 'R' : 'D',
        activity: Math.random() > 0.7 ? 'HIGH' : 'LOW',
        sentiment: Math.random() * 100
    })));

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                // Fallback to mock data if service fails or is empty for demo
                try {
                    const result = await politicsService.getDisclosures();
                    if (result.data && result.data.length > 0) {
                        setDisclosures(result.data);
                    } else {
                        throw new Error("No data");
                    }
                } catch (e) {
                    // Mock Disclosures for Demo purposes if backend is empty
                    setDisclosures([
                        { member: 'Nancy P.', ticker: 'NVDA', transaction: 'Purchase', amount_range: '$1M-$5M', date: '2026-01-12', sector: 'Technology' },
                        { member: 'Dan C.', ticker: 'XOM', transaction: 'Sale', amount_range: '$50k-$100k', date: '2026-01-10', sector: 'Energy' },
                        { member: 'Mitch M.', ticker: 'LLY', transaction: 'Purchase', amount_range: '$250k-$500k', date: '2026-01-08', sector: 'Healthcare' },
                        { member: 'Ro K.', ticker: 'TSLA', transaction: 'Sale', amount_range: '$15k-$50k', date: '2026-01-05', sector: 'Consumer' },
                        { member: 'Tommy T.', ticker: 'PLTR', transaction: 'Purchase', amount_range: '$100k-$250k', date: '2026-01-02', sector: 'Defense' },
                    ]);
                }
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) return (
        <div className="flex items-center justify-center h-screen bg-slate-900 text-amber-500">
            <div className="flex flex-col items-center animate-pulse">
                <Landmark size={64} className="mb-4 text-amber-400/80" />
                <h2 className="text-2xl font-mono tracking-widest">DECODING CAPITOL HILL DATA STREAMS...</h2>
            </div>
        </div>
    );

    return (
        <div className="political-alpha-container min-h-screen bg-slate-950 text-slate-200 p-8 pb-16 overflow-y-auto relative">
            {/* Header: Capitol Matrix Style */}
            <header className="mb-10 flex justify-between items-end border-b border-amber-500/30 pb-4">
                <div>
                    <div className="flex items-center gap-3 mb-2">
                        <Landmark className="text-amber-400" size={32} />
                        <h1 className="text-4xl font-bold font-display text-white tracking-tight text-shadow-gold">
                            POLITICAL <span className="text-amber-400">ALPHA</span>
                        </h1>
                    </div>
                    <p className="text-slate-400 font-mono text-sm tracking-wider">
                        CONGRESSIONAL INSIDER TRADING & LEGISLATIVE IMPACT TRACKER
                    </p>
                </div>
                <div className="flex gap-6">
                    <div className="text-right">
                        <span className="block text-xs text-amber-500/70 font-bold uppercase">Active Session</span>
                        <span className="text-xl font-mono text-white">119th Congress</span>
                    </div>
                    <div className="text-right">
                        <span className="block text-xs text-amber-500/70 font-bold uppercase">Lobbying Spend (YTD)</span>
                        <span className="text-xl font-mono text-green-400">$4.2B</span>
                    </div>
                </div>
            </header>

            <div className="grid grid-cols-12 gap-8">

                {/* Left Column: Legislative Heatmap & Bills (The "Matrix" view) */}
                <div className="col-span-12 lg:col-span-4 flex flex-col gap-8">

                    {/* Senate Sentiment Map */}
                    <div className="glass-panel-gold p-6 relative overflow-hidden">
                        <div className="flex items-center justify-between mb-4">
                            <h3 className="text-lg font-bold text-amber-200 flex items-center gap-2">
                                <Activity size={18} /> Senate Sentiment Map
                            </h3>
                            <span className="text-xs font-mono text-amber-500/50">LIVE FEED</span>
                        </div>
                        <div className="grid grid-cols-10 gap-1 h-48 content-center">
                            {senateHeatmap.map((seat) => (
                                <div
                                    key={seat.id}
                                    onClick={() => setSelectedSenator(seat)}
                                    className={`h-3 w-3 rounded-full transition-all duration-300 cursor-pointer hover:scale-150 hover:shadow-glow-gold z-10 ${seat.activity === 'HIGH'
                                        ? (seat.party === 'R' ? 'bg-red-500 shadow-glow-red' : 'bg-blue-500 shadow-glow-blue')
                                        : 'bg-slate-800 hover:bg-slate-600'
                                        }`}
                                    title={`Seat ${seat.id} - ${seat.party}`}
                                ></div>
                            ))}
                        </div>
                        <div className="mt-4 flex justify-between text-xs text-slate-400 font-mono">
                            <span className="flex items-center gap-1"><div className="w-2 h-2 bg-red-500 rounded-full"></div> GOP Activity</span>
                            <span className="flex items-center gap-1"><div className="w-2 h-2 bg-blue-500 rounded-full"></div> DEM Activity</span>
                        </div>
                    </div>

                    {/* Sector Impact Chart */}
                    <div className="glass-panel-gold p-6 h-64">
                        <SectorImpactChart />
                    </div>

                    {/* Active Legislation Tracker */}
                    <div className="glass-panel-gold p-6 flex-1">
                        <div className="flex items-center justify-between mb-6">
                            <h3 className="text-lg font-bold text-amber-200 flex items-center gap-2">
                                <Gavel size={18} /> Legislative Watchlist
                            </h3>
                        </div>
                        <div className="space-y-4">
                            {bills.map(bill => (
                                <div key={bill.id} className="bill-item p-4 bg-slate-900/40 border-l-4 border-slate-700 hover:border-amber-400 transition-all duration-200 hover:scale-[1.02] hover:bg-slate-800/60 shadow-lg cursor-pointer group">
                                    <div className="flex justify-between items-start mb-2">
                                        <span className="font-mono text-xs text-amber-500/80">{bill.id}</span>
                                        <span className={`text-xs px-2 py-0.5 rounded font-bold ${bill.impact === 'HIGH' || bill.impact === 'POSITIVE' ? 'bg-green-900/30 text-green-400' :
                                            bill.impact === 'NEGATIVE' ? 'bg-red-900/30 text-red-400' : 'bg-slate-700 text-slate-300'
                                            }`}>{bill.impact} IMPACT</span>
                                    </div>
                                    <h4 className="text-sm font-bold text-slate-200 group-hover:text-amber-100 mb-1">{bill.name}</h4>
                                    <div className="flex justify-between items-center text-xs text-slate-500 mt-2">
                                        <span className="italic">{bill.status}</span>
                                        <span className="font-mono">{bill.sector}</span>
                                    </div>
                                    <div className="w-full bg-slate-800 h-1 mt-3 rounded-full overflow-hidden">
                                        <div className="h-full bg-amber-500/50" style={{ width: `${bill.impactScore}%` }}></div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    </div>
                </div>

                {/* Right Column: Disclosure Feed (The "Data Stream") */}
                <div className="col-span-12 lg:col-span-8">
                    <div className="glass-panel-gold p-6 min-h-[600px]">
                        <div className="flex items-center justify-between mb-6">
                            <h3 className="text-lg font-bold text-amber-200 flex items-center gap-2">
                                <Eye size={18} /> Live Disclosure Feed
                            </h3>
                            <button className="text-xs bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 px-3 py-1 rounded transition-colors border border-amber-500/30">
                                EXPORT REPORT
                            </button>
                        </div>

                        {/* Custom Table Layout for "Premium" feel */}
                        <div className="overflow-x-auto">
                            <table className="w-full text-left border-collapse">
                                <thead>
                                    <tr className="border-b border-slate-700 text-xs text-slate-500 uppercase tracking-wider font-mono">
                                        <th className="p-4 font-normal">Congress Member</th>
                                        <th className="p-4 font-normal">Asset / Ticker</th>
                                        <th className="p-4 font-normal">Transaction</th>
                                        <th className="p-4 font-normal">Value Range</th>
                                        <th className="p-4 font-normal">Filing Date</th>
                                        <th className="p-4 font-normal text-right">Action</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-slate-800/50">
                                    {disclosures.map((d, index) => (
                                        <tr key={index} className="group hover:bg-amber-500/5 transition-all duration-200 cursor-default border-l-4 border-l-transparent hover:border-l-amber-500/50">
                                            <td className="p-4">
                                                <div className="font-bold text-slate-200 group-hover:text-amber-100">{d.member}</div>
                                                <div className="text-xs text-slate-500">{d.sector || 'Unknown Sector'}</div>
                                            </td>
                                            <td className="p-4">
                                                <div className="font-mono text-amber-400 font-bold">{d.ticker}</div>
                                                <div className="text-xs text-slate-600">Common Stock</div>
                                            </td>
                                            <td className="p-4">
                                                <span className={`inline-flex items-center gap-1 px-2 py-1 rounded text-xs font-bold ${d.transaction === 'Purchase' || d.transaction.includes('Buy')
                                                    ? 'bg-green-500/10 text-green-400 border border-green-500/20'
                                                    : 'bg-red-500/10 text-red-400 border border-red-500/20'
                                                    }`}>
                                                    {d.transaction === 'Purchase' ? <TrendingUp size={12} /> : <TrendingUp size={12} className="rotate-180" />}
                                                    {d.transaction}
                                                </span>
                                            </td>
                                            <td className="p-4 font-mono text-sm text-slate-300">
                                                {d.amount_range}
                                            </td>
                                            <td className="p-4 text-sm text-slate-400">
                                                {d.date}
                                            </td>
                                            <td className="p-4 text-right">
                                                <button
                                                    onClick={() => alert(`Analyzing ${d.ticker} correlation...`)}
                                                    className="p-2 hover:bg-amber-500/20 rounded-full text-slate-500 hover:text-amber-400 transition-colors"
                                                    title="Analyze Correlation"
                                                >
                                                    <Activity size={16} />
                                                </button>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>

            {/* Premium Features */}
            <NewsTicker />
            <SenatorModal senator={selectedSenator} onClose={() => setSelectedSenator(null)} />
        </div>
    );
};

export default PoliticalAlpha;
