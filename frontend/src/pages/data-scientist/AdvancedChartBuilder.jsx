import React, { useState, useEffect, useRef } from 'react';
import { chartService } from '../../services/chartService';
import { DrawingToolbar } from '../../components/charts/DrawingToolbar';
import { toast } from 'sonner';
import { ChartExportModal } from '../../components/modals/ChartExportModal';
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, ReferenceLine } from 'recharts';
import { Layout, Maximize2, Settings, Save, Search, CandlestickChart } from 'lucide-react';

const AdvancedChartBuilder = () => {
    const [ticker, setTicker] = useState('AAPL');
    const [timeframe, setTimeframe] = useState('1day');
    const [data, setData] = useState([]);
    const [drawings, setDrawings] = useState([]);
    const [activeTool, setActiveTool] = useState('cursor');
    const [loading, setLoading] = useState(false);
    const [showExport, setShowExport] = useState(false);
    
    // Mock Drawing Interaction State
    const [isDrawing, setIsDrawing] = useState(false);
    const [tempDrawing, setTempDrawing] = useState(null);

    useEffect(() => {
        loadData();
    }, [ticker, timeframe]);

    const loadData = async () => {
        try {
            setLoading(true);
            const res = await chartService.getCandles(ticker, timeframe);
            if (res.data) {
                // Formatting for Recharts
                const formatted = res.data.map(d => ({
                   ...d,
                   dateStr: new Date(d.date).toLocaleDateString()
                }));
                setData(formatted);
            }
        } catch (e) {
            toast.error("Failed to load chart data");
        } finally {
            setLoading(false);
        }
    };

    const handleChartClick = (e) => {
        if (activeTool === 'cursor') return;
        
        // Mock drawing logic
        if (!isDrawing) {
            setIsDrawing(true);
            const point = { x: e.activeLabel, y: e.activePayload?.[0]?.value };
            setTempDrawing({ start: point, end: point, type: activeTool });
        } else {
            setIsDrawing(false);
             const point = { x: e.activeLabel, y: e.activePayload?.[0]?.value };
            setDrawings([...drawings, { ...tempDrawing, end: point }]);
            setTempDrawing(null);
            toast.success("Drawing added");
        }
    };

    return (
        <div className="relative h-full flex flex-col bg-slate-950 text-slate-200">
            {/* Top Bar */}
            <div className="h-16 border-b border-slate-800 flex items-center px-4 justify-between bg-slate-900">
                <div className="flex items-center gap-4">
                    <div className="flex bg-slate-800 rounded-lg p-1 border border-slate-700">
                        <Search size={16} className="ml-2 text-slate-500" />
                        <input 
                            value={ticker}
                            onChange={(e) => setTicker(e.target.value.toUpperCase())}
                            onKeyDown={(e) => e.key === 'Enter' && loadData()}
                            className="bg-transparent border-none text-white text-sm px-2 w-24 outline-none font-bold"
                        />
                    </div>
                    
                    <div className="flex bg-slate-800 rounded-lg p-1 border border-slate-700">
                        {['15min', '1hr', '4hr', '1day', '1week'].map(tf => (
                            <button
                                key={tf}
                                onClick={() => setTimeframe(tf)}
                                className={`px-3 py-1 text-xs font-bold rounded ${timeframe === tf ? 'bg-slate-600 text-white' : 'text-slate-400 hover:text-white'}`}
                            >
                                {tf}
                            </button>
                        ))}
                    </div>
                </div>

                <div className="flex items-center gap-2">
                    <button onClick={() => setShowExport(true)} className="p-2 hover:bg-slate-800 rounded text-slate-400"><Save size={18} /></button>
                    <button className="p-2 hover:bg-slate-800 rounded text-slate-400"><Settings size={18} /></button>
                    <button className="p-2 hover:bg-slate-800 rounded text-slate-400"><Maximize2 size={18} /></button>
                </div>
            </div>

            {/* Main Workspace */}
            <div className="flex-1 relative overflow-hidden">
                <DrawingToolbar activeTool={activeTool} onSelectTool={setActiveTool} />
                
                {/* Chart Area */}
                {loading ? (
                    <div className="absolute inset-0 flex items-center justify-center">
                        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-cyan-500"></div>
                    </div>
                ) : (
                    <div className="w-full h-full p-4 pl-12">
                         <ResponsiveContainer width="100%" height="100%">
                            <AreaChart 
                                data={data} 
                                onClick={handleChartClick}
                                margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                            >
                                <defs>
                                    <linearGradient id="colorClose" x1="0" y1="0" x2="0" y2="1">
                                        <stop offset="5%" stopColor="#8884d8" stopOpacity={0.3}/>
                                        <stop offset="95%" stopColor="#8884d8" stopOpacity={0}/>
                                    </linearGradient>
                                </defs>
                                <XAxis dataKey="dateStr" tick={{fontSize: 10}} minTickGap={50} />
                                <YAxis domain={['auto', 'auto']} tick={{fontSize: 10}} orientation="right" />
                                <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                                <Tooltip 
                                    contentStyle={{backgroundColor: '#0f172a', borderColor: '#1e293b', color: '#f1f5f9'}}
                                    itemStyle={{color: '#8884d8'}}
                                />
                                <Area type="monotone" dataKey="close" stroke="#8884d8" fillOpacity={1} fill="url(#colorClose)" />
                                
                                {/* Mock Rendering of Drawings (Reference Lines for simplicty) */}
                                {drawings.map((d, i) => (
                                    <ReferenceLine key={i} y={d.start.y} stroke="red" strokeDasharray="3 3" />
                                ))}
                            </AreaChart>
                        </ResponsiveContainer>
                    </div>
                )}
            </div>
            
             <div className="absolute bottom-4 right-4 bg-slate-900/80 border border-slate-800 px-3 py-1 rounded text-[10px] text-slate-500 font-mono">
                O: {data[data.length-1]?.open.toFixed(2)} H: {data[data.length-1]?.high.toFixed(2)} L: {data[data.length-1]?.low.toFixed(2)} C: {data[data.length-1]?.close.toFixed(2)}
            </div>

            <ChartExportModal isOpen={showExport} onClose={() => setShowExport(false)} />
        </div>
    );
};

export default AdvancedChartBuilder;
