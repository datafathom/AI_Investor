import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import './AttributionChart.css';

/**
 * Brinson-Fachler Performance Attribution Widget
 * 
 * Displays sector allocation effects (diverging bar chart)
 * comparing portfolio vs benchmark allocation.
 */
const AttributionChart = ({ portfolioData, benchmarkData }) => {
    const svgRef = useRef(null);
    const [selectedSector, setSelectedSector] = useState(null);

    // Mock data for demonstration
    const attributionData = [
        { sector: 'Technology', allocation: 0.28, benchmark: 0.25, selection: 0.015, interaction: 0.003 },
        { sector: 'Healthcare', allocation: 0.18, benchmark: 0.15, selection: 0.008, interaction: -0.002 },
        { sector: 'Financials', allocation: 0.12, benchmark: 0.14, selection: -0.005, interaction: 0.001 },
        { sector: 'Consumer Disc.', allocation: 0.10, benchmark: 0.11, selection: 0.002, interaction: 0.000 },
        { sector: 'Industrials', allocation: 0.09, benchmark: 0.09, selection: 0.000, interaction: 0.002 },
        { sector: 'Energy', allocation: 0.07, benchmark: 0.05, selection: 0.012, interaction: -0.001 },
        { sector: 'Materials', allocation: 0.05, benchmark: 0.04, selection: 0.003, interaction: 0.000 },
        { sector: 'Utilities', allocation: 0.04, benchmark: 0.06, selection: -0.008, interaction: 0.001 },
        { sector: 'Real Estate', allocation: 0.04, benchmark: 0.05, selection: -0.002, interaction: 0.000 },
        { sector: 'Comm. Services', allocation: 0.03, benchmark: 0.06, selection: -0.010, interaction: -0.001 },
    ];

    useEffect(() => {
        if (!svgRef.current) return;

        const svg = d3.select(svgRef.current);
        svg.selectAll('*').remove();

        const margin = { top: 20, right: 30, bottom: 40, left: 100 };
        const width = 500 - margin.left - margin.right;
        const height = 400 - margin.top - margin.bottom;

        const g = svg
            .attr('width', width + margin.left + margin.right)
            .attr('height', height + margin.top + margin.bottom)
            .append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);

        // Scales
        const y = d3.scaleBand()
            .domain(attributionData.map(d => d.sector))
            .range([0, height])
            .padding(0.2);

        const maxVal = Math.max(
            d3.max(attributionData, d => Math.abs(d.selection)),
            d3.max(attributionData, d => Math.abs(d.interaction))
        );
        
        const x = d3.scaleLinear()
            .domain([-maxVal * 1.5, maxVal * 1.5])
            .range([0, width]);

        // Axes
        g.append('g')
            .attr('class', 'axis axis-y')
            .call(d3.axisLeft(y));

        g.append('g')
            .attr('class', 'axis axis-x')
            .attr('transform', `translate(0,${height})`)
            .call(d3.axisBottom(x).tickFormat(d3.format('.1%')));

        // Zero line
        g.append('line')
            .attr('class', 'zero-line')
            .attr('x1', x(0))
            .attr('x2', x(0))
            .attr('y1', 0)
            .attr('y2', height)
            .attr('stroke', 'var(--border-primary)')
            .attr('stroke-width', 1);

        // Selection Effect bars
        g.selectAll('.bar-selection')
            .data(attributionData)
            .enter()
            .append('rect')
            .attr('class', 'bar-selection')
            .attr('y', d => y(d.sector))
            .attr('height', y.bandwidth() / 2)
            .attr('x', d => d.selection >= 0 ? x(0) : x(d.selection))
            .attr('width', d => Math.abs(x(d.selection) - x(0)))
            .attr('fill', d => d.selection >= 0 ? 'var(--color-bullish)' : 'var(--color-bearish)')
            .attr('opacity', 0.8)
            .on('mouseover', (event, d) => setSelectedSector(d))
            .on('mouseout', () => setSelectedSector(null));

        // Interaction Effect bars (stacked below)
        g.selectAll('.bar-interaction')
            .data(attributionData)
            .enter()
            .append('rect')
            .attr('class', 'bar-interaction')
            .attr('y', d => y(d.sector) + y.bandwidth() / 2)
            .attr('height', y.bandwidth() / 2)
            .attr('x', d => d.interaction >= 0 ? x(0) : x(d.interaction))
            .attr('width', d => Math.abs(x(d.interaction) - x(0)))
            .attr('fill', d => d.interaction >= 0 ? 'var(--color-info)' : 'var(--color-warning)')
            .attr('opacity', 0.6);

        // Legend
        const legend = g.append('g')
            .attr('class', 'legend')
            .attr('transform', `translate(${width - 120}, -10)`);

        legend.append('rect').attr('x', 0).attr('y', 0).attr('width', 12).attr('height', 12).attr('fill', 'var(--color-bullish)');
        legend.append('text').attr('x', 16).attr('y', 10).text('Selection').attr('fill', 'var(--text-secondary)').style('font-size', '10px');

        legend.append('rect').attr('x', 70).attr('y', 0).attr('width', 12).attr('height', 12).attr('fill', 'var(--color-info)');
        legend.append('text').attr('x', 86).attr('y', 10).text('Interaction').attr('fill', 'var(--text-secondary)').style('font-size', '10px');

    }, [attributionData]);

    return (
        <div className="attribution-chart">
            <div className="chart-header">
                <h3>Brinson-Fachler Attribution</h3>
                <span className="period-label">YTD Performance</span>
            </div>
            <svg ref={svgRef}></svg>
            {selectedSector && (
                <div className="sector-detail">
                    <strong>{selectedSector.sector}</strong>
                    <div>Allocation: {(selectedSector.allocation * 100).toFixed(1)}% vs Benchmark: {(selectedSector.benchmark * 100).toFixed(1)}%</div>
                    <div>Selection Effect: <span className={selectedSector.selection >= 0 ? 'positive' : 'negative'}>{(selectedSector.selection * 100).toFixed(2)}%</span></div>
                    <div>Interaction Effect: <span className={selectedSector.interaction >= 0 ? 'positive' : 'negative'}>{(selectedSector.interaction * 100).toFixed(2)}%</span></div>
                </div>
            )}
        </div>
    );
};

export default AttributionChart;
