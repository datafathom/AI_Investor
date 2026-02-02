import React, { useState, useEffect, useRef } from 'react';
import { Award, Target, Activity } from 'lucide-react';
import { Responsive, WidthProvider } from 'react-grid-layout';
import { StatCard } from '../components/DataViz';
import SCMScore from '../components/Reporting/SCMScore';
import InflationBasket from '../components/Settings/InflationBasket';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';

const ResponsiveGridLayout = WidthProvider(Responsive);

const DEFAULT_LAYOUT = {
    lg: [
        { i: 'header', x: 0, y: 0, w: 12, h: 3 },
        { i: 'scm-score', x: 0, y: 3, w: 4, h: 10 },
        { i: 'inflation-basket', x: 4, y: 3, w: 8, h: 10 },
        { i: 'class-risk', x: 0, y: 13, w: 4, h: 8 },
        { i: 'swr-adjuster', x: 4, y: 13, w: 4, h: 8 },
        { i: 'dilution', x: 8, y: 13, w: 4, h: 8 }
    ]
};

const SocialClassMaintenance = () => {
    const STORAGE_KEY = 'layout_social_class_maintenance';
    const [layouts, setLayouts] = useState(() => {
        try {
            const saved = localStorage.getItem(STORAGE_KEY);
            return saved ? JSON.parse(saved) : DEFAULT_LAYOUT;
        } catch (e) {
            return DEFAULT_LAYOUT;
        }
    });

    const onLayoutChange = (currentLayout, allLayouts) => {
        setLayouts(allLayouts);
        localStorage.setItem(STORAGE_KEY, JSON.stringify(allLayouts));
    };

    const [scmData, setScmData] = useState({ score: 1.0, clew: 0.03, yield: 0.05, dilution: 0 });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await apiClient.get('/economics/clew');
                if (response.status === 'success' || response.current_index) {
                    const clew = response.inflation_rate || 0.084;
                    const yieldRate = 0.115; // Placeholder for actual portfolio yield
                    setScmData({
                        score: yieldRate / clew,
                        clew: clew,
                        yield: yieldRate,
                        dilution: 43.5 // Mock for now until dilution svc linked
                    });
                }
            } catch (err) {
                console.error("SCM Data fetch failed:", err);
            } finally {
                setLoading(false);
            }
        };
        fetchData();
    }, []);

    return (
        <div className="full-bleed-page system-dashboard-page p-4 bg-slate-950">
             <ResponsiveGridLayout
                className="layout"
                layouts={layouts}
                onLayoutChange={onLayoutChange}
                breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
                cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
                rowHeight={40}
                isDraggable={true}
                isResizable={true}
                margin={[16, 16]}
            >
                {/* Header */}
                <div key="header" className="glass-panel glass-premium glass-glow-cyan p-6 flex flex-col justify-center">
                    <div className="flex justify-between items-center">
                        <div>
                            <h1 className="text-3xl font-bold text-white flex items-center gap-3">
                                <Award className="text-yellow-500 animate-neon-pulse" size={32} />
                                Social Class Maintenance (SCM)
                            </h1>
                            <p className="text-zinc-400 mt-2 font-mono text-xs uppercase tracking-widest">Phase 197: Return on Lifestyle & Personal Inflation Monitor</p>
                        </div>
                        <div className="flex gap-4">
                             <StatCard 
                                label="Safe Withdrawal Rate" 
                                value={2.8} 
                                suffix="%"
                                changeLabel="Adjusted for Lifestyle"
                                status="positive"
                            />
                        </div>
                    </div>
                </div>

                {/* SCM Score Component */}
                <div key="scm-score" className="glass-panel glass-premium p-0 flex flex-col overflow-hidden">
                    <SCMScore 
                        score={scmData.score} 
                        clewRate={scmData.clew} 
                        yieldRate={scmData.yield} 
                    />
                </div>

                {/* Inflation Basket Settings */}
                <div key="inflation-basket" className="glass-panel glass-premium p-0 flex flex-col overflow-hidden">
                    <InflationBasket onSave={(data) => console.log("SCM Settings Saved", data)} />
                </div>

                {/* Class Risk Simulator */}
                <div key="class-risk" className="glass-panel glass-premium glass-glow-red p-6">
                    <h3 className="text-sm font-black text-zinc-200 mb-6 flex items-center gap-2 uppercase tracking-widest">
                        <Target size={18} className="text-purple-400"/>
                        Class Risk Simulator
                    </h3>
                    <div className="flex flex-col items-center justify-center h-full">
                         <div className="relative w-32 h-32 flex items-center justify-center">
                            <svg className="w-full h-full" viewBox="0 0 36 36">
                                <path
                                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                                    fill="none"
                                    stroke="#3f3f46"
                                    strokeWidth="3"
                                />
                                <path
                                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831"
                                    fill="none"
                                    stroke="#ef4444"
                                    strokeWidth="3"
                                    strokeDasharray="5, 100"
                                />
                            </svg>
                            <div className="absolute text-center">
                                <span className="text-2xl font-bold text-white">4.2%</span>
                                <p className="text-[10px] text-zinc-500">Drop Prob.</p>
                            </div>
                         </div>
                    </div>
                </div>

                {/* SWR Adjuster */}
                <div key="swr-adjuster" className="glass-panel p-6">
                    <h3 className="text-lg font-semibold text-zinc-200 mb-4 flex items-center gap-2 uppercase">
                        SWR Adjuster
                    </h3>
                     <div className="space-y-4">
                         <div className="flex justify-between items-center bg-emerald-900/10 p-3 rounded-lg border border-emerald-500/20">
                            <span className="text-emerald-400 text-sm font-medium">UHNW 2.8% Rule</span>
                            <span className="text-white text-sm">$28k / $1M</span>
                        </div>
                        <p className="text-xs text-zinc-500">
                            Combatting higher personal inflation and multi-generational duration requirements.
                        </p>
                    </div>
                </div>

                {/* Dilution Tracker */}
                <div key="dilution" className="glass-panel p-6">
                     <h3 className="text-lg font-semibold text-zinc-200 mb-4 flex items-center gap-2 uppercase">
                        Gen 3 Dilution
                    </h3>
                    <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                            <span className="text-zinc-400">Grandkids (Gen 3)</span>
                            <span className="text-red-400">$11.2M / ea</span>
                        </div>
                        <div className="mt-4 p-2 bg-red-900/20 border border-red-500/20 rounded text-center">
                            <span className="text-red-400 text-xs font-bold uppercase tracking-tighter">Wealth Decay Protection Enabled</span>
                        </div>
                    </div>
                </div>

            </ResponsiveGridLayout>
        </div>
    );
};

export default SocialClassMaintenance;
