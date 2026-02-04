/**
 * Performance Monitor Widget
 * 
 * Displays Core Web Vitals and performance metrics.
 */

import React, { useState, useEffect } from 'react';
import performanceMonitor from '../../utils/performanceMonitor';
import './PerformanceMonitor.css';

export default function PerformanceMonitor() {
  const [metrics, setMetrics] = useState(() => performanceMonitor.getMetrics());
  const [overallScore, setOverallScore] = useState(() => performanceMonitor.getOverallScore());

  useEffect(() => {
    const updateMetrics = () => {
      setMetrics(performanceMonitor.getMetrics());
      setOverallScore(performanceMonitor.getOverallScore());
    };

    performanceMonitor.on('metric:lcp', updateMetrics);
    performanceMonitor.on('metric:fid', updateMetrics);
    performanceMonitor.on('metric:cls', updateMetrics);
    performanceMonitor.on('metric:fcp', updateMetrics);
    performanceMonitor.on('metric:ttfb', updateMetrics);

    // Update periodically
    const interval = setInterval(updateMetrics, 5000);

    return () => {
      performanceMonitor.off('metric:lcp', updateMetrics);
      performanceMonitor.off('metric:fid', updateMetrics);
      performanceMonitor.off('metric:cls', updateMetrics);
      performanceMonitor.off('metric:fcp', updateMetrics);
      performanceMonitor.off('metric:ttfb', updateMetrics);
      clearInterval(interval);
    };
  }, []);

  const getScoreColor = (score) => {
    switch (score) {
      case 'good': return '#28ca42';
      case 'needs-improvement': return '#ffbd2e';
      case 'poor': return '#ff5f57';
      default: return '#5a4a3a';
    }
  };

  const formatMetric = (value, unit = 'ms') => {
    if (value === null) return '';
    if (unit === 'ms') return `${Math.round(value)}ms`;
    return `${value.toFixed(2)}${unit}`;
  };

  const MetricCard = ({ label, value, unit, metric }) => {
    const score = performanceMonitor.getMetricScore(metric, value || 0);
    return (
      <div className="performance-metric-card">
        <div className="performance-metric-header">
          <span className="performance-metric-label">{label}</span>
          <span
            className="performance-metric-score"
            style={{ color: getScoreColor(score) }}
          >
            {score}
          </span>
        </div>
        <div className="performance-metric-value">
          {formatMetric(value, unit)}
        </div>
      </div>
    );
  };

  return (
    <div className="performance-monitor">
      <div className="performance-monitor-header">
        <h3>Performance Monitor</h3>
        <div
          className="performance-monitor-overall"
          style={{ color: getScoreColor(overallScore) }}
        >
          {overallScore.toUpperCase()}
        </div>
      </div>

      <div className="performance-monitor-content">
        <div className="performance-metrics-grid">
          <MetricCard
            label="LCP"
            value={metrics.LCP}
            unit="ms"
            metric="LCP"
          />
          <MetricCard
            label="FID"
            value={metrics.FID}
            unit="ms"
            metric="FID"
          />
          <MetricCard
            label="CLS"
            value={metrics.CLS}
            unit=""
            metric="CLS"
          />
          <MetricCard
            label="FCP"
            value={metrics.FCP}
            unit="ms"
            metric="FCP"
          />
          <MetricCard
            label="TTFB"
            value={metrics.TTFB}
            unit="ms"
            metric="TTFB"
          />
        </div>

        <div className="performance-monitor-info">
          <p className="performance-monitor-note">
            Core Web Vitals are measured automatically. Scores update as metrics become available.
          </p>
        </div>
      </div>
    </div>
  );
}

