/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Market/PriceChart.jsx
 * ROLE: Historical Price Chart Widget
 * PURPOSE: Renders historical OHLCV data with interactive zoom/pan using Recharts.
 *          
 * INTEGRATION POINTS:
 *     - marketStore: Zustand state management for history data
 *     - /api/v1/market/history/{symbol}: Backend API endpoint
 *     
 * PROPS:
 *     - symbol (string, required): Stock ticker symbol
 *     - period (string, default: 'compact'): 'compact' or 'full'
 *     - height (number, default: 300): Chart height in pixels
 *     - showVolume (boolean, default: true): Show volume bars
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * ==============================================================================
 */

import React, { useEffect, useState } from 'react';
import { useMarketStore } from '../../stores/marketStore';
import {
    LineChart, Line, XAxis, YAxis, CartesianGrid, 
    Tooltip, ResponsiveContainer, AreaChart, Area, BarChart, Bar
} from 'recharts';
import './Market.css';

/**
 * Loading Skeleton
 */
const ChartSkeleton = ({ height }) => (
    <div className="price-chart price-chart--loading" style={{ height }}>
        <div className="price-chart__skeleton"></div>
    </div>
);

/**
 * PriceChart Component
 */
const PriceChart = ({ 
    symbol, 
    period = 'compact', 
    height = 300,
    showVolume = true 
}) => {
    const { getHistory, fetchHistory, isLoading, getError } = useMarketStore();
    const [chartType, setChartType] = useState('area'); // area, line
    
    const historyData = getHistory(symbol);
    const loading = isLoading('history');
    const error = getError('history');

    useEffect(() => {
        if (symbol) {
            fetchHistory(symbol, period, true);
        }
    }, [symbol, period, fetchHistory]);

    if (loading && !historyData) return <ChartSkeleton height={height} />;
    
    if (error && !historyData) {
        return (
            <div className="price-chart price-chart--error" style={{ height }}>
                <span>⚠️ {error}</span>
            </div>
        );
    }

    if (!historyData?.bars?.length) {
        return (
            <div className="price-chart price-chart--empty" style={{ height }}>
                <span>No data available for {symbol}</span>
            </div>
        );
    }

    // Transform data for Recharts (reverse to show oldest first)
    const chartData = [...historyData.bars]
        .reverse()
        .slice(-100) // Last 100 data points
        .map(bar => ({
            date: new Date(bar.timestamp).toLocaleDateString('en-US', { 
                month: 'short', 
                day: 'numeric' 
            }),
            close: bar.close,
            open: bar.open,
            high: bar.high,
            low: bar.low,
            volume: bar.volume,
            adjustedClose: bar.adjusted_close
        }));

    const minPrice = Math.min(...chartData.map(d => d.low)) * 0.995;
    const maxPrice = Math.max(...chartData.map(d => d.high)) * 1.005;

    const CustomTooltip = ({ active, payload, label }) => {
        if (active && payload && payload.length) {
            const data = payload[0].payload;
            return (
                <div className="price-chart__tooltip">
                    <p className="price-chart__tooltip-date">{label}</p>
                    <p>Close: ${data.close?.toFixed(2)}</p>
                    <p>Open: ${data.open?.toFixed(2)}</p>
                    <p>High: ${data.high?.toFixed(2)}</p>
                    <p>Low: ${data.low?.toFixed(2)}</p>
                    {showVolume && <p>Vol: {(data.volume / 1e6).toFixed(2)}M</p>}
                </div>
            );
        }
        return null;
    };

    return (
        <div className="price-chart" style={{ height: showVolume ? height + 80 : height }}>
            <div className="price-chart__header">
                <h3 className="price-chart__title">{symbol} Price History</h3>
                <div className="price-chart__controls">
                    <button 
                        className={`price-chart__btn ${chartType === 'area' ? 'active' : ''}`}
                        onClick={() => setChartType('area')}
                    >
                        Area
                    </button>
                    <button 
                        className={`price-chart__btn ${chartType === 'line' ? 'active' : ''}`}
                        onClick={() => setChartType('line')}
                    >
                        Line
                    </button>
                </div>
            </div>
            
            <ResponsiveContainer width="100%" height={height - 40}>
                {chartType === 'area' ? (
                    <AreaChart data={chartData}>
                        <defs>
                            <linearGradient id="colorPrice" x1="0" y1="0" x2="0" y2="1">
                                <stop offset="5%" stopColor="var(--accent-color, #00d4ff)" stopOpacity={0.4}/>
                                <stop offset="95%" stopColor="var(--accent-color, #00d4ff)" stopOpacity={0}/>
                            </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color, #333)" />
                        <XAxis 
                            dataKey="date" 
                            tick={{ fill: 'var(--text-secondary, #888)', fontSize: 10 }}
                            interval="preserveStartEnd"
                        />
                        <YAxis 
                            domain={[minPrice, maxPrice]}
                            tick={{ fill: 'var(--text-secondary, #888)', fontSize: 10 }}
                            tickFormatter={(v) => `$${v.toFixed(0)}`}
                        />
                        <Tooltip content={<CustomTooltip />} />
                        <Area 
                            type="monotone" 
                            dataKey="close" 
                            stroke="var(--accent-color, #00d4ff)" 
                            fill="url(#colorPrice)"
                            strokeWidth={2}
                        />
                    </AreaChart>
                ) : (
                    <LineChart data={chartData}>
                        <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color, #333)" />
                        <XAxis 
                            dataKey="date" 
                            tick={{ fill: 'var(--text-secondary, #888)', fontSize: 10 }}
                            interval="preserveStartEnd"
                        />
                        <YAxis 
                            domain={[minPrice, maxPrice]}
                            tick={{ fill: 'var(--text-secondary, #888)', fontSize: 10 }}
                            tickFormatter={(v) => `$${v.toFixed(0)}`}
                        />
                        <Tooltip content={<CustomTooltip />} />
                        <Line 
                            type="monotone" 
                            dataKey="close" 
                            stroke="var(--accent-color, #00d4ff)" 
                            strokeWidth={2}
                            dot={false}
                        />
                    </LineChart>
                )}
            </ResponsiveContainer>

            {showVolume && (
                <ResponsiveContainer width="100%" height={60}>
                    <BarChart data={chartData}>
                        <XAxis dataKey="date" hide />
                        <YAxis hide />
                        <Bar 
                            dataKey="volume" 
                            fill="var(--text-secondary, #555)" 
                            opacity={0.5}
                        />
                    </BarChart>
                </ResponsiveContainer>
            )}
        </div>
    );
};

export default PriceChart;
