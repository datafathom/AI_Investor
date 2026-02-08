import React, { useState, useEffect } from 'react';
import './LatencyHeatmapWidget.css';
import LatencyHistogram from '../charts/LatencyHistogram';

const LatencyHeatmapWidget = () => {
    const [summary, setSummary] = useState(null);
    const [loading, setLoading] = useState(true);
    const [selectedEndpoint, setSelectedEndpoint] = useState(null);
    const [histogram, setHistogram] = useState(null);

    useEffect(() => {
        fetchSummary();
        const interval = setInterval(fetchSummary, 60000);
        return () => clearInterval(interval);
    }, []);

    const fetchSummary = async () => {
        try {
            const response = await fetch('/api/v1/admin/latency/summary');
            const data = await response.json();
            setSummary(data);
        } catch (error) {
            console.error("Error fetching latency summary:", error);
        } finally {
            setLoading(false);
        }
    };

    const fetchHistogram = async (path) => {
        setSelectedEndpoint(path);
        setHistogram(null);
        try {
            const response = await fetch(`/api/v1/admin/latency/endpoints/${encodeURIComponent(path)}/histogram`);
            const data = await response.json();
            setHistogram(data);
        } catch (error) {
            console.error("Error fetching histogram:", error);
        }
    };

    const getStatusClass = (val) => {
        if (val < 100) return 'fast';
        if (val < 500) return 'moderate';
        return 'slow';
    };

    if (loading) return <div className="latency-loading">ANALYZING_NETWORK_LATENCY...</div>;

    return (
        <div className="latency-heatmap-widget">
            <header className="widget-header">
                <h3>LATENCY_HEATMAP</h3>
                <span className="refresh-rate">60S_POLL</span>
            </header>

            <div className="heatmap-grid">
                <div className="grid-header">
                    <span>ENDPOINT</span>
                    <span>P50</span>
                    <span>P95</span>
                    <span>P99</span>
                    <span>COUNT</span>
                </div>
                <div className="grid-body">
                    {summary?.endpoints.map((ep, i) => (
                        <div 
                            key={i} 
                            className={`grid-row ${selectedEndpoint === ep.path ? 'selected' : ''}`}
                            onClick={() => fetchHistogram(ep.path)}
                        >
                            <span className="path" title={ep.path}>{ep.path}</span>
                            <span className={`val ${getStatusClass(ep.p50)}`}>{ep.p50}ms</span>
                            <span className={`val ${getStatusClass(ep.p95)}`}>{ep.p95}ms</span>
                            <span className={`val ${getStatusClass(ep.p99)}`}>{ep.p99}ms</span>
                            <span className="count">{ep.count}</span>
                        </div>
                    ))}
                </div>
            </div>

            {selectedEndpoint && (
                <div className="latency-drilldown">
                    <h4>DISTRIBUTION: {selectedEndpoint}</h4>
                    {histogram ? (
                        <LatencyHistogram data={histogram.buckets} />
                    ) : (
                        <div className="drilldown-loading">CALCULATING_BUCKETS...</div>
                    )}
                </div>
            )}
        </div>
    );
};

export default LatencyHeatmapWidget;
