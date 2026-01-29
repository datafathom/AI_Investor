import React from 'react';
import { Treemap, ResponsiveContainer, Tooltip } from 'recharts';

const PortfolioTreeMap = ({ data, height = 400 }) => {
    // Default mock data if none provided
    const defaultData = [
        {
            name: 'Technology',
            children: [
                { name: 'AAPL', size: 1200000, value: 0.05 },
                { name: 'MSFT', size: 950000, value: 0.03 },
                { name: 'NVDA', size: 1500000, value: 0.12 },
            ],
        },
        {
            name: 'Finance',
            children: [
                { name: 'JPM', size: 600000, value: 0.01 },
                { name: 'GS', size: 400000, value: -0.02 },
            ],
        },
        {
            name: 'Crypto',
            children: [
                { name: 'BTC', size: 2500000, value: 0.15 },
                { name: 'ETH', size: 1200000, value: 0.08 },
            ],
        },
    ];

    const chartData = data || defaultData;

    const COLORS = [
        'hsl(var(--primary-h), 70%, 50%)',
        'hsl(var(--accent-h), 70%, 50%)',
        'hsl(var(--success-h), 70%, 50%)',
        'hsl(var(--warning-h), 70%, 50%)',
        'hsl(var(--danger-h), 70%, 50%)',
    ];

    const CustomizedContent = (props) => {
        const { root, depth, x, y, width, height, index, payload, name } = props;

        return (
            <g>
                <rect
                    x={x}
                    y={y}
                    width={width}
                    height={height}
                    style={{
                        fill: depth < 2 ? COLORS[index % COLORS.length] : 'rgba(255, 255, 255, 0.05)',
                        stroke: 'rgba(255,255,255,0.1)',
                        strokeWidth: 2 / (depth + 1),
                        strokeOpacity: 1,
                    }}
                    className="transition-all duration-300 hover:brightness-125"
                />
                {width > 30 && height > 20 && (
                    <text
                        x={x + width / 2}
                        y={y + height / 2}
                        textAnchor="middle"
                        fill="#fff"
                        fontSize={depth === 1 ? 14 : 10}
                        fontWeight={depth === 1 ? "bold" : "normal"}
                        style={{ pointerEvents: 'none', filter: 'drop-shadow(0 1px 2px rgba(0,0,0,0.5))' }}
                    >
                        {name}
                    </text>
                )}
            </g>
        );
    };

    return (
        <div className="portfolio-treemap-container glass-premium p-4 rounded-xl" style={{ height }}>
            <h3 className="text-sm font-semibold mb-4 flex items-center gap-2 text-primary-light">
                <span className="w-2 h-2 rounded-full bg-accent animate-pulse" />
                Portfolio Allocation Treemap
            </h3>
            <ResponsiveContainer width="100%" height="85%">
                <Treemap
                    data={chartData}
                    dataKey="size"
                    ratio={4 / 3}
                    stroke="#fff"
                    fill="var(--color-primary)"
                    content={<CustomizedContent />}
                >
                    <Tooltip 
                        contentStyle={{ 
                            backgroundColor: 'rgba(15, 23, 42, 0.9)', 
                            border: '1px solid rgba(255,255,255,0.1)',
                            borderRadius: '8px',
                            backdropFilter: 'blur(8px)'
                        }}
                    />
                </Treemap>
            </ResponsiveContainer>
        </div>
    );
};

export default PortfolioTreeMap;
