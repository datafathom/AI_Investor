import React from 'react';
import { 
  BarChart, 
  Bar, 
  XAxis, 
  YAxis, 
  CartesianGrid, 
  Tooltip, 
  ResponsiveContainer, 
  Cell 
} from 'recharts';
import './GeneFrequencyPlot.css';

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    return (
      <div className="custom-tooltip" style={{ 
        backgroundColor: '#1a212c', 
        border: '1px solid #00f2ff', 
        padding: '12px',
        borderRadius: '8px'
      }}>
        <p style={{ margin: 0, color: '#00f2ff', fontWeight: 'bold' }}>{payload[0].payload.name}</p>
        <p style={{ margin: '4px 0 0', color: '#fff' }}>Frequency: {(payload[0].value * 100).toFixed(1)}%</p>
      </div>
    );
  }
  return null;
};

const GeneFrequencyPlot = ({ data }) => {
  // Mock data if none provided
  const plotData = data || [
    { name: 'RSI Period', frequency: 0.85, color: '#00f2ff' },
    { name: 'RSI Buy', frequency: 0.72, color: '#00d4ff' },
    { name: 'RSI Sell', frequency: 0.61, color: '#00b6ff' },
    { name: 'Stop Loss', frequency: 0.45, color: '#0098ff' },
    { name: 'Take Profit', frequency: 0.38, color: '#007aff' },
    { name: 'Leverage', frequency: 0.29, color: '#005cff' },
  ];

  return (
    <div className="gene-frequency-container">
      <div className="gene-frequency-header">
        <h3>Genetic Prevalence Matrix</h3>
        <div className="gene-frequency-legend">
          <div className="legend-item">
            <div className="legend-color" style={{ backgroundColor: '#00f2ff' }}></div>
            <span>Dominant</span>
          </div>
          <div className="legend-item">
            <div className="legend-color" style={{ backgroundColor: '#005cff' }}></div>
            <span>Recessive</span>
          </div>
        </div>
      </div>

      <div style={{ width: '100%', height: 300 }}>
        <ResponsiveContainer>
          <BarChart data={plotData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} />
            <XAxis 
              dataKey="name" 
              axisLine={false} 
              tickLine={false} 
            />
            <YAxis 
              axisLine={false} 
              tickLine={false} 
              tickFormatter={(val) => `${(val * 100)}%`}
            />
            <Tooltip content={<CustomTooltip />} cursor={{ fill: 'rgba(255, 255, 255, 0.05)' }} />
            <Bar dataKey="frequency" radius={[4, 4, 0, 0]}>
              {plotData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default GeneFrequencyPlot;
