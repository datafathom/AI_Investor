import React, { useState, useEffect } from 'react';
import { politicsService } from '../services/politicsService';
import { Landmark, Gavel, TrendingUp, AlertTriangle, FileText, DollarSign, Activity, Eye, PieChart, Info } from 'lucide-react';
import { Responsive, WidthProvider } from 'react-grid-layout';
import './PoliticalAlpha.css';
import SenatorModal from '../components/Political/SenatorModal';
import SectorImpactChart from '../components/Political/SectorImpactChart';
import NewsTicker from '../components/Political/NewsTicker';
import PageHeader from '../components/Navigation/PageHeader';

const ResponsiveGridLayout = WidthProvider(Responsive);
const STORAGE_KEY = 'political_alpha_layout_v15'; // Incremented for fresh layout

const DEFAULT_LAYOUTS = {
    lg: [
        { i: 'summary', x: 0, y: 0, w: 12, h: 3 },
        { i: 'sentiment', x: 0, y: 3, w: 12, h: 8 },
        { i: 'impact', x: 0, y: 11, w: 12, h: 6 },
        { i: 'watchlist', x: 0, y: 17, w: 12, h: 10 },
        { i: 'feed', x: 0, y: 27, w: 12, h: 16 },
        { i: 'news-ticker', x: 0, y: 43, w: 12, h: 1.5 }
    ],
    md: [
        { i: 'summary', x: 0, y: 0, w: 10, h: 3 },
        { i: 'sentiment', x: 0, y: 3, w: 10, h: 8 },
        { i: 'impact', x: 0, y: 11, w: 10, h: 6 },
        { i: 'watchlist', x: 0, y: 17, w: 10, h: 10 },
        { i: 'feed', x: 0, y: 27, w: 10, h: 16 },
        { i: 'news-ticker', x: 0, y: 43, w: 10, h: 1.5 }
    ],
    sm: [
        { i: 'summary', x: 0, y: 0, w: 6, h: 4 },
        { i: 'sentiment', x: 0, y: 4, w: 6, h: 8 },
        { i: 'impact', x: 0, y: 12, w: 6, h: 6 },
        { i: 'watchlist', x: 0, y: 18, w: 6, h: 10 },
        { i: 'feed', x: 0, y: 28, w: 6, h: 24 },
        { i: 'news-ticker', x: 0, y: 52, w: 6, h: 1.5 }
    ]
};

const MOCK_CHAMBER_DATA = [
    { 
        name: 'AI & TECHNOLOGY', 
        sentiment: 78, 
        members: [
            { party: 'D', activity: 'HIGH' }, { party: 'R', activity: 'HIGH' }, { party: 'D', activity: 'LOW' },
            { party: 'R', activity: 'LOW' }, { party: 'D', activity: 'HIGH' }, { party: 'D', activity: 'HIGH' },
            { party: 'R', activity: 'HIGH' }, { party: 'R', activity: 'LOW' }, { party: 'D', activity: 'LOW' },
            { party: 'D', activity: 'HIGH' }
        ]
    },
    { 
        name: 'FINANCE & BANKING', 
        sentiment: 42, 
        members: [
            { party: 'R', activity: 'HIGH' }, { party: 'R', activity: 'HIGH' }, { party: 'D', activity: 'LOW' },
            { party: 'R', activity: 'LOW' }, { party: 'R', activity: 'HIGH' }, { party: 'D', activity: 'LOW' },
            { party: 'D', activity: 'HIGH' }, { party: 'R', activity: 'HIGH' }, { party: 'R', activity: 'LOW' },
            { party: 'D', activity: 'HIGH' }
        ]
    },
    { 
        name: 'ENERGY & INFRA', 
        sentiment: 64, 
        members: [
            { party: 'D', activity: 'HIGH' }, { party: 'D', activity: 'LOW' }, { party: 'R', activity: 'HIGH' },
            { party: 'R', activity: 'HIGH' }, { party: 'D', activity: 'HIGH' }, { party: 'R', activity: 'LOW' },
            { party: 'D', activity: 'HIGH' }, { party: 'D', activity: 'LOW' }, { party: 'R', activity: 'HIGH' },
            { party: 'D', activity: 'HIGH' }
        ]
    },
    { 
        name: 'ARMED SERVICES', 
        sentiment: 92, 
        members: [
            { party: 'R', activity: 'HIGH' }, { party: 'D', activity: 'HIGH' }, { party: 'R', activity: 'HIGH' },
            { party: 'R', activity: 'HIGH' }, { party: 'D', activity: 'HIGH' }, { party: 'R', activity: 'HIGH' },
            { party: 'D', activity: 'HIGH' }, { party: 'R', activity: 'HIGH' }, { party: 'D', activity: 'LOW' },
            { party: 'R', activity: 'HIGH' }
        ]
    }
];

// Standardized Widget Header Component
const WidgetHeader = ({ icon: Icon, title, subtitle }) => (
    <div className="flex items-center justify-between mb-6 pb-4 border-b border-white/10">
        <div className="flex flex-col">
            <h3 className="text-lg font-bold text-amber-100 flex items-center gap-3">
                <Icon size={20} className="text-amber-400" /> {title}
            </h3>
            {subtitle && <span className="text-[10px] font-mono text-slate-500 mt-1 tracking-[0.2em] uppercase pl-8">{subtitle}</span>}
        </div>
        {/* Placeholder for potential right-side actions */}
    </div>
);

const PoliticalAlpha = () => {
    // ... (state logic remains unchanged) ...
    const [disclosures, setDisclosures] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedSenator, setSelectedSenator] = useState(null);
    const [sortConfig, setSortConfig] = useState({ key: 'date', direction: 'desc' });

    // Column Width State
    const [colWidths, setColWidths] = useState({
        member: 200,
        sector: 150,
        ticker: 100,
        transaction: 150,
        amount_range: 150,
        date: 120
    });

    // Resize Ref
    const resizingRef = React.useRef(null);

    // Persisted Layout State
    const [layouts, setLayouts] = useState(() => {
        try {
            const saved = localStorage.getItem(STORAGE_KEY);
            return saved ? JSON.parse(saved) : DEFAULT_LAYOUTS;
        } catch (e) {
            console.warn("Failed to load political layout:", e);
            return DEFAULT_LAYOUTS;
        }
    });

    const onLayoutChange = (current, allLayouts) => {
        setLayouts(allLayouts);
        localStorage.setItem(STORAGE_KEY, JSON.stringify(allLayouts));
    };

    const handleSort = (key) => {
        console.log(`Sorting by ${key}`);
        let direction = 'asc';
        if (sortConfig.key === key && sortConfig.direction === 'asc') {
            direction = 'desc';
        }
        setSortConfig({ key, direction });
    };

    const sortedDisclosures = [...disclosures].sort((a, b) => {
        if (!sortConfig.key) return 0;
        const aVal = a[sortConfig.key] || '';
        const bVal = b[sortConfig.key] || '';
        if (aVal < bVal) return sortConfig.direction === 'asc' ? -1 : 1;
        if (aVal > bVal) return sortConfig.direction === 'asc' ? 1 : -1;
        return 0;
    });

    // Resize Logic
    const startResize = (e, key) => {
        e.preventDefault();
        e.stopPropagation();
        resizingRef.current = { key, startX: e.clientX, startWidth: colWidths[key] };
        document.addEventListener('mousemove', handleMouseMove);
        document.addEventListener('mouseup', handleMouseUp);
        document.body.style.cursor = 'col-resize';
    };

    const handleMouseMove = (e) => {
        if (!resizingRef.current) return;
        const { key, startX, startWidth } = resizingRef.current;
        const diff = e.clientX - startX;
        setColWidths(prev => ({
            ...prev,
            [key]: Math.max(50, startWidth + diff) // Min width 50px
        }));
    };

    const handleMouseUp = () => {
        resizingRef.current = null;
        document.removeEventListener('mousemove', handleMouseMove);
        document.removeEventListener('mouseup', handleMouseUp);
        document.body.style.cursor = '';
    };

    // PDF Export Logic
    const handleExport = () => {
        const printWindow = window.open('', '', 'height=600,width=800');
        printWindow.document.write('<html><head><title>Political Alpha Disclosure Report</title>');
        printWindow.document.write('<style>table { width: 100%; border-collapse: collapse; } th, td { border: 1px solid black; padding: 8px; text-align: center; } th { background-color: #2563eb; color: white; }</style>');
        printWindow.document.write('</head><body>');
        printWindow.document.write('<h1>Live Disclosure Feed Report</h1>');
        // Extract table HTML simply by ID or reconstructing
        // Reconstructing for cleanliness
        let tableHtml = '<table><thead><tr>';
        Object.keys(colWidths).forEach(key => {
            tableHtml += `<th>${key.toUpperCase().replace('_', ' ')}</th>`;
        });
        tableHtml += '</tr></thead><tbody>';
        sortedDisclosures.forEach(d => {
            tableHtml += '<tr>';
            tableHtml += `<td>${d.member}</td>`;
            tableHtml += `<td>${d.sector}</td>`;
            tableHtml += `<td>${d.ticker}</td>`;
            tableHtml += `<td>${d.transaction}</td>`;
            tableHtml += `<td>${d.amount_range}</td>`;
            tableHtml += `<td>${d.date}</td>`;
            tableHtml += '</tr>';
        });
        tableHtml += '</tbody></table>';
        printWindow.document.write(tableHtml);
        printWindow.document.write('</body></html>');
        printWindow.document.close();
        printWindow.print();
    };

    const [bills] = useState([
        { id: 'HR-5521', name: 'AI Regulation Act of 2026', status: 'In Committee', impact: 'HIGH', impactScore: 88, sector: 'TECH' },
        { id: 'S-229', name: 'Quantum Computing Authorization', status: 'Passed Senate', impact: 'POSITIVE', impactScore: 92, sector: 'DEFENSE' },
        { id: 'HR-104', name: 'Green Energy Subsidies Revamp', status: 'Introduced', impact: 'MIXED', impactScore: 45, sector: 'ENERGY' },
        { id: 'S-881', name: 'Digital Asset Framework', status: 'Vetoed', impact: 'NEGATIVE', impactScore: 12, sector: 'FINANCE' },
    ]);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                try {
                    const result = await politicsService.getDisclosures();
                    if (result.data && result.data.length > 0) {
                        setDisclosures(result.data);
                    } else {
                        throw new Error("No data");
                    }
                } catch (e) {
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
        return () => {
            // Cleanup generic listeners if component unmounts mid-drag
            document.removeEventListener('mousemove', handleMouseMove);
            document.removeEventListener('mouseup', handleMouseUp);
        };
    }, []);

    if (loading) return (
        <div className="flex items-center justify-center p-20 text-amber-500">
            <div className="flex flex-col items-center animate-pulse">
                <Landmark size={64} className="mb-4 text-amber-400/80" />
                <h2 className="text-2xl font-mono tracking-widest">DECODING CAPITOL HILL DATA STREAMS...</h2>
            </div>
        </div>
    );

    return (
        <div className="full-bleed-page political-alpha-page">
            <PageHeader 
                icon={<Landmark />}
                title={<>POLITICAL <span className="text-amber-400">ALPHA</span></>}
            />

            <div className="scrollable-content-wrapper">
                <ResponsiveGridLayout
                    className="layout"
                    layouts={layouts}
                    onLayoutChange={onLayoutChange}
                    breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
                    cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
                    rowHeight={50}
                    isDraggable={true}
                    isResizable={true}
                    margin={[20, 20]}
                >
                    {/* 0. Political Summary Widget */}
                    <div key="summary" className="glass-panel-gold flex items-center justify-between px-10 py-6">
                        <div className="flex flex-col justify-center">
                             <h3 className="text-amber-500/80 font-mono text-xs tracking-[0.2em] mb-2 uppercase">
                                 CONGRESSIONAL INSIDER TRADING & LEGISLATIVE IMPACT TRACKER
                             </h3>
                             <div className="flex gap-12">
                                 <div>
                                     <span className="block text-[9px] text-slate-500 font-bold uppercase mb-1">Active Session</span>
                                     <span className="text-xl font-mono text-white tracking-tight">119th Congress</span>
                                 </div>
                                 <div>
                                     <span className="block text-[9px] text-slate-500 font-bold uppercase mb-1">Lobbying Spend (YTD)</span>
                                     <span className="text-xl font-mono text-green-400 tracking-tight">$4.2B</span>
                                 </div>
                             </div>
                        </div>
                    </div>

                    {/* 1. Senate Sentiment Map */}
                    <div key="sentiment" className="glass-panel-gold">
                       <div className="p-6 h-full flex flex-col overflow-y-auto scrollbar-gold">
                            <WidgetHeader icon={Activity} title="Senate Sentiment Map" subtitle="Institutional Chamber Pulse" />
                            
                            <div className="flex-1 grid grid-cols-1 xl:grid-cols-2 gap-6 items-start">
                                {MOCK_CHAMBER_DATA.map((committee) => (
                                    <div key={committee.name} className="group bg-slate-900/60 p-5 rounded-2xl border border-white/5 hover:border-amber-400/40 transition-all duration-500 hover:bg-slate-900/80 shadow-xl">
                                        <div className="flex justify-between items-end mb-5">
                                            <div className="flex flex-col">
                                                <span className="text-[9px] font-bold text-amber-500/60 font-mono tracking-widest mb-1 uppercase">Legislative Group</span>
                                                <h4 className="text-sm font-black text-white group-hover:text-amber-100 tracking-tight transition-colors">
                                                    {committee.name}
                                                </h4>
                                            </div>
                                            <div className="flex flex-col items-end">
                                                <span style={{ 
                                                    color: committee.sentiment > 50 ? '#10b981' : '#ef4444', 
                                                    fontSize: '14px', 
                                                    fontWeight: '900',
                                                    letterSpacing: '-0.02em',
                                                    lineHeight: '1'
                                                }}>
                                                    {committee.sentiment}% {committee.sentiment > 50 ? 'BULLISH' : 'BEARISH'}
                                                </span>
                                                <div className="w-24 h-1.5 bg-slate-800 rounded-full mt-2 overflow-hidden border border-white/5">
                                                    <div 
                                                        className="h-full transition-all duration-1000 ease-out" 
                                                        style={{ 
                                                            width: `${committee.sentiment}%`, 
                                                            backgroundColor: committee.sentiment > 50 ? '#10b981' : '#ef4444',
                                                            boxShadow: `0 0 15px ${committee.sentiment > 50 ? '#10b98188' : '#ef444488'}`
                                                        }}
                                                    />
                                                </div>
                                            </div>
                                        </div>
                                        
                                        <div className="flex flex-wrap gap-2.5 justify-start p-3 bg-black/40 rounded-xl border border-white/5 shadow-inner">
                                            {committee.members.map((m, idx) => (
                                                <div 
                                                    key={idx}
                                                    className="h-4.5 w-4.5 rounded-sm transition-all duration-300 hover:scale-[2.0] hover:z-50 cursor-crosshair border border-black/30"
                                                    style={{
                                                        backgroundColor: m.activity === 'HIGH' 
                                                            ? (m.party === 'R' ? '#f43f5e' : '#3b82f6') 
                                                            : '#334155',
                                                        boxShadow: m.activity === 'HIGH'
                                                            ? `0 0 8px ${m.party === 'R' ? 'rgba(244, 63, 94, 0.4)' : 'rgba(59, 130, 246, 0.4)'}`
                                                            : 'none',
                                                        opacity: m.activity === 'HIGH' ? 1 : 0.6
                                                    }}
                                                    title={`${committee.name} Senator | Party: ${m.party}`}
                                                ></div>
                                            ))}
                                        </div>
                                    </div>
                                ))}
                            </div>

                            <div className="mt-8 pt-6 border-t border-white/10 flex flex-wrap justify-center gap-10 text-[11px] text-slate-500 font-mono font-bold uppercase tracking-tighter">
                                <span className="flex items-center gap-3 transition-colors hover:text-red-400 group cursor-default">
                                    <div className="w-3 h-3 bg-red-500 rounded-sm shadow-[0_0_8px_#ef4444] group-hover:scale-125 transition-transform"></div> 
                                    GOP ACTIVE
                                </span>
                                <span className="flex items-center gap-3 transition-colors hover:text-blue-400 group cursor-default">
                                    <div className="w-3 h-3 bg-blue-500 rounded-sm shadow-[0_0_8px_#3b82f6] group-hover:scale-125 transition-transform"></div> 
                                    DEM ACTIVE
                                </span>
                                <span className="flex items-center gap-3 transition-colors hover:text-slate-300 group cursor-default">
                                    <div className="w-3 h-3 bg-slate-600 rounded-sm group-hover:scale-125 transition-transform"></div> 
                                    NEUTRAL / INACTIVE
                                </span>
                            </div>
                       </div>
                    </div>

                    {/* 2. Sector Impact Chart */}
                    <div key="impact" className="glass-panel-gold overflow-hidden">
                        <div className="p-6 h-full flex flex-col">
                            <WidgetHeader icon={PieChart} title="Sector Impact Profile" />
                            <div className="flex-1 min-h-0">
                                <SectorImpactChart />
                            </div>
                        </div>
                    </div>

                    {/* 3. Active Legislation Tracker */}
                    <div key="watchlist" className="glass-panel-gold overflow-hidden">
                        <div className="p-6 h-full flex flex-col">
                            <WidgetHeader icon={Gavel} title="Legislative Watchlist" />
                            <div className="flex-1 overflow-y-auto pr-2 scrollbar-gold grid grid-cols-1 xl:grid-cols-2 gap-4 items-start">
                                {bills.map(bill => (
                                    <div key={bill.id} className="bill-item p-5 bg-slate-900/60 border border-white/5 rounded-2xl hover:border-amber-400/30 transition-all duration-300 hover:bg-slate-900/80 shadow-xl group cursor-pointer">
                                        <div className="flex justify-between items-start mb-4">
                                            <div className="flex flex-col">
                                                <span className="font-mono text-[10px] text-amber-500/60 mb-1 tracking-tighter">{bill.id}</span>
                                                <h4 className="text-sm font-black text-white group-hover:text-amber-100 leading-tight transition-colors">{bill.name}</h4>
                                            </div>
                                            <span className={`text-[9px] px-2.5 py-1 rounded-full font-black tracking-tighter border ${
                                                bill.impact === 'HIGH' || bill.impact === 'POSITIVE' 
                                                ? 'bg-green-500/10 text-green-400 border-green-500/20' 
                                                : bill.impact === 'NEGATIVE' 
                                                ? 'bg-red-500/10 text-red-400 border-red-500/20' 
                                                : 'bg-slate-700/30 text-slate-300 border-slate-700/50'
                                            }`}>
                                                {bill.impact} IMPACT
                                            </span>
                                        </div>

                                        <div className="grid grid-cols-2 gap-4 mb-4 pt-4 border-t border-white/5">
                                            <div className="flex flex-col">
                                                <span style={{ color: '#64748b', fontWeight: '900', fontSize: '8px' }} className="uppercase tracking-[0.1em] mb-1">STATUS:</span>
                                                <span style={{ color: '#ffffff', fontStyle: 'italic', fontSize: '11px' }} className="font-mono truncate">{bill.status}</span>
                                            </div>
                                            <div className="flex flex-col border-l border-white/5 pl-4">
                                                <span style={{ color: '#64748b', fontWeight: '900', fontSize: '8px' }} className="uppercase tracking-[0.1em] mb-1">SECTOR:</span>
                                                <span style={{ color: '#fbbf24', fontWeight: 'bold', fontSize: '11px' }} className="font-mono uppercase">{bill.sector}</span>
                                            </div>
                                        </div>

                                        <div className="space-y-2 pt-2">
                                            <div className="flex justify-between items-center text-[10px] font-mono">
                                                <span style={{ color: '#64748b', fontWeight: '900' }} className="tracking-tighter">PROBABILITY:</span>
                                                <span style={{ color: '#fbbf24', backgroundColor: 'rgba(245, 158, 11, 0.15)' }} className="font-black px-2 py-0.5 rounded">{bill.impactScore}%</span>
                                            </div>
                                            <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden border border-white/5 shadow-inner">
                                                <div className="h-full bg-amber-500/60 shadow-[0_0_12px_rgba(245,158,11,0.4)] transition-all duration-1000" style={{ width: `${bill.impactScore}%` }}></div>
                                            </div>
                                        </div>
                                    </div>
                                ))}
                            </div>
                        </div>
                    </div>

                    {/* 4. Right Column: Disclosure Feed (The "Data Stream") */}
                    <div key="feed" className="glass-panel-gold overflow-hidden flex flex-col h-full w-full">
                        <div className="p-6 h-full flex flex-col w-full">
                            <div className="flex items-center justify-between mb-6">
                                <h3 className="text-lg font-bold text-amber-200 flex items-center gap-2">
                                    <Eye size={18} /> Live Disclosure Feed
                                </h3>
                                <button 
                                    onClick={handleExport}
                                    className="text-xs bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 px-3 py-1 rounded transition-colors border border-amber-500/30"
                                >
                                    EXPORT REPORT
                                </button>
                            </div>

                            <div className="flex-1 overflow-visible rounded-lg border-2 border-slate-600 bg-black/20 shadow-inner w-full" style={{ display: 'flex', flexDirection: 'column' }}>
                                <div className="w-full relative overflow-y-auto scrollbar-gold" style={{ flex: 1 }}>
                                    <table className="w-full table-fixed border-collapse" style={{ width: '100%', minWidth: '100%' }}>
                                        
                                        <colgroup>
                                            <col style={{ width: colWidths.member }} />
                                            <col style={{ width: colWidths.sector }} />
                                            <col style={{ width: colWidths.ticker }} />
                                            <col style={{ width: colWidths.transaction }} />
                                            <col style={{ width: colWidths.amount_range }} />
                                            <col style={{ width: colWidths.date }} />
                                            <col style={{ width: 100 }} /> 
                                        </colgroup>

                                        <thead className="sticky top-0 z-50 shadow-xl" style={{ backgroundColor: '#2563eb', borderBottom: '4px solid #1e40af' }}>
                                            <tr className="text-[11px] text-white uppercase tracking-[0.1em] font-mono font-black">
                                                {[
                                                    { key: 'member', label: 'Member' },
                                                    { key: 'sector', label: 'Sector' },
                                                    { key: 'ticker', label: 'Asset' },
                                                    { key: 'transaction', label: 'Trade' },
                                                    { key: 'amount_range', label: 'Value' },
                                                    { key: 'date', label: 'Date' }
                                                ].map(col => (
                                                    <th 
                                                        key={col.key}
                                                        className="p-0 select-none cursor-pointer relative hover:bg-blue-500 transition-colors nodrag"
                                                        style={{ 
                                                            cursor: 'pointer', 
                                                            borderRight: '2px solid #94a3b8', 
                                                            borderBottom: '2px solid #94a3b8',
                                                            backgroundColor: '#2563eb',
                                                            textAlign: 'center'
                                                        }}
                                                        onMouseDown={(e) => {
                                                            e.stopPropagation();
                                                            e.preventDefault(); 
                                                            handleSort(col.key);
                                                        }}
                                                    >
                                                        <div className="flex items-center justify-center w-full h-full p-4 pointer-events-none nodrag relative">
                                                            <span style={{ textDecoration: 'underline', textUnderlineOffset: '4px' }}>{col.label}</span>
                                                            <span className="text-white ml-2">
                                                                {sortConfig.key === col.key 
                                                                    ? (sortConfig.direction === 'asc' ? '▲' : '▼') 
                                                                    : '↕'}
                                                            </span>
                                                        </div>
                                                        {/* Resize Handle */}
                                                        <div 
                                                            className="absolute top-0 right-0 w-2 h-full cursor-col-resize hover:bg-blue-300/50 z-50 nodrag"
                                                            style={{ right: '-1px' }}
                                                            onMouseDown={(e) => startResize(e, col.key)}
                                                        />
                                                    </th>
                                                ))}
                                                <th className="p-4 font-normal text-center bg-blue-600" style={{ borderLeft: '2px solid #94a3b8', borderBottom: '2px solid #94a3b8', backgroundColor: '#2563eb' }}>ACTION</th>
                                            </tr>
                                        </thead>
                                        <tbody className="w-full">
                                            {sortedDisclosures.map((d, index) => (
                                                <tr key={index} className="group hover:bg-white/5 transition-colors duration-150 w-full">
                                                    <td className="p-4 truncate text-center" style={{ borderRight: '2px solid #64748b', borderBottom: '2px solid #64748b', textAlign: 'center' }}>
                                                        <div className="font-bold text-slate-200 group-hover:text-amber-100 transition-colors truncate flex justify-center">{d.member}</div>
                                                    </td>
                                                    <td className="p-4 truncate text-center" style={{ borderRight: '2px solid #64748b', borderBottom: '2px solid #64748b', textAlign: 'center' }}>
                                                        <div className="text-[10px] text-slate-400 uppercase font-bold tracking-tighter truncate bg-slate-800/50 px-2 py-1 rounded inline-block border border-slate-700">
                                                            {d.sector || 'Unknown'}
                                                        </div>
                                                    </td>
                                                    <td className="p-4 truncate text-center" style={{ borderRight: '2px solid #64748b', borderBottom: '2px solid #64748b', textAlign: 'center' }}>
                                                        <div className="font-mono text-amber-400 font-black text-sm">{d.ticker}</div>
                                                        <div className="text-[9px] text-slate-600 font-bold">Stock</div>
                                                    </td>
                                                    <td className="p-4 truncate text-center" style={{ borderRight: '2px solid #64748b', borderBottom: '2px solid #64748b', textAlign: 'center' }}>
                                                        <span 
                                                            style={{ 
                                                                borderColor: (d.transaction === 'Purchase' || d.transaction.includes('Buy')) ? '#10b981' : 
                                                                            (d.transaction === 'Sale' || d.transaction.includes('Sell')) ? '#ef4444' : '#f59e0b',
                                                                color: (d.transaction === 'Purchase' || d.transaction.includes('Buy')) ? '#34d399' : 
                                                                       (d.transaction === 'Sale' || d.transaction.includes('Sell')) ? '#f87171' : '#fbbf24',
                                                                backgroundColor: (d.transaction === 'Purchase' || d.transaction.includes('Buy')) ? 'rgba(16, 185, 129, 0.1)' : 
                                                                                (d.transaction === 'Sale' || d.transaction.includes('Sell')) ? 'rgba(239, 68, 68, 0.1)' : 'rgba(245, 158, 11, 0.1)'
                                                            }}
                                                            className="inline-flex items-center gap-2 px-3 py-1.5 rounded-sm text-[9px] font-black tracking-widest border border-dashed uppercase truncate justify-center"
                                                        >
                                                            <div 
                                                                style={{ 
                                                                    backgroundColor: (d.transaction === 'Purchase' || d.transaction.includes('Buy')) ? '#10b981' : 
                                                                                    (d.transaction === 'Sale' || d.transaction.includes('Sell')) ? '#ef4444' : '#f59e0b',
                                                                    boxShadow: (d.transaction === 'Purchase' || d.transaction.includes('Buy')) ? '0 0 10px #10b981' : 
                                                                               (d.transaction === 'Sale' || d.transaction.includes('Sell')) ? '0 0 10px #ef4444' : '0 0 10px #f59e0b'
                                                                }}
                                                                className="w-1.5 h-1.5 rounded-full flex-shrink-0"
                                                            />
                                                            {d.transaction}
                                                        </span>
                                                    </td>
                                                    <td className="p-4 font-mono text-xs text-slate-300 truncate text-center" style={{ borderRight: '2px solid #64748b', borderBottom: '2px solid #64748b', textAlign: 'center' }}>
                                                        {d.amount_range}
                                                    </td>
                                                    <td className="p-4 font-mono text-xs text-slate-400 truncate text-center" style={{ borderRight: '2px solid #64748b', borderBottom: '2px solid #64748b', textAlign: 'center' }}>
                                                        {d.date}
                                                    </td>
                                                    <td className="p-4 text-center" style={{ borderBottom: '2px solid #64748b', textAlign: 'center' }}>
                                                        <button
                                                            onClick={() => alert(`Analyzing ${d.ticker} correlation...`)}
                                                            className="p-2 hover:bg-amber-500/20 rounded-full text-slate-500 hover:text-amber-400 transition-colors"
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

                    {/* 5. News Ticker Widget */}
                    <div key="news-ticker" className="glass-panel-gold overflow-hidden">
                        <NewsTicker isWidget={true} />
                    </div>
                </ResponsiveGridLayout>
                
                {/* Bottom Buffer */}
                <div className="scroll-buffer-100" />
            </div>

            {/* Premium Features */}
            <SenatorModal senator={selectedSenator} onClose={() => setSelectedSenator(null)} />
        </div>
    );
};

export default PoliticalAlpha;
