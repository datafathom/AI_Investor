import React, { useEffect } from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, ZAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine } from 'recharts';
import { CloudRain, Leaf } from 'lucide-react';
import useImpactStore from '../../stores/impactStore';
import './CarbonScatter.css';

const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
        const data = payload[0].payload;
        return (
            <div className="bg-black/90 border border-gray-700 p-2 rounded text-xs shadow-xl">
                <div className="font-bold text-white mb-1">{data.ticker} ({data.sector})</div>
                <div className="text-gray-300">Alpha: <span className={data.alpha > 0 ? 'text-green-400' : 'text-red-400'}>{data.alpha}%</span></div>
                <div className="text-gray-300">Carbon: <span className="text-yellow-400">{data.carbon_intensity}</span> t/M</div>
            </div>
        );
    }
    return null;
};

const CarbonScatter = () => {
    const { carbonData, fetchCarbonData, isLoading } = useImpactStore();

    useEffect(() => {
        fetchCarbonData();
    }, []);

    if (isLoading || !carbonData) return <div className="carbon-scatter">Loading Carbon Data...</div>;

    const { footprint, scatter_data } = carbonData;

    return (
        <div className="carbon-scatter">
            <div className="scatter-header">
                <h3><CloudRain size={18} className="text-gray-400" /> Carbon vs Alpha</h3>
                <div className="footprint-summary">
                    <div className="fp-stat">
                        <small>Total Emissions</small>
                        <strong>{footprint?.total?.toFixed(1)} tons</strong>
                    </div>
                </div>
            </div>

            <div style={{ width: '100%', height: 200, flexGrow: 1 }}>
                <ResponsiveContainer>
                    <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 0 }}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                        <XAxis 
                            type="number" 
                            dataKey="carbon_intensity" 
                            name="Carbon Intensity" 
                            label={{ value: 'Intensity (tCO2e)', position: 'bottom', fill: '#666', fontSize: 10 }} 
                            stroke="#666"
                            fontSize={10}
                        />
                        <YAxis 
                            type="number" 
                            dataKey="alpha" 
                            name="Alpha" 
                            label={{ value: 'Alpha %', angle: -90, position: 'left', fill: '#666', fontSize: 10 }} 
                            stroke="#666"
                            fontSize={10}
                        />
                        <Tooltip content={<CustomTooltip />} cursor={{ strokeDasharray: '3 3' }} />
                        <ReferenceLine y={0} stroke="#444" />
                        <Scatter name="Holdings" data={scatter_data} fill="#8884d8">
                            {
                                scatter_data.map((entry, index) => (
                                    <cell key={`cell-${index}`} fill={entry.sector === 'Energy' ? '#ef4444' : '#60a5fa'} />
                                ))
                            }
                        </Scatter>
                    </ScatterChart>
                </ResponsiveContainer>
            </div>

            <button className="offset-btn">
                <Leaf size={14} className="inline mr-2" />
                Offset Portfolio Carbon (~${footprint?.cost?.toFixed(2)})
            </button>
        </div>
    );
};

export default CarbonScatter;
