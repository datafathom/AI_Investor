import React, { useRef, useEffect, useState } from 'react';
import { AlertTriangle, Info, Sliders, Loader2 } from 'lucide-react';
import useBacktestStore from '../../stores/backtestStore';
import './MonteCarlo.css';

/**
 * Monte Carlo Simulation Visualizer (Phase 14 -> 57)
 * 
 * Canvas-based 10K path visualization with quantile shading.
 */
const MonteCarlo = () => {
    const canvasRef = useRef(null);
    const { 
        simulationPaths, 
        quantiles, 
        ruinProbability, 
        params, 
        setParams, 
        runSimulation, 
        isSimulating 
    } = useBacktestStore();

    useEffect(() => {
        if (!canvasRef.current || quantiles.p50.length === 0) return;

        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;

        // Clear
        ctx.fillStyle = getComputedStyle(document.documentElement).getPropertyValue('--bg-surface-2').trim() || '#1a1a2e';
        ctx.fillRect(0, 0, width, height);

        const steps = quantiles.p50.length;
        
        // Dynamic scaling based on data
        const maxVal = Math.max(...quantiles.p95) * 1.1;
        const minVal = Math.min(...quantiles.p5) * 0.9;
        const range = maxVal - minVal;

        const xScale = (i) => (i / (steps - 1)) * (width - 60) + 40;
        const yScale = (v) => height - 30 - ((v - minVal) / range) * (height - 60);

        // Draw 95th percentile area (green)
        ctx.fillStyle = 'rgba(74, 222, 128, 0.15)';
        ctx.beginPath();
        ctx.moveTo(xScale(0), yScale(quantiles.p95[0]));
        quantiles.p95.forEach((v, i) => ctx.lineTo(xScale(i), yScale(v)));
        quantiles.p50.slice().reverse().forEach((v, i) => ctx.lineTo(xScale(steps - 1 - i), yScale(v)));
        ctx.closePath();
        ctx.fill();

        // Draw 5th percentile area (red)
        ctx.fillStyle = 'rgba(248, 113, 113, 0.15)';
        ctx.beginPath();
        ctx.moveTo(xScale(0), yScale(quantiles.p50[0]));
        quantiles.p50.forEach((v, i) => ctx.lineTo(xScale(i), yScale(v)));
        quantiles.p5.slice().reverse().forEach((v, i) => ctx.lineTo(xScale(steps - 1 - i), yScale(v)));
        ctx.closePath();
        ctx.fill();

        // Draw median line
        ctx.strokeStyle = '#60a5fa';
        ctx.lineWidth = 2;
        ctx.beginPath();
        quantiles.p50.forEach((v, i) => {
            if (i === 0) ctx.moveTo(xScale(i), yScale(v));
            else ctx.lineTo(xScale(i), yScale(v));
        });
        ctx.stroke();

        // Draw individual paths (sample)
        ctx.strokeStyle = 'rgba(255,255,255,0.05)';
        ctx.lineWidth = 0.5;
        simulationPaths.slice(0, 50).forEach(path => {
            ctx.beginPath();
            path.forEach((v, i) => {
                if (i === 0) ctx.moveTo(xScale(i), yScale(v));
                else ctx.lineTo(xScale(i), yScale(v));
            });
            ctx.stroke();
        });

    }, [quantiles, simulationPaths]);

    const handleRun = () => runSimulation();

    return (
        <div className="monte-carlo">
            <div className="widget-header">
                <h3>Monte Carlo Simulation</h3>
                <span className="path-count">{params.paths / 1000}K Paths</span>
            </div>

            <div className="canvas-container">
                <canvas ref={canvasRef} width={550} height={300}></canvas>
                {isSimulating && (
                    <div className="simulation-overlay">
                        <Loader2 className="spinning" size={32} />
                        <span>Simulating 10,000 Universes...</span>
                    </div>
                )}
            </div>

            <div className="controls-row">
                <div className="volatility-control">
                    <Sliders size={14} />
                    <span>Volatility: {(params.sigma * 100).toFixed(0)}%</span>
                    <input 
                        type="range" 
                        min="0.05" 
                        max="0.50" 
                        step="0.01" 
                        value={params.sigma}
                        onChange={(e) => setParams({ sigma: parseFloat(e.target.value) })}
                    />
                </div>
                <button className="run-btn" onClick={handleRun} disabled={isSimulating}>
                    {isSimulating ? 'Running...' : 'Run Simulation'}
                </button>
            </div>

            <div className="metrics-row">
                <div className="metric">
                    <span className="label">5th Percentile</span>
                    <span className="value negative">
                        {quantiles.p5.length > 0 ? `${((quantiles.p5[quantiles.p5.length-1] / 1000000 - 1) * 100).toFixed(1)}%` : '--'}
                    </span>
                </div>
                <div className="metric">
                    <span className="label">Median</span>
                    <span className="value">
                        {quantiles.p50.length > 0 ? `${((quantiles.p50[quantiles.p50.length-1] / 1000000 - 1) * 100).toFixed(1)}%` : '--'}
                    </span>
                </div>
                <div className="metric">
                    <span className="label">95th Percentile</span>
                    <span className="value positive">
                        {quantiles.p95.length > 0 ? `${((quantiles.p95[quantiles.p95.length-1] / 1000000 - 1) * 100).toFixed(1)}%` : '--'}
                    </span>
                </div>
            </div>

            <div className={`ruin-probability ${(ruinProbability * 100) > 5 ? 'danger' : ''}`}>
                <AlertTriangle size={14} />
                <span>Probability of Ruin (50% DD): {(ruinProbability * 100).toFixed(2)}%</span>
            </div>

            <div className="legend">
                <span className="legend-item green">95th Percentile</span>
                <span className="legend-item blue">Median</span>
                <span className="legend-item red">5th Percentile</span>
            </div>
        </div>
    );
};

export default MonteCarlo;
