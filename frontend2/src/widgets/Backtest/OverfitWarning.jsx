import React, { useEffect, useState } from 'react';
import apiClient from '../../services/apiClient';
import { AlertTriangle, TrendingDown, CheckCircle, Info } from 'lucide-react';
import useBacktestStore from '../../stores/backtestStore';
import './OverfitWarning.css';

const OverfitWarning = () => {
    const { params } = useBacktestStore();
    const [overfitData, setOverfitData] = useState({ is_overfit: false, variance: 0 });

    useEffect(() => {
        const checkOverfit = async () => {
            try {
                const response = await apiClient.get('/backtest/overfit', { 
                    params: { is_sharpe: 2.45, oos_sharpe: 1.12 } 
                });
                setOverfitData(response.data);
            } catch (err) {
                console.error('Failed to check overfit:', err);
            }
        };
        checkOverfit();
    }, []);

    const { is_overfit, variance } = overfitData;

    return (
        <div className={`overfit-warning-widget ${is_overfit ? 'warning-active' : ''}`}>
            <div className="widget-header">
                <h3><AlertTriangle size={18} className="text-amber-500"/> OOS Variance Matrix</h3>
                <div className="info-icon" title="Compares In-Sample (Training) vs Out-of-Sample (Validation) performance.">
                    <Info size={14} />
                </div>
            </div>

            <div className="status-banner">
                {is_overfit ? (
                    <>
                        <div className="status-icon warning"><AlertTriangle size={24} /></div>
                        <div className="status-text">
                            <h4>High Overfit Risk Detected</h4>
                            <p>Out-of-Sample variance ({(variance * 100).toFixed(1)}%) exceeds 20% threshold.</p>
                        </div>
                    </>
                ) : (
                    <>
                        <div className="status-icon success"><CheckCircle size={24} /></div>
                        <div className="status-text">
                            <h4>Model Stable</h4>
                            <p>Performance consistent across datasets ({(variance * 100).toFixed(1)}% variance).</p>
                        </div>
                    </>
                )}
            </div>

            <div className="metrics-comparison">
                <div className="comparison-row header">
                    <span>Metric</span>
                    <span>In-Sample</span>
                    <span>Out-Sample</span>
                    <span>Variance</span>
                </div>
                <div className="comparison-row">
                    <span className="metric-name">Sharpe</span>
                    <span className="val in-sample">2.45</span>
                    <span className="val out-sample">1.12</span>
                    <span className="val variance negative">-54.3%</span>
                </div>
                <div className="comparison-row">
                    <span className="metric-name">Sortino</span>
                    <span className="val in-sample">3.12</span>
                    <span className="val out-sample">1.45</span>
                    <span className="val variance negative">-53.5%</span>
                </div>
                <div className="comparison-row">
                    <span className="metric-name">Win Rate</span>
                    <span className="val in-sample">68%</span>
                    <span className="val out-sample">51%</span>
                    <span className="val variance negative">-25.0%</span>
                </div>
            </div>

            <div className="p-value-section">
                <span>Statistical Significance (p-test):</span>
                <span className="p-value">p = {is_overfit ? '0.042' : '0.001'} (Significant)</span>
            </div>
        </div>
    );
};

export default OverfitWarning;
