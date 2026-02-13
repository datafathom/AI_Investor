import React, { useState, useEffect } from 'react';
import apiClient from '../../services/apiClient';
import { Layers, RotateCw, ZoomIn, Download } from 'lucide-react';
import { ResponsiveContainer, ScatterChart, Scatter, XAxis, YAxis, ZAxis, Tooltip } from 'recharts';

const GreeksSurface = () => {
    const [data, setData] = useState([]);
    const [metric, setMetric] = useState('delta');

    useEffect(() => {
        loadData();
    }, []);

    const loadData = async () => {
        try {
            const res = await apiClient.get('/options/AAPL/greeks/surface');
            if (res.data.success) {
                setData(res.data.data);
            }
        } catch (e) {
            console.error(e);
        }
    };

    return (
        <div className="p-8 h-full overflow-y-auto text-slate-200">
            <header className="mb-8 flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold text-white flex items-center gap-2">
                        <Layers className="text-pink-500" /> Greeks Surface (3D)
                    </h1>
                    <p className="text-slate-500">Volatility Surface & Risk Topography</p>
                </div>
                <div className="flex gap-2">
                    <select 
                        value={metric} 
                        onChange={e => setMetric(e.target.value)}
                        className="bg-slate-900 border border-slate-700 rounded px-3 py-2 text-white"
                    >
                        <option value="delta">Delta</option>
                        <option value="gamma">Gamma</option>
                        <option value="vega">Vega</option>
                    </select>
                </div>
            </header>

            <div className="bg-slate-900 border border-slate-800 rounded-xl p-6 h-[500px] relative">
                <div className="absolute top-6 right-6 flex gap-2">
                    <button className="p-2 bg-slate-800 rounded hover:bg-slate-700 text-white"><RotateCw size={18} /></button>
                    <button className="p-2 bg-slate-800 rounded hover:bg-slate-700 text-white"><ZoomIn size={18} /></button>
                    <button className="p-2 bg-slate-800 rounded hover:bg-slate-700 text-white"><Download size={18} /></button>
                </div>
                
                {data.length > 0 ? (
                    <ResponsiveContainer width="100%" height="100%">
                        <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
                            <XAxis type="number" dataKey="strike" name="Strike" stroke="#94a3b8" />
                            <YAxis type="category" dataKey="expiry" name="Expiry" stroke="#94a3b8" />
                            <ZAxis type="number" dataKey={metric} range={[50, 400]} name={metric} />
                            <Tooltip cursor={{ strokeDasharray: '3 3' }} contentStyle={{ backgroundColor: '#0f172a', borderColor: '#334155' }} />
                            <Scatter name="Greeks" data={data} fill="#ec4899" />
                        </ScatterChart>
                    </ResponsiveContainer>
                ) : (
                    <div className="flex items-center justify-center h-full text-slate-500">
                        Generating 3D Surface Mesh...
                    </div>
                )}
            </div>
        </div>
    );
};

export default GreeksSurface;
