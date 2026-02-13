import React, { useState, useEffect } from 'react';
import { chartService } from '../../services/chartService';
import { ResponsiveContainer, Treemap, Tooltip } from 'recharts';
import { Grid, Layers, Download } from 'lucide-react';
import { toast } from 'sonner';

const CorrelationMatrix = ({ data }) => {
    if (!data) return null;
    const { tickers, matrix } = data;

    const getColor = (val) => {
        // Red (-1) to White (0) to Green (1)
        if (val === 1) return '#10b981'; // Identity
        if (val > 0) {
            // Log scale for better visibility? Just linear for now
            const alpha = Math.min(Math.abs(val), 1);
            return `rgba(16, 185, 129, ${alpha})`;
        } else {
             const alpha = Math.min(Math.abs(val), 1);
            return `rgba(239, 68, 68, ${alpha})`;
        }
    };

    return (
        <div className="overflow-x-auto">
            <table className="w-full text-xs text-center border-collapse">
                <thead>
                    <tr>
                        <th className="p-2 bg-slate-900 border border-slate-800"></th>
                        {tickers.map(t => (
                            <th key={t} className="p-2 bg-slate-900 border border-slate-800 font-bold text-slate-400">{t}</th>
                        ))}
                    </tr>
                </thead>
                <tbody>
                    {matrix.map((row, i) => (
                        <tr key={i}>
                            <td className="p-2 bg-slate-900 border border-slate-800 font-bold text-slate-400">{tickers[i]}</td>
                            {row.map((val, j) => (
                                <td 
                                    key={j} 
                                    className="p-2 border border-slate-800 text-white font-mono"
                                    style={{ backgroundColor: getColor(val) }}
                                >
                                    {val.toFixed(2)}
                                </td>
                            ))}
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

// Custom Content for Treemap
const CustomizedContent = (props) => {
    const { root, depth, x, y, width, height, index, payload, colors, rank, name, value, change } = props;

    const color = change > 0 ? '#10b981' : '#ef4444';
    const opacity = Math.min(Math.abs(change) / 3, 1) * 0.8 + 0.2; // Opacity based on magnitude

    return (
        <g>
            <rect
                x={x}
                y={y}
                width={width}
                height={height}
                style={{
                    fill: color,
                    fillOpacity: opacity,
                    stroke: '#0f172a',
                    strokeWidth: 2 / (depth + 1e-10),
                    strokeOpacity: 1 / (depth + 1e-10),
                }}
            />
            {width > 30 && height > 30 && (
                <text x={x + width / 2} y={y + height / 2 + 7} textAnchor="middle" fill="#fff" fontSize={10} fontWeight="bold">
                    {name}
                    <tspan x={x + width / 2} dy="1.2em" fontSize={9} fill="rgba(255,255,255,0.8)">{change?.toFixed(2)}%</tspan>
                </text>
            )}
        </g>
    );
};

const HeatmapGenerator = () => {
    const [activeTab, setActiveTab] = useState('sector');
    const [correlationData, setCorrelationData] = useState(null);
    const [sectorData, setSectorData] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        loadData();
    }, [activeTab]);

    const loadData = async () => {
        setLoading(true);
        try {
            if (activeTab === 'correlation' && !correlationData) {
                const res = await chartService.getCorrelationHeatmap();
                setCorrelationData(res);
            } else if (activeTab === 'sector' && !sectorData) {
                const res = await chartService.getSectorHeatmap();
                // Transform for Recharts Treemap
                // Root -> Sectors -> Stocks
                const tree = res.sectors.map(sector => ({
                    name: sector.name,
                    children: sector.stocks.map(s => ({
                        name: s.ticker,
                        size: s.market_cap,
                        change: s.change
                    }))
                }));
                setSectorData(tree);
            }
        } catch (e) {
            toast.error("Failed to load heatmap data");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="h-full bg-slate-950 p-6 text-slate-200 flex flex-col">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-2xl font-bold bg-gradient-to-r from-cyan-400 to-blue-500 bg-clip-text text-transparent flex items-center gap-3">
                    <Grid className="text-blue-500" /> Heatmap Generator
                </h1>
                
                <div className="flex gap-2">
                    <div className="bg-slate-900 p-1 rounded-lg flex border border-slate-800">
                        <button 
                            onClick={() => setActiveTab('sector')}
                            className={`px-4 py-1.5 rounded text-sm font-bold transition-all ${activeTab === 'sector' ? 'bg-cyan-500 text-white shadow-lg shadow-cyan-500/20' : 'text-slate-400 hover:text-white'}`}
                        >
                            <span className="flex items-center gap-2"><Layers size={14} /> Sector Map</span>
                        </button>
                        <button 
                            onClick={() => setActiveTab('correlation')}
                            className={`px-4 py-1.5 rounded text-sm font-bold transition-all ${activeTab === 'correlation' ? 'bg-cyan-500 text-white shadow-lg shadow-cyan-500/20' : 'text-slate-400 hover:text-white'}`}
                        >
                            <span className="flex items-center gap-2"><Grid size={14} /> Correlation</span>
                        </button>
                    </div>
                </div>
            </div>

            <div className="flex-1 bg-slate-900 rounded-xl border border-slate-800 p-4 relative overflow-hidden">
                {loading && (
                     <div className="absolute inset-0 flex items-center justify-center bg-slate-900/50 z-10">
                        <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-cyan-500"></div>
                    </div>
                )}

                {activeTab === 'correlation' && correlationData && (
                    <CorrelationMatrix data={correlationData} />
                )}

                {activeTab === 'sector' && sectorData && (
                    <div className="h-full w-full">
                         <ResponsiveContainer width="100%" height="100%">
                            <Treemap
                                data={sectorData}
                                dataKey="size"
                                aspectRatio={4 / 3}
                                stroke="#fff"
                                content={<CustomizedContent />}
                            >
                                <Tooltip content={({ payload }) => {
                                    if (!payload || !payload.length) return null;
                                    const d = payload[0].payload;
                                    return (
                                        <div className="bg-slate-900 border border-slate-700 p-2 rounded shadow-xl text-xs">
                                            <div className="font-bold text-white">{d.name}</div>
                                            <div className={`${d.change > 0 ? 'text-emerald-400' : 'text-red-400'}`}>
                                                Change: {d.change?.toFixed(2)}%
                                            </div>
                                            <div className="text-slate-500">Cap: ${d.size?.toFixed(1)}B</div>
                                        </div>
                                    );
                                }}/>
                            </Treemap>
                        </ResponsiveContainer>
                    </div>
                )}
            </div>
        </div>
    );
};

export default HeatmapGenerator;
