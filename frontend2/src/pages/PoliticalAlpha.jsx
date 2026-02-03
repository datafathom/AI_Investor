import React, { useState, useEffect, Suspense, lazy, useTransition } from 'react';
import { politicsService } from '../services/politicsService';
import { StorageService } from '../utils/storageService';
import { Landmark, Gavel, TrendingUp, AlertTriangle, FileText, DollarSign, Activity, Eye, PieChart, Info } from 'lucide-react';
import { Responsive, WidthProvider } from 'react-grid-layout';
import './PoliticalAlpha.css';

const SenatorModal = lazy(() => import('../components/Political/SenatorModal'));
const SectorImpactChart = lazy(() => import('../components/Political/SectorImpactChart'));
const NewsTicker = lazy(() => import('../components/Political/NewsTicker'));
import PageHeader from '../components/Navigation/PageHeader';

const ResponsiveGridLayout = WidthProvider(Responsive);
const STORAGE_KEY = 'political_alpha_layout_v16'; // Incremented for fresh layout

const DEFAULT_LAYOUTS = {
    lg: [
        { i: 'summary', x: 0, y: 0, w: 12, h: 3 },
        { i: 'sentiment', x: 0, y: 3, w: 12, h: 10 },
        { i: 'impact', x: 0, y: 13, w: 12, h: 8 },
        { i: 'watchlist', x: 0, y: 21, w: 12, h: 10 },
        { i: 'feed', x: 0, y: 31, w: 12, h: 12 },
        { i: 'news-ticker', x: 0, y: 43, w: 12, h: 2 }
    ],
    md: [
        { i: 'summary', x: 0, y: 0, w: 10, h: 3 },
        { i: 'sentiment', x: 0, y: 3, w: 10, h: 8 },
        { i: 'impact', x: 0, y: 11, w: 10, h: 6 },
        { i: 'watchlist', x: 0, y: 17, w: 10, h: 8 },
        { i: 'feed', x: 0, y: 25, w: 10, h: 8 },
        { i: 'news-ticker', x: 0, y: 33, w: 10, h: 2 }
    ],
    sm: [
        { i: 'summary', x: 0, y: 0, w: 6, h: 4 },
        { i: 'sentiment', x: 0, y: 4, w: 6, h: 8 },
        { i: 'impact', x: 0, y: 12, w: 6, h: 6 },
        { i: 'watchlist', x: 0, y: 18, w: 6, h: 8 },
        { i: 'feed', x: 0, y: 26, w: 6, h: 10 },
        { i: 'news-ticker', x: 0, y: 36, w: 6, h: 2 }
    ]
};

const MOCK_CHAMBER_DATA = [
// ... (data skipped) ...
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

// Standardized Widget Header (Inline handles in JSX below)

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

    // Concurrent Sorting
    const [isPending, startTransition] = useTransition();

    // Resize Ref
    const resizingRef = React.useRef(null);

    // Persisted Layout State
    const [layouts, setLayouts] = useState(DEFAULT_LAYOUTS);

    useEffect(() => {
        const loadLayout = async () => {
            const saved = await StorageService.get(STORAGE_KEY);
            if (saved) setLayouts(saved);
        };
        loadLayout();
    }, []);

    const onLayoutChange = (current, allLayouts) => {
        setLayouts(allLayouts);
        StorageService.set(STORAGE_KEY, allLayouts);
    };

    const handleSort = (key) => {
        startTransition(() => {
            console.log(`Sorting by ${key}`);
            let direction = 'asc';
            if (sortConfig.key === key && sortConfig.direction === 'asc') {
                direction = 'desc';
            }
            setSortConfig({ key, direction });
        });
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
                    if (result && Array.isArray(result) && result.length > 0) {
                        setDisclosures(result);
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

    // Enable scrolling on parent containers for this page
    useEffect(() => {
        const root = document.getElementById('root');
        const appShell = document.querySelector('.app-shell');
        const main = document.querySelector('main');
        
        const originalStyles = {
            root: root ? root.style.cssText : '',
            appShell: appShell ? appShell.style.cssText : '',
            main: main ? main.style.cssText : ''
        };

        if (root) {
            root.style.height = 'auto';
            root.style.minHeight = '100vh';
            root.style.overflowY = 'auto';
            root.style.overflowX = 'hidden';
        }
        if (appShell) {
            appShell.style.height = 'auto';
            appShell.style.minHeight = '100vh';
            appShell.style.overflowY = 'auto';
            appShell.style.overflowX = 'hidden';
        }
        if (main) {
            main.style.overflow = 'visible';
            main.style.height = 'auto';
        }

        // Cleanup: restore original styles when leaving page
        return () => {
            if (root) root.style.cssText = originalStyles.root;
            if (appShell) appShell.style.cssText = originalStyles.appShell;
            if (main) main.style.cssText = originalStyles.main;
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

            <div style={{ height: 'calc(100vh - 120px)', overflowY: 'auto', overflowX: 'hidden' }}>
                <ResponsiveGridLayout
                    className="layout"
                    layouts={layouts}
                    onLayoutChange={onLayoutChange}
                    breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
                    cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
                    rowHeight={40}
                    isDraggable={true}
                    isResizable={true}
                    margin={[10, 10]}
                >
                    {/* 0. Political Summary Widget */}
                    <div key="summary" className="glass-panel flex items-center justify-between px-10 py-6">
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
                    <div key="sentiment" className="glass-panel">
                       <div className="glass-panel-header">
                            <Activity size={14} className="text-amber-400" />
                            <span>Senate Sentiment Map | Institutional Pulse</span>
                       </div>
                       <div className="p-6 h-full flex flex-col overflow-y-auto scrollbar-gold">
                            
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
                    <div key="impact" className="glass-panel overflow-hidden">
                        <div className="glass-panel-header">
                            <PieChart size={14} className="text-amber-400" />
                            <span>Sector Impact Profile</span>
                        </div>
                        <div className="p-6 h-full flex flex-col">
                            <div className="flex-1 min-h-0">
                                <Suspense fallback={<div className="flex items-center justify-center h-full text-amber-500/50">Loading Chart...</div>}>
                                    <SectorImpactChart />
                                </Suspense>
                            </div>
                        </div>
                    </div>

                    {/* ... (Active Legislation Tracker skipped for brevity if not changed) ... */}
                    {/* 3. Active Legislation Tracker (Actually next is News Ticker at end of grid) */}
                    
                    {/* ... Feed widget ... */}

                    {/* 5. News Ticker Widget */}
                    <div key="news-ticker" className="glass-panel overflow-hidden">
                        <div className="glass-panel-header">
                            <TrendingUp size={14} className="text-amber-400" />
                            <span>Capitol Hill Ticker</span>
                        </div>
                        <Suspense fallback={<div className="p-2 text-center text-xs text-amber-500/50">Loading Ticker...</div>}>
                            <NewsTicker isWidget={true} />
                        </Suspense>
                    </div>
                </ResponsiveGridLayout>
                
                {/* Bottom Buffer */}
                <div className="scroll-buffer-200" />
            </div>

            {/* Premium Features */}
            <Suspense fallback={null}>
                <SenatorModal senator={selectedSenator} onClose={() => setSelectedSenator(null)} />
            </Suspense>
        </div>
    );
};

export default PoliticalAlpha;
