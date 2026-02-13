import React from 'react';
import { AreaChart, Area, XAxis, Tooltip, ResponsiveContainer } from 'recharts';

const TrendVelocityChart = ({ data, color = "#8b5cf6" }) => {
    // Generate simple mock historical data based on current velocity if no history provided
    const chartData = data || Array.from({ length: 10 }, (_, i) => ({
        time: i,
        val: Math.random() * 100 + (i * 10)
    }));

    return (
        <div className="h-20 w-full">
            <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={chartData}>
                    <defs>
                        <linearGradient id={`gradient-${color}`} x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor={color} stopOpacity={0.3}/>
                            <stop offset="95%" stopColor={color} stopOpacity={0}/>
                        </linearGradient>
                    </defs>
                    <Tooltip cursor={false} content={<></>} />
                    <Area 
                        type="monotone" 
                        dataKey="val" 
                        stroke={color} 
                        fillOpacity={1} 
                        fill={`url(#gradient-${color})`} 
                        strokeWidth={2}
                    />
                </AreaChart>
            </ResponsiveContainer>
        </div>
    );
};

export default TrendVelocityChart;
