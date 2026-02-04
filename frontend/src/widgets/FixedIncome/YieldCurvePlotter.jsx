import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import { useFixedIncomeStore } from '../../stores/fixedIncomeStore';
import './YieldCurvePlotter.css';

/**
 * Yield Curve Plotter Widget
 * 
 * Displays US Treasury yield curve with inversion detection.
 * Integrates with FixedIncomeService via store.
 */
const YieldCurvePlotter = () => {
    const svgRef = useRef(null);
    const { yieldCurve, isLoading } = useFixedIncomeStore();
    const [isInverted, setIsInverted] = useState(false);

    // Transform store data to D3 format
    const getYieldData = () => {
        if (!yieldCurve || !yieldCurve.rates) {
            // Fallback skeleton or empty state could be handled here
            // For now returning mock structure to prevent crash if data missing
            return [];
        }

        const maturityMap = {
            '1M': 1, '3M': 3, '6M': 6, 
            '1Y': 12, '2Y': 24, '3Y': 36, '5Y': 60, '7Y': 84, 
            '10Y': 120, '20Y': 240, '30Y': 360
        };

        return Object.entries(yieldCurve.rates)
            .map(([label, rate]) => ({
                label,
                yield: rate,
                maturity: maturityMap[label] || 0
            }))
            .sort((a, b) => a.maturity - b.maturity);
    };

    const yieldData = getYieldData();

    useEffect(() => {
        if (!yieldData.length) return;

        // Check for inversion (2Y > 10Y)
        const twoYear = yieldData.find(d => d.maturity === 24)?.yield || 0;
        const tenYear = yieldData.find(d => d.maturity === 120)?.yield || 0;
        setIsInverted(twoYear > tenYear);

        if (!svgRef.current) return;

        const svg = d3.select(svgRef.current);
        svg.selectAll('*').remove();

        const margin = { top: 20, right: 30, bottom: 50, left: 50 };
        const width = 500 - margin.left - margin.right;
        const height = 300 - margin.top - margin.bottom;

        const g = svg
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);

        // Scales
        const x = d3.scalePoint()
            .domain(yieldData.map(d => d.label))
            .range([0, width])
            .padding(0.5);

        const y = d3.scaleLinear()
            .domain([
                d3.min(yieldData, d => d.yield) - 0.5,
                d3.max(yieldData, d => d.yield) + 0.5
            ])
            .range([height, 0]);

        // Grid lines
        g.append('g')
            .attr('class', 'grid')
            .call(d3.axisLeft(y)
                .tickSize(-width)
                .tickFormat('')
            );

        // Axes
        g.append('g')
            .attr('class', 'axis axis-x')
            .attr('transform', `translate(0,${height})`)
            .call(d3.axisBottom(x));

        g.append('g')
            .attr('class', 'axis axis-y')
            .call(d3.axisLeft(y).tickFormat(d => `${d.toFixed(1)}%`));

        // Line generator
        const line = d3.line()
            .x(d => x(d.label))
            .y(d => y(d.yield))
            .curve(d3.curveMonotoneX);

        // Area fill
        const area = d3.area()
            .x(d => x(d.label))
            .y0(height)
            .y1(d => y(d.yield))
            .curve(d3.curveMonotoneX);

        g.append('path')
            .datum(yieldData)
            .attr('class', 'yield-area')
            .attr('d', area)
            .attr('fill', isInverted ? 'rgba(239, 68, 68, 0.1)' : 'rgba(59, 130, 246, 0.1)');

        // Line path
        g.append('path')
            .datum(yieldData)
            .attr('class', 'yield-line')
            .attr('d', line)
            .attr('fill', 'none')
            .attr('stroke', isInverted ? 'var(--color-bearish)' : 'var(--color-info)')
            .attr('stroke-width', 2);

        // Data points
        g.selectAll('.yield-point')
            .data(yieldData)
            .enter()
            .append('circle')
            .attr('class', 'yield-point')
            .attr('cx', d => x(d.label))
            .attr('cy', d => y(d.yield))
            .attr('r', 4)
            .attr('fill', isInverted ? 'var(--color-bearish)' : 'var(--color-info)')
            .attr('stroke', 'var(--bg-surface)')
            .attr('stroke-width', 2);

        // 2Y-10Y Spread annotation
        if (isInverted) {
            const x2Y = x('2Y');
            const x10Y = x('10Y');
            const y2Y = y(twoYear);
            const y10Y = y(tenYear);

            g.append('line')
                .attr('class', 'spread-line')
                .attr('x1', x2Y)
                .attr('x2', x10Y)
                .attr('y1', y2Y)
                .attr('y2', y10Y)
                .attr('stroke', 'var(--color-warning)')
                .attr('stroke-width', 2)
                .attr('stroke-dasharray', '5,5');
        }

    }, [yieldData, isInverted]);

    return (
        <div className="yield-curve-widget">
            <div className="widget-header">
                <h3>US Treasury Yield Curve</h3>
                {isInverted && (
                    <span className="inversion-badge">INVERTED</span>
                )}
            </div>
            <svg ref={svgRef}></svg>
            <div className="yield-stats">
                <div className="stat">
                    <span className="stat-label">2Y-10Y Spread</span>
                    <span className={`stat-value ${isInverted ? 'negative' : 'positive'}`}>
                        {((yieldData.find(d => d.maturity === 120)?.yield || 0) - 
                          (yieldData.find(d => d.maturity === 24)?.yield || 0)).toFixed(2)}%
                    </span>
                </div>
                <div className="stat">
                    <span className="stat-label">Fed Funds</span>
                    <span className="stat-value">5.25-5.50%</span>
                </div>
            </div>
        </div>
    );
};

export default YieldCurvePlotter;
