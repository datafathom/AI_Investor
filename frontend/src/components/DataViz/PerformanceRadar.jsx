import React, { useMemo } from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine, Label } from 'recharts';
import { Card, CardContent, Typography } from '@mui/material';

// Dummy data for prototype
const generateData = () => {
  const data = [];
  for (let i = 0; i < 50; i++) {
    data.push({
      id: `Mission-${i}`,
      cost: Math.floor(Math.random() * 500), // Gas/API Cost
      profit: Math.floor(Math.random() * 2000) - 500, // P&L
      dept: Math.floor(Math.random() * 5)
    });
  }
  return data;
};

const CustomTooltip = ({ active, payload }) => {
  if (active && payload && payload.length) {
    const data = payload[0].payload;
    return (
      <div style={{ backgroundColor: 'rgba(255, 255, 255, 0.9)', padding: '10px', border: '1px solid #ccc' }}>
        <p style={{ fontWeight: 'bold' }}>{data.id}</p>
        <p>Cost: ${data.cost}</p>
        <p>Profit: ${data.profit}</p>
        <p style={{ color: data.profit > data.cost ? 'green' : 'red' }}>
          ROI: {((data.profit - data.cost) / data.cost * 100).toFixed(1)}%
        </p>
      </div>
    );
  }
  return null;
};

const PerformanceRadar = ({ data }) => {
  const chartData = useMemo(() => data || generateData(), [data]);

  return (
    <Card sx={{ height: '100%', bgcolor: '#fdf6e3' }}>
      <CardContent sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
        <Typography variant="h6" gutterBottom color="primary">
          ROI Efficiency Frontier
        </Typography>
        <div style={{ flex: 1, minHeight: 0 }}>
          <ResponsiveContainer width="100%" height="100%">
            <ScatterChart margin={{ top: 20, right: 20, bottom: 20, left: 20 }}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" dataKey="cost" name="Cost" unit="$">
                <Label value="Resource Cost (Gas/API)" offset={-10} position="insideBottom" />
              </XAxis>
              <YAxis type="number" dataKey="profit" name="Profit" unit="$">
                <Label value="Alpha Generated (USD)" angle={-90} position="insideLeft" />
              </YAxis>
              <Tooltip content={<CustomTooltip />} />
              
              {/* Leech Line: Cost > Profit */}
              <ReferenceLine segment={[{ x: 0, y: 0 }, { x: 2000, y: 2000 }]} stroke="red" strokeDasharray="3 3" label="Breakeven" />
              
              <Scatter name="Missions" data={chartData} fill="#8884d8">
                {chartData.map((entry, index) => (
                  <cell key={`cell-${index}`} fill={entry.profit < entry.cost ? '#dc322f' : '#859900'} />
                ))}
              </Scatter>
            </ScatterChart>
          </ResponsiveContainer>
        </div>
      </CardContent>
    </Card>
  );
};

export default PerformanceRadar;
