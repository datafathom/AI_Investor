import React, { useMemo } from 'react';
import * as d3 from 'd3';

const NodeConnectionHeatmap = ({ data }) => {
    // data: { nodes: [], links: [] }
    
    const heatmapData = useMemo(() => {
        if (!data || !data.nodes) return [];
        
        // Calculate degree centrality (number of connections) for each node
        const centrality = {};
        data.nodes.forEach(n => centrality[n.id] = 0);
        data.links.forEach(l => {
            const sourceId = typeof l.source === 'object' ? l.source.id : l.source;
            const targetId = typeof l.target === 'object' ? l.target.id : l.target;
            if (centrality[sourceId] !== undefined) centrality[sourceId]++;
            if (centrality[targetId] !== undefined) centrality[targetId]++;
        });

        return data.nodes.map(n => ({
            id: n.id,
            group: n.group,
            connections: centrality[n.id] || 0,
            x: Math.random() * 100, // Placeholder positions if no spatial data
            y: Math.random() * 100
        })).sort((a, b) => b.connections - a.connections);
    }, [data]);

    return (
        <div className="w-full h-full flex flex-col p-4 overflow-auto">
            <div className="grid grid-cols-1 gap-2">
                {heatmapData.slice(0, 10).map((node, i) => (
                    <div key={node.id} className="flex items-center justify-between p-2 bg-slate-900/50 rounded border border-white/5">
                        <div className="flex items-center gap-3">
                            <div 
                                className="w-3 h-3 rounded-full" 
                                style={{ 
                                    backgroundColor: node.connections > 5 ? 'hsl(0, 84%, 60%)' : 'hsl(217, 91%, 60%)',
                                    boxShadow: node.connections > 5 ? '0 0 10px hsl(0, 84%, 60%)' : 'none'
                                }}
                            />
                            <span className="text-zinc-300 text-xs font-mono">{node.id}</span>
                        </div>
                        <div className="flex items-center gap-2">
                             <div className="h-1.5 w-24 bg-zinc-800 rounded-full overflow-hidden">
                                <div 
                                    className={`h-full ${node.connections > 5 ? 'bg-red-500' : 'bg-blue-500'}`}
                                    style={{ width: `${Math.min(100, node.connections * 10)}%` }}
                                />
                            </div>
                            <span className="text-white text-[10px] font-bold w-4">{node.connections}</span>
                        </div>
                    </div>
                ))}
            </div>
            {heatmapData.length === 0 && (
                <div className="flex-1 flex items-center justify-center text-zinc-500 text-xs italic">
                    No graph data loaded
                </div>
            )}
        </div>
    );
};

export default NodeConnectionHeatmap;
