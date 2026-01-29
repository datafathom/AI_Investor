import React, { useState, useEffect, useRef } from 'react';
import { Network, Activity, Cpu, ShieldAlert, Zap, Layers, Box, TreeStructure, Clock, AlertTriangle } from 'lucide-react';
import { Responsive, WidthProvider } from 'react-grid-layout';
import * as d3 from 'd3';
import { StatCard } from '../components/DataViz';
import useTimelineStore from '../stores/timelineStore';

// Sprint 3 Widgets
import NodeConnectionHeatmap from '../widgets/Graph/NodeConnectionHeatmap';
import SpatialAssetBubble from '../widgets/Graph/SpatialAssetBubble';
import ReflexivityEcho from '../widgets/Graph/ReflexivityEcho';
import Neo4jHealthVitals from '../widgets/Graph/Neo4jHealthVitals';
import EntityOwnershipMatrix from '../widgets/Graph/EntityOwnershipMatrix';
import GraphTimeScrubber from '../widgets/Graph/GraphTimeScrubber';

import 'react-grid-layout/css/styles.css';
import 'react-resizable/css/styles.css';

const ResponsiveGridLayout = WidthProvider(Responsive);

const MasterOrchestrator = () => {
    // Layout Calculation
    const DEFAULT_LAYOUT = {
        lg: [
            { i: 'header', x: 0, y: 0, w: 12, h: 3 },
            { i: 'graph-view', x: 0, y: 3, w: 9, h: 10 },
            { i: 'system-pulse', x: 9, y: 3, w: 3, h: 5 },
            { i: 'reflexivity', x: 9, y: 8, w: 3, h: 5 },
            { i: 'spatial-grid', x: 0, y: 13, w: 4, h: 8 },
            { i: 'ownership-matrix', x: 4, y: 13, w: 5, h: 8 },
            { i: 'time-scrubber', x: 9, y: 13, w: 3, h: 8 },
            { i: 'heatmap', x: 0, y: 21, w: 12, h: 4 }
        ]
    };

    const graphRef = useRef(null);
    const [data, setData] = useState({ nodes: [], links: [] });
    const [loading, setLoading] = useState(true);
    const [activeShock, setActiveShock] = useState(null);
    const [selectedNode, setSelectedNode] = useState(null);

    // Sprint 6: Subscribe to timeline store for historical mode
    const { currentTime, isHistoricalMode } = useTimelineStore();

    // Fetch graph data - supports historical snapshots
    useEffect(() => {
        const fetchGraph = async () => {
            try {
                setLoading(true);
                // In historical mode, pass timestamp to API for snapshot data
                const endpoint = isHistoricalMode 
                    ? `/api/v1/master/graph?timestamp=${new Date(currentTime).toISOString()}`
                    : '/api/v1/master/graph';
                
                const response = await fetch(endpoint);
                const result = await response.json();
                if (result.status === 'success') {
                    setData(result.data);
                }
            } catch (error) {
                console.error("Failed to fetch graph data:", error);
            } finally {
                setLoading(false);
            }
        };
        fetchGraph();
    }, [isHistoricalMode, currentTime]); // Re-fetch when timeline changes

    const triggerShock = async (nodeId) => {
        try {
            const response = await fetch('/api/v1/master/shock', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ asset_id: nodeId, magnitude: -0.25 })
            });
            const result = await response.json();
            if (result.status === 'success') {
                setActiveShock(result.data);
                // Visual feedback in D3 graph would happen here
            }
        } catch (error) {
            console.error("Shock trigger failed:", error);
        }
    };

    // D3 Force Graph Implementation
    useEffect(() => {
        if (!graphRef.current || data.nodes.length === 0) return;

        d3.select(graphRef.current).selectAll("*").remove();

        const width = graphRef.current.clientWidth;
        const height = graphRef.current.clientHeight;

        const svg = d3.select(graphRef.current)
            .append("svg")
            .attr("width", width)
            .attr("height", height)
            .attr("viewBox", [0, 0, width, height]);

        const simulation = d3.forceSimulation(data.nodes)
            .force("link", d3.forceLink(data.links).id(d => d.id).distance(120))
            .force("charge", d3.forceManyBody().strength(-400))
            .force("center", d3.forceCenter(width / 2, height / 2));

        const link = svg.append("g")
            .attr("stroke", "#334155")
            .attr("stroke-opacity", 0.4)
            .selectAll("line")
            .data(data.links)
            .join("line")
            .attr("stroke-width", d => Math.sqrt(d.value || 1) * 2);

        const node = svg.append("g")
            .selectAll("circle")
            .data(data.nodes)
            .join("circle")
            .attr("r", d => d.val || 8)
            .attr("fill", d => {
                const colors = {
                    entity: "hsl(217, 91%, 60%)",
                    trust: "hsl(262, 83%, 58%)",
                    portfolio: "hsl(142, 71%, 45%)",
                    asset: "hsl(38, 92%, 50%)",
                    risk: "hsl(0, 84%, 60%)"
                };
                return colors[d.group] || "hsl(215, 16%, 47%)";
            })
            .style("cursor", "pointer")
            .on("click", (event, d) => {
                setSelectedNode(d);
                if (d.group === 'asset') triggerShock(d.id);
            })
            .call(d3.drag()
                .on("start", (e, d) => {
                    if (!e.active) simulation.alphaTarget(0.3).restart();
                    d.fx = d.x; d.fy = d.y;
                })
                .on("drag", (e, d) => { d.fx = e.x; d.fy = e.y; })
                .on("end", (e, d) => {
                    if (!e.active) simulation.alphaTarget(0);
                    d.fx = null; d.fy = null;
                }));

        const text = svg.append("g")
            .selectAll("text")
            .data(data.nodes)
            .join("text")
            .text(d => d.id)
            .attr("font-size", "10px")
            .attr("fill", "#94a3b8")
            .attr("dx", 12)
            .attr("dy", 4);

        simulation.on("tick", () => {
            link.attr("x1", d => d.source.x).attr("y1", d => d.source.y)
                .attr("x2", d => d.target.x).attr("y2", d => d.target.y);
            node.attr("cx", d => d.x).attr("cy", d => d.y);
            text.attr("x", d => d.x).attr("y", d => d.y);
        });

    }, [data]);

    return (
        <div className="orchestrator-dashboard-container p-4 h-full bg-slate-950 overflow-y-auto">
            <ResponsiveGridLayout
                className="layout"
                layouts={{ lg: DEFAULT_LAYOUT }}
                breakpoints={{ lg: 1200, md: 996, sm: 768, xs: 480, xxs: 0 }}
                cols={{ lg: 12, md: 10, sm: 6, xs: 4, xxs: 2 }}
                rowHeight={40}
                isDraggable={true}
                isResizable={true}
                margin={[16, 16]}
            >
                {/* Header */}
                <div key="header" className={`glass-panel glass-premium ${isHistoricalMode ? 'glass-glow-amber' : 'glass-glow-cyan'} p-6 flex flex-col justify-center`}>
                    {/* Historical Mode Banner */}
                    {isHistoricalMode && (
                        <div className="absolute top-0 left-0 right-0 bg-amber-500/20 border-b border-amber-500/30 px-4 py-2 flex items-center justify-center gap-2">
                            <AlertTriangle size={14} className="text-amber-400" />
                            <span className="text-amber-300 text-[10px] font-bold uppercase tracking-widest">
                                HISTORICAL VIEW: {new Date(currentTime).toLocaleString()}
                            </span>
                        </div>
                    )}
                    <div className={`flex justify-between items-center ${isHistoricalMode ? 'mt-6' : ''}`}>
                        <div>
                            <h1 className="text-3xl font-black text-white flex items-center gap-3">
                                <Network className={`${isHistoricalMode ? 'text-amber-400' : 'text-cyan-400'} animate-neon-pulse`} size={32} />
                                Ultimate AI Wealth Orchestrator
                            </h1>
                            <p className="text-zinc-400 mt-2 font-mono text-xs uppercase tracking-widest flex items-center gap-2">
                                <Activity size={12} className={isHistoricalMode ? 'text-amber-500' : 'text-emerald-500'}/>
                                {isHistoricalMode ? 'Viewing Historical Snapshot' : 'Unified Neo4j Super-Graph & System Reflexivity Logic'}
                            </p>
                        </div>
                        <div className="flex gap-4">
                             <StatCard label="Active Nodes" value={data.nodes.length || "0"} icon={Layers} color="blue" />
                             <StatCard label="Prop. Velocity" value={activeShock ? `${Math.round(activeShock.contagion_velocity * 100)}%` : "Low"} icon={ShieldAlert} color={activeShock ? "red" : "emerald"} />
                        </div>
                    </div>
                </div>

                {/* Graph View */}
                <div key="graph-view" className="glass-panel glass-premium p-0 relative overflow-hidden flex flex-col">
                    <div className="absolute top-4 left-4 z-10 glass-panel bg-black/40 p-3 rounded-lg backdrop-blur-md border border-white/5">
                         <h3 className="text-xs font-bold text-zinc-200 flex items-center gap-2 uppercase tracking-wide">
                            <Activity size={14} className="text-cyan-400 animate-pulse"/>
                            Neo4j Super-Graph Live View
                        </h3>
                    </div>
                    {selectedNode && (
                        <div className="absolute top-4 right-4 z-10 glass-panel bg-black/60 p-3 rounded-lg border border-white/10 animate-in fade-in zoom-in duration-300">
                             <p className="text-[10px] text-zinc-500 uppercase font-black mb-1">Node Inspector</p>
                             <p className="text-white text-xs font-bold">{selectedNode.id}</p>
                             <p className="text-cyan-400 text-[9px] uppercase">{selectedNode.group}</p>
                             {selectedNode.group === 'asset' && (
                                 <button 
                                    onClick={() => triggerShock(selectedNode.id)}
                                    className="mt-2 text-[9px] bg-red-500/20 text-red-400 border border-red-500/30 px-2 py-1 rounded hover:bg-red-500/40"
                                 >
                                    TRIGGER SHOCK
                                 </button>
                             )}
                        </div>
                    )}
                    <div className="flex-1 w-full h-full" ref={graphRef}></div>
                </div>

                {/* System Pulse / Health Vitals */}
                <div key="system-pulse" className="glass-panel glass-premium p-4">
                     <h3 className="text-[10px] font-black text-zinc-500 mb-4 flex items-center gap-2 uppercase tracking-widest">
                        <Cpu size={14} className="text-blue-400"/>
                        Neo4j Engine Vitals
                    </h3>
                    <Neo4jHealthVitals />
                </div>

                {/* Reflexivity Monitor */}
                <div key="reflexivity" className="glass-panel glass-premium glass-glow-red p-4">
                     <h3 className="text-[10px] font-black text-zinc-500 mb-4 flex items-center gap-2 uppercase tracking-widest">
                        <Zap size={14} className="text-yellow-400 animate-pulse"/>
                        Reflexivity Echo Monitor
                    </h3>
                    <ReflexivityEcho activeShock={activeShock} />
                </div>

                {/* Spatial Grid */}
                <div key="spatial-grid" className="glass-panel glass-premium p-0 overflow-hidden">
                    <h3 className="absolute top-4 left-4 z-10 text-[10px] font-black text-white/40 uppercase tracking-widest flex items-center gap-2">
                        <Box size={14} className="text-purple-400"/>
                        Spatial 3D Asset Cockpit
                    </h3>
                    <SpatialAssetBubble data={data} />
                </div>

                {/* Ownership Matrix */}
                <div key="ownership-matrix" className="glass-panel glass-premium p-4 flex flex-col">
                    <h3 className="text-[10px] font-black text-zinc-500 mb-4 flex items-center gap-2 uppercase tracking-widest">
                        <TreeStructure size={14} className="text-emerald-400"/>
                        Entity Ownership Matrix
                    </h3>
                    <div className="flex-1 overflow-hidden">
                        <EntityOwnershipMatrix data={data} />
                    </div>
                </div>

                {/* Time Scrubber */}
                <div key="time-scrubber" className="glass-panel glass-premium p-4 flex flex-col">
                    <h3 className="text-[10px] font-black text-zinc-500 mb-4 flex items-center gap-2 uppercase tracking-widest">
                        <Clock size={14} className="text-zinc-400"/>
                        Temporal Snapshot
                    </h3>
                    <div className="flex-1">
                        <GraphTimeScrubber />
                    </div>
                </div>

                {/* Heatmap / SPF Finder */}
                <div key="heatmap" className="glass-panel glass-premium p-4">
                    <h3 className="text-[10px] font-black text-zinc-500 mb-4 flex items-center gap-2 uppercase tracking-widest">
                        <Layers size={14} className="text-red-400"/>
                        Single Points of Failure (SPF) Heatmap
                    </h3>
                    <NodeConnectionHeatmap data={data} />
                </div>

            </ResponsiveGridLayout>
        </div>
    );
};

export default MasterOrchestrator;
