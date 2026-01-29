import React, { useState, useEffect, useRef } from 'react';
import { Shield, TrendingUp, AlertTriangle, Activity, DollarSign, Award, Target } from 'lucide-react';
import { Responsive, WidthProvider } from 'react-grid-layout';
import * as d3 from 'd3';
import { StatCard, GlassCard } from '../components/DataViz';
import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';

const ResponsiveGridLayout = WidthProvider(Responsive);

const DEFAULT_LAYOUT = {
    lg: [
        { i: 'header', x: 0, y: 0, w: 12, h: 3 },
        { i: 'clew-chart', x: 0, y: 3, w: 8, h: 10 },
        { i: 'burn-rate', x: 8, y: 3, w: 4, h: 10 },
        { i: 'class-risk', x: 0, y: 13, w: 4, h: 8 },
        { i: 'swr-adjuster', x: 4, y: 13, w: 4, h: 8 },
        { i: 'dilution', x: 8, y: 13, w: 4, h: 8 }
    ]
};

const SocialClassMaintenance = () => {
    const STORAGE_KEY = 'layout_social_class_maintenance';
    const [inflationData, setInflationData] = useState([]);
    const chartRef = useRef(null);

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

    // Mock Data Generator for CLEW (Cost of Living Extremely Well) Index
    useEffect(() => {
        const generateData = () => {
            const data = [];
            let cpi = 100;
            let clew = 100;
            const startDate = new Date('2020-01-01');

            for (let i = 0; i < 60; i++) { // 5 years monthly
                const date = new Date(startDate);
                date.setMonth(date.getMonth() + i);
                
                // CPI ~3% annual
                cpi *= (1 + (0.03/12) + (Math.random() * 0.002 - 0.001));
                
                // CLEW ~8% annual (Tuition, Luxury Travel, Staff)
                clew *= (1 + (0.08/12) + (Math.random() * 0.005 - 0.0025));

                data.push({
                    date: date,
                    cpi: cpi,
                    clew: clew
                });
            }
            setInflationData(data);
        };
        generateData();
    }, []);

    // D3 Chart Implementation
    useEffect(() => {
        if (!inflationData.length || !chartRef.current) return;

        // Clear previous
        d3.select(chartRef.current).selectAll("*").remove();

        const margin = { top: 20, right: 30, bottom: 30, left: 40 };
        const width = Math.max(0, chartRef.current.clientWidth - margin.left - margin.right);
        const height = Math.max(0, chartRef.current.clientHeight - margin.top - margin.bottom);

        if (width <= 0 || height <= 0) return;

        const svg = d3.select(chartRef.current)
            .append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", `translate(${margin.left},${margin.top})`);

        // Scales
        const x = d3.scaleTime()
            .domain(d3.extent(inflationData, d => d.date))
            .range([0, width]);

        const y = d3.scaleLinear()
            .domain([90, d3.max(inflationData, d => Math.max(d.cpi, d.clew)) * 1.1])
            .range([height, 0]);

        // Lines
        const lineCPI = d3.line()
            .x(d => x(d.date))
            .y(d => y(d.cpi))
            .curve(d3.curveMonotoneX);

        const lineCLEW = d3.line()
            .x(d => x(d.date))
            .y(d => y(d.clew))
            .curve(d3.curveMonotoneX);

        // Axes
        svg.append("g")
            .attr("transform", `translate(0,${height})`)
            .call(d3.axisBottom(x).ticks(5))
            .attr("color", "#64748b");

        svg.append("g")
            .call(d3.axisLeft(y))
            .attr("color", "#64748b");

        // Paths
        svg.append("path")
            .datum(inflationData)
            .attr("fill", "none")
            .attr("stroke", "#94a3b8") // Slate 400
            .attr("stroke-width", 2)
            .attr("d", lineCPI);

        svg.append("path")
            .datum(inflationData)
            .attr("fill", "none")
            .attr("stroke", "#ef4444") // Red 500
            .attr("stroke-width", 3)
            .attr("d", lineCLEW);

        // Legend
        svg.append("text").attr("x", 20).attr("y", 20).text("CPI (Standard)").attr("fill", "#94a3b8").style("font-size", "12px");
        svg.append("text").attr("x", 20).attr("y", 40).text("CLEW (Index)").attr("fill", "#ef4444").style("font-size", "12px").style("font-weight", "bold");

    }, [inflationData]);


    return (
        <div className="full-bleed-page system-dashboard-page p-4">
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
                                label="Current CLEW Inflation" 
                                value={8.4} 
                                suffix="%"
                                change={0.5} 
                                status="negative"
                            />
                            <StatCard 
                                label="Safe Withdrawal Rate" 
                                value={2.8} 
                                suffix="%"
                                change={0}
                                changeLabel="Adjusted for Lifestyle"
                                status="positive"
                            />
                        </div>
                    </div>
                </div>

                {/* CLEW vs CPI Chart */}
                <div key="clew-chart" className="glass-panel glass-premium p-6 flex flex-col">
                    <h3 className="text-sm font-black text-zinc-200 mb-6 flex items-center gap-2 uppercase tracking-widest">
                        <Activity size={18} className="text-blue-400"/>
                        CLEW Index vs. Global CPI
                    </h3>
                    <div className="flex-1 w-full h-full" ref={chartRef}></div>
                </div>

                {/* Burn Rate Widget */}
                <div key="burn-rate" className="glass-panel glass-premium p-6">
                    <h3 className="text-sm font-black text-zinc-200 mb-8 flex items-center gap-2 uppercase tracking-widest">
                        <AlertTriangle size={18} className="text-orange-400"/>
                        Lifestyle Burn Rate
                    </h3>
                    <div className="space-y-6">
                        <div>
                            <div className="flex justify-between text-sm text-zinc-400 mb-1">
                                <span>Annual Spend (Current)</span>
                                <span className="text-white">$1.2M</span>
                            </div>
                            <div className="w-full bg-zinc-800 h-2 rounded-full">
                                <div className="bg-blue-500 h-2 rounded-full" style={{ width: '40%' }}></div>
                            </div>
                        </div>
                         <div>
                            <div className="flex justify-between text-sm text-zinc-400 mb-1">
                                <span>Projected Spend (2035)</span>
                                <span className="text-red-400">$3.8M</span>
                            </div>
                            <div className="w-full bg-zinc-800 h-2 rounded-full">
                                <div className="bg-red-500 h-2 rounded-full" style={{ width: '85%' }}></div>
                            </div>
                            <p className="text-xs text-zinc-500 mt-2">
                                *Assumes 8.4% CLEW inflation (Tuition +12%, Staff +5%, Travel +9%)
                            </p>
                        </div>
                    </div>
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
                                <span className="text-2xl font-bold text-white">5%</span>
                                <p className="text-[10px] text-zinc-500">Drop Prob.</p>
                            </div>
                         </div>
                         <p className="text-center text-xs text-zinc-400 mt-4">
                             Probability of mandatory lifestyle reduction (e.g. Commercial Flying) within 10 years.
                         </p>
                    </div>
                </div>

                {/* SWR Adjuster */}
                <div key="swr-adjuster" className="glass-panel p-6">
                    <h3 className="text-lg font-semibold text-zinc-200 mb-4 flex items-center gap-2">
                        <DollarSign size={18} className="text-emerald-400"/>
                        SWR Adjuster
                    </h3>
                     <div className="space-y-4">
                        <div className="flex justify-between items-center bg-zinc-900/50 p-3 rounded-lg border border-zinc-800">
                            <span className="text-zinc-400 text-sm">Standard 4% Rule</span>
                            <span className="text-zinc-500 text-sm line-through">$40k / $1M</span>
                        </div>
                         <div className="flex justify-between items-center bg-emerald-900/10 p-3 rounded-lg border border-emerald-500/20">
                            <span className="text-emerald-400 text-sm font-medium">UHNW 2.8% Rule</span>
                            <span className="text-white text-sm">$28k / $1M</span>
                        </div>
                        <p className="text-xs text-zinc-500">
                            UHNW portfolios require lower withdrawal rates to combat higher personal inflation and support multi-generational duration.
                        </p>
                    </div>
                </div>

                {/* Dilution Tracker */}
                <div key="dilution" className="glass-panel p-6">
                     <h3 className="text-lg font-semibold text-zinc-200 mb-4 flex items-center gap-2">
                        <Activity size={18} className="text-cyan-400"/>
                        Gen 3 Dilution
                    </h3>
                    <div className="space-y-2">
                        <div className="flex justify-between text-sm">
                            <span className="text-zinc-400">Founder (Gen 1)</span>
                            <span className="text-white">$100M</span>
                        </div>
                         <div className="flex justify-between text-sm">
                            <span className="text-zinc-400">Children (Gen 2 - 3x)</span>
                            <span className="text-zinc-300">$33M / ea</span>
                        </div>
                         <div className="flex justify-between text-sm">
                            <span className="text-zinc-400">Grandkids (Gen 3 - 9x)</span>
                            <span className="text-red-400">$11M / ea</span>
                        </div>
                        <div className="mt-4 p-2 bg-red-900/20 border border-red-500/20 rounded text-center">
                            <span className="text-red-400 text-xs font-bold uppercase">Wealth Decay Alert</span>
                        </div>
                    </div>
                </div>

            </ResponsiveGridLayout>
        </div>
    );
};

export default SocialClassMaintenance;
