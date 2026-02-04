import React, { useRef, useState, useEffect } from 'react';
import { Download, Play, Pause, TrendingUp, AlertTriangle } from 'lucide-react';
import './RelativeStrength.css';

/**
 * Relative Strength Chart (Phase 6)
 * 
 * Canvas-based chart comparing strategy vs benchmark with regime shift detection.
 */
const RelativeStrength = () => {
    const canvasRef = useRef(null);
    const [isPlaying, setIsPlaying] = useState(false);
    const [regimeShifts, setRegimeShifts] = useState([
        { start: '2025-03-01', end: '2025-04-15', correlation: 0.32 },
        { start: '2025-09-10', end: '2025-10-05', correlation: 0.41 },
    ]);

    // Mock equity curve data
    const generateCurve = (volatility, trend) => {
        let value = 100;
        return Array.from({ length: 365 }, (_, i) => {
            value += (Math.random() - 0.5) * volatility + trend;
            return { day: i, value };
        });
    };

    const [strategyCurve] = useState(() => generateCurve(2, 0.1));
    const [benchmarkCurve] = useState(() => generateCurve(1.5, 0.08));

    useEffect(() => {
        if (!canvasRef.current) return;

        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;

        // Clear
        ctx.fillStyle = 'var(--bg-surface)';
        ctx.fillRect(0, 0, width, height);

        // Find bounds
        const allValues = [...strategyCurve, ...benchmarkCurve].map(d => d.value);
        const minVal = Math.min(...allValues) - 5;
        const maxVal = Math.max(...allValues) + 5;

        const xScale = (day) => (day / 365) * (width - 60) + 40;
        const yScale = (val) => height - 30 - ((val - minVal) / (maxVal - minVal)) * (height - 60);

        // Draw regime shift zones
        ctx.fillStyle = 'rgba(251, 191, 36, 0.15)';
        regimeShifts.forEach(shift => {
            const startDay = new Date(shift.start).getDate() + new Date(shift.start).getMonth() * 30;
            const endDay = new Date(shift.end).getDate() + new Date(shift.end).getMonth() * 30;
            ctx.fillRect(xScale(startDay), 30, xScale(endDay) - xScale(startDay), height - 60);
        });

        // Draw benchmark curve (thinner)
        ctx.strokeStyle = '#60a5fa';
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        benchmarkCurve.forEach((d, i) => {
            if (i === 0) ctx.moveTo(xScale(d.day), yScale(d.value));
            else ctx.lineTo(xScale(d.day), yScale(d.value));
        });
        ctx.stroke();

        // Draw strategy curve (bold)
        ctx.strokeStyle = '#4ade80';
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        strategyCurve.forEach((d, i) => {
            if (i === 0) ctx.moveTo(xScale(d.day), yScale(d.value));
            else ctx.lineTo(xScale(d.day), yScale(d.value));
        });
        ctx.stroke();

    }, [strategyCurve, benchmarkCurve, regimeShifts]);

    const finalStrategy = strategyCurve[strategyCurve.length - 1]?.value || 100;
    const finalBenchmark = benchmarkCurve[benchmarkCurve.length - 1]?.value || 100;
    const outperformance = ((finalStrategy - finalBenchmark) / finalBenchmark * 100).toFixed(2);

    return (
        <div className="relative-strength">
            <div className="widget-header">
                <h3>Relative Strength</h3>
                <div className="header-actions">
                    <button className="action-btn" onClick={() => setIsPlaying(!isPlaying)}>
                        {isPlaying ? <Pause size={14} /> : <Play size={14} />}
                    </button>
                    <button className="action-btn">
                        <Download size={14} /> PDF
                    </button>
                </div>
            </div>

            {regimeShifts.length > 0 && (
                <div className="regime-alert">
                    <AlertTriangle size={12} />
                    <span>{regimeShifts.length} Regime Shift(s) Detected</span>
                </div>
            )}

            <canvas ref={canvasRef} width={600} height={250}></canvas>

            <div className="chart-legend">
                <div className="legend-item">
                    <span className="legend-color strategy"></span>
                    <span>Strategy: {finalStrategy.toFixed(1)}</span>
                </div>
                <div className="legend-item">
                    <span className="legend-color benchmark"></span>
                    <span>Benchmark: {finalBenchmark.toFixed(1)}</span>
                </div>
                <div className={`outperformance ${parseFloat(outperformance) >= 0 ? 'positive' : 'negative'}`}>
                    <TrendingUp size={12} />
                    {outperformance}% Alpha
                </div>
            </div>
        </div>
    );
};

export default RelativeStrength;
