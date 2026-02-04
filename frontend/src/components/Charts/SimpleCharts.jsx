import React from 'react';
import { BarChart, PieChart, LineChart, AreaChart, ScatterChart, XAxis, YAxis, CartesianGrid, Tooltip, Legend, Bar, Pie, Line, Area, Scatter, Cell, ResponsiveContainer } from 'recharts';

// --- 1. Reusable Bar Chart ---
export const SimpleBarChart = React.memo(({ data, width = 600, height = 400, colorScale = null }) => {
    // Data format expected: [{ label: 'Series A', values: [{x: 'A', y: 10}, {x: 'B', y: 5}] }]
    // Convert to recharts format: [{ name: 'A', 'Series A': 10, 'Series B': 5 }]

    const defaultColors = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#8dd1e1', '#d084d0'];

    // Transform data to recharts format
    const transformedData = React.useMemo(() => {
        if (!data || data.length === 0) return [];

        // Get all unique x values
        const allXValues = new Set();
        data.forEach(series => {
            series.values?.forEach(point => {
                allXValues.add(point.x);
            });
        });

        // Create data points for each x value
        const result = Array.from(allXValues).map(x => {
            const point = { name: x };
            data.forEach(series => {
                const value = series.values?.find(v => v.x === x);
                point[series.label] = value?.y || 0;
            });
            return point;
        });

        return result;
    }, [data]);

    const colors = colorScale || defaultColors;

    return (
        <div className="chart-container bar-chart" style={{ width: '100%', height: '100%', padding: 0, margin: 0 }}>
            <ResponsiveContainer width="100%" height="100%">
                <BarChart data={transformedData} margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    {(data || []).map((series, index) => (
                        <Bar
                            key={series.label}
                            dataKey={series.label}
                            fill={colors[index % colors.length]}
                        />
                    ))}
                </BarChart>
            </ResponsiveContainer>
        </div>
    );
}, (prevProps, nextProps) => {
    // Only re-render if data or dimensions change
    return prevProps.data === nextProps.data &&
        prevProps.width === nextProps.width &&
        prevProps.height === nextProps.height &&
        prevProps.colorScale === nextProps.colorScale;
});

SimpleBarChart.displayName = 'SimpleBarChart';

// --- 2. Reusable Pie Chart ---
export const SimplePieChart = React.memo(({ data, width = 600, height = 400 }) => {
    // Data format expected: { label: 'Series A', values: [{x: 'Item 1', y: 10}, {x: 'Item 2', y: 5}] }

    const defaultColors = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#8dd1e1', '#d084d0'];

    // Transform to recharts format
    const transformedData = React.useMemo(() => {
        if (!data?.values) return [];
        return data.values.map(item => ({
            name: item.x,
            value: item.y
        }));
    }, [data]);

    const colors = defaultColors;

    return (
        <div className="chart-container pie-chart" style={{ width: '100%', height: '100%', padding: 0, margin: 0 }}>
            <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                    <Pie
                        data={transformedData}
                        cx="50%"
                        cy="50%"
                        labelLine={false}
                        label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                        outerRadius="80%"
                        fill="#8884d8"
                        dataKey="value"
                    >
                        {transformedData.map((entry, index) => (
                            <Cell key={`cell-${index}`} fill={colors[index % colors.length]} />
                        ))}
                    </Pie>
                    <Tooltip />
                </PieChart>
            </ResponsiveContainer>
        </div>
    );
}, (prevProps, nextProps) => {
    return prevProps.data === nextProps.data &&
        prevProps.width === nextProps.width &&
        prevProps.height === nextProps.height;
});

SimplePieChart.displayName = 'SimplePieChart';

// --- 3. Reusable Line Chart ---
export const SimpleLineChart = React.memo(({ data, width = 600, height = 400 }) => {
    // Data format expected: [{ label: 'Series A', values: [{x: new Date(2020, 1, 1), y: 10}, ...] }]

    const defaultColors = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#8dd1e1', '#d084d0'];

    // Transform data to recharts format
    const transformedData = React.useMemo(() => {
        if (!data || data.length === 0) return [];

        const allXValues = new Set();
        data.forEach(series => {
            series.values?.forEach(point => {
                allXValues.add(point.x);
            });
        });

        const result = Array.from(allXValues).map(x => {
            const point = { name: x instanceof Date ? x.toLocaleDateString() : x };
            data.forEach(series => {
                const value = series.values?.find(v => v.x === x);
                point[series.label] = value?.y || 0;
            });
            return point;
        });

        return result;
    }, [data]);

    const colors = defaultColors;

    return (
        <div className="chart-container line-chart" style={{ width: '100%', height: '100%', padding: 0, margin: 0 }}>
            <ResponsiveContainer width="100%" height="100%">
                <LineChart data={transformedData} margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    {(data || []).map((series, index) => (
                        <Line
                            key={`${series.label}-${index}`}
                            type="monotone"
                            dataKey={series.label}
                            stroke={colors[index % colors.length]}
                        />
                    ))}
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}, (prevProps, nextProps) => {
    return prevProps.data === nextProps.data &&
        prevProps.width === nextProps.width &&
        prevProps.height === nextProps.height;
});

SimpleLineChart.displayName = 'SimpleLineChart';

// --- 4. Reusable Area Chart ---
export const SimpleAreaChart = React.memo(({ data, width = 600, height = 400 }) => {
    const defaultColors = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#8dd1e1', '#d084d0'];

    // Transform data to recharts format
    const transformedData = React.useMemo(() => {
        if (!data || data.length === 0) return [];

        const allXValues = new Set();
        data.forEach(series => {
            series.values?.forEach(point => {
                allXValues.add(point.x);
            });
        });

        const result = Array.from(allXValues).map(x => {
            const point = { name: x instanceof Date ? x.toLocaleDateString() : x };
            data.forEach(series => {
                const value = series.values?.find(v => v.x === x);
                point[series.label] = value?.y || 0;
            });
            return point;
        });

        return result;
    }, [data]);

    const colors = defaultColors;

    return (
        <div className="chart-container area-chart" style={{ width: '100%', height: '100%', padding: 0, margin: 0 }}>
            <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={transformedData} margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    {(data || []).map((series, index) => (
                        <Area
                            key={series.label}
                            type="monotone"
                            dataKey={series.label}
                            stackId="1"
                            stroke={colors[index % colors.length]}
                            fill={colors[index % colors.length]}
                        />
                    ))}
                </AreaChart>
            </ResponsiveContainer>
        </div>
    );
}, (prevProps, nextProps) => {
    return prevProps.data === nextProps.data &&
        prevProps.width === nextProps.width &&
        prevProps.height === nextProps.height;
});

SimpleAreaChart.displayName = 'SimpleAreaChart';

// --- 5. Reusable Scatter Plot ---
export const SimpleScatterPlot = React.memo(({ data, width = 600, height = 400 }) => {
    const defaultColors = ['#8884d8', '#82ca9d', '#ffc658', '#ff7300', '#8dd1e1', '#d084d0'];

    // Transform data to recharts format
    const transformedData = React.useMemo(() => {
        if (!data || data.length === 0) return [];

        return data.map(series => ({
            name: series.label,
            data: series.values?.map(point => ({ x: point.x, y: point.y })) || []
        }));
    }, [data]);

    const colors = defaultColors;

    return (
        <div className="chart-container scatter-plot" style={{ width: '100%', height: '100%', padding: 0, margin: 0 }}>
            <ResponsiveContainer width="100%" height="100%">
                <ScatterChart margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" dataKey="x" name="X Axis" />
                    <YAxis type="number" dataKey="y" name="Y Axis" />
                    <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                    <Legend />
                    {transformedData.map((series, index) => (
                        <Scatter
                            key={series.name}
                            name={series.name}
                            data={series.data}
                            fill={colors[index % colors.length]}
                        />
                    ))}
                </ScatterChart>
            </ResponsiveContainer>
        </div>
    );
}, (prevProps, nextProps) => {
    return prevProps.data === nextProps.data &&
        prevProps.width === nextProps.width &&
        prevProps.height === nextProps.height;
});

SimpleScatterPlot.displayName = 'SimpleScatterPlot';

// --- 6. Moving Average Chart (Derived Component) ---
export const MovingAverageChart = React.memo(({ rawData, windowSize = 5, width = 600, height = 400 }) => {
    // This component calculates the moving average from raw data and renders a LineChart

    // 1. Helper to calculate SMA
    const calculateSMA = (data, window) => {
        let smaData = [];
        for (let i = 0; i < data.length; i++) {
            if (i < window - 1) continue; // Need enough data points for the window

            let sum = 0;
            for (let j = 0; j < window; j++) {
                sum += data[i - j].y;
            }
            smaData.push({
                x: data[i].x,
                y: sum / window
            });
        }
        return smaData;
    };

    // 2. Prepare Data Structure for Recharts
    const chartData = React.useMemo(() => {
        const allXValues = new Set();
        rawData.forEach(point => allXValues.add(point.x));
        const smaData = calculateSMA(rawData, windowSize);
        smaData.forEach(point => allXValues.add(point.x));

        return Array.from(allXValues).map(x => {
            const rawPoint = rawData.find(p => p.x === x);
            const smaPoint = smaData.find(p => p.x === x);
            return {
                name: x instanceof Date ? x.toLocaleDateString() : x,
                'Raw Data': rawPoint?.y || null,
                [`Moving Average (${windowSize})`]: smaPoint?.y || null
            };
        });
    }, [rawData, windowSize]);

    return (
        <div className="chart-container ma-chart" style={{ width: '100%', height: '100%', padding: 0, margin: 0 }}>
            <ResponsiveContainer width="100%" height="100%">
                <LineChart data={chartData} margin={{ top: 5, right: 5, left: 5, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="name" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Line type="monotone" dataKey="Raw Data" stroke="#ccc" />
                    <Line type="monotone" dataKey={`Moving Average (${windowSize})`} stroke="#ff7f0e" />
                </LineChart>
            </ResponsiveContainer>
        </div>
    );
}, (prevProps, nextProps) => {
    return prevProps.rawData === nextProps.rawData &&
        prevProps.windowSize === nextProps.windowSize &&
        prevProps.width === nextProps.width &&
        prevProps.height === nextProps.height;
});

MovingAverageChart.displayName = 'MovingAverageChart';

// --- 7. Waveform Chart (Canvas-based for performance) ---
export const AudioWaveform = React.memo(({ data, width = 1000, height = 200 }) => {
    // Data should be normalized between [0, 1]
    const canvasRef = React.useRef(null);
    const containerRef = React.useRef(null);

    // Draw waveform on canvas for better performance with high-frequency updates
    React.useEffect(() => {
        const canvas = canvasRef.current;
        const container = containerRef.current;
        if (!canvas || !container || !data || data.length === 0) return;

        const ctx = canvas.getContext('2d');
        const rect = container.getBoundingClientRect();
        const canvasWidth = rect.width;
        const canvasHeight = rect.height;

        // Set canvas size
        canvas.width = canvasWidth;
        canvas.height = canvasHeight;

        // Clear canvas
        ctx.clearRect(0, 0, canvasWidth, canvasHeight);

        // Create gradient
        const gradient = ctx.createLinearGradient(0, 0, canvasWidth, 0);
        gradient.addColorStop(0, '#eb1785');
        gradient.addColorStop(1, '#ff7b16');

        // Draw grid lines
        ctx.strokeStyle = 'rgba(0, 0, 0, 0.1)';
        ctx.lineWidth = 1;
        for (let i = 0; i <= 4; i++) {
            const y = (canvasHeight / 4) * i;
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(canvasWidth, y);
            ctx.stroke();
        }

        // Draw waveform
        const stepX = canvasWidth / data.length;
        const centerY = canvasHeight / 2;

        ctx.strokeStyle = gradient;
        ctx.fillStyle = gradient;
        ctx.lineWidth = 2;

        // Draw area
        ctx.beginPath();
        ctx.moveTo(0, centerY);

        for (let i = 0; i < data.length; i++) {
            const x = i * stepX;
            const value = Math.max(0, Math.min(1, data[i])); // Clamp between 0 and 1
            const amplitude = (value * canvasHeight) / 2;
            const y = centerY - amplitude;
            ctx.lineTo(x, y);
        }

        for (let i = data.length - 1; i >= 0; i--) {
            const x = i * stepX;
            const value = Math.max(0, Math.min(1, data[i]));
            const amplitude = (value * canvasHeight) / 2;
            const y = centerY + amplitude;
            ctx.lineTo(x, y);
        }

        ctx.closePath();
        ctx.fill();

        // Draw stroke
        ctx.beginPath();
        ctx.moveTo(0, centerY);
        for (let i = 0; i < data.length; i++) {
            const x = i * stepX;
            const value = Math.max(0, Math.min(1, data[i]));
            const amplitude = (value * canvasHeight) / 2;
            const y = centerY - amplitude;
            ctx.lineTo(x, y);
        }
        ctx.stroke();

    }, [data, width, height]);

    return (
        <div
            ref={containerRef}
            className="chart-container waveform"
            style={{ width: '100%', height: '100%', padding: 0, margin: 0, position: 'relative' }}
        >
            <canvas
                ref={canvasRef}
                style={{ width: '100%', height: '100%', display: 'block' }}
            />
        </div>
    );
}, (prevProps, nextProps) => {
    // Only re-render if data reference changes (data array itself)
    // The canvas will redraw on data changes via useEffect
    return prevProps.data === nextProps.data &&
        prevProps.width === nextProps.width &&
        prevProps.height === nextProps.height;
});

AudioWaveform.displayName = 'AudioWaveform';

