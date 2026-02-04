import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import './InteractionHeatmap.css';

/**
 * Interaction Effect Heatmap 
 * 
 * 11x11 matrix showing cross-sector interaction effects from Brinson-Fachler attribution.
 */
const InteractionHeatmap = () => {
    const svgRef = useRef(null);
    const [hoveredCell, setHoveredCell] = useState(null);

    const sectors = [
        'Tech', 'Health', 'Fin', 'ConD', 'Ind', 
        'Energy', 'Mat', 'Util', 'RE', 'Comm', 'ConS'
    ];

    // Mock interaction matrix (sector vs sector)
    const generateMatrix = () => {
        return sectors.map(() => 
            sectors.map(() => (Math.random() - 0.5) * 20) // -10 to +10 bps
        );
    };

    const [matrix] = useState(generateMatrix);

    useEffect(() => {
        if (!svgRef.current) return;

        const svg = d3.select(svgRef.current);
        svg.selectAll('*').remove();

        const size = 350;
        const margin = { top: 40, right: 20, bottom: 20, left: 40 };
        const gridSize = (size - margin.left - margin.right) / sectors.length;

        const g = svg
            .attr('width', size)
            .attr('height', size)
            .append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);

        // Color scale
        const colorScale = d3.scaleSequential(d3.interpolateRdYlGn)
            .domain([-10, 10]);

        // Draw cells
        sectors.forEach((rowSector, i) => {
            sectors.forEach((colSector, j) => {
                const value = matrix[i][j];
                const isOutlier = Math.abs(value) > 8;

                g.append('rect')
                    .attr('x', j * gridSize)
                    .attr('y', i * gridSize)
                    .attr('width', gridSize - 2)
                    .attr('height', gridSize - 2)
                    .attr('fill', colorScale(value))
                    .attr('stroke', isOutlier ? 'var(--color-warning)' : 'var(--border-primary)')
                    .attr('stroke-width', isOutlier ? 2 : 0.5)
                    .attr('class', isOutlier ? 'outlier-cell' : '')
                    .on('mouseenter', () => setHoveredCell({ row: rowSector, col: colSector, value }))
                    .on('mouseleave', () => setHoveredCell(null));
            });
        });

        // Row labels
        g.selectAll('.row-label')
            .data(sectors)
            .enter()
            .append('text')
            .attr('class', 'row-label')
            .attr('x', -5)
            .attr('y', (d, i) => i * gridSize + gridSize / 2 + 4)
            .attr('text-anchor', 'end')
            .attr('fill', 'var(--text-secondary)')
            .style('font-size', '9px')
            .text(d => d);

        // Column labels
        g.selectAll('.col-label')
            .data(sectors)
            .enter()
            .append('text')
            .attr('class', 'col-label')
            .attr('x', (d, i) => i * gridSize + gridSize / 2)
            .attr('y', -10)
            .attr('text-anchor', 'middle')
            .attr('fill', 'var(--text-secondary)')
            .style('font-size', '9px')
            .text(d => d);

    }, [matrix, sectors]);

    return (
        <div className="interaction-heatmap">
            <div className="widget-header">
                <h3>Interaction Effects</h3>
            </div>

            <svg ref={svgRef}></svg>

            {hoveredCell && (
                <div className="heatmap-tooltip">
                    <div className="tooltip-title">{hoveredCell.row} × {hoveredCell.col}</div>
                    <div className={`tooltip-value ${hoveredCell.value >= 0 ? 'positive' : 'negative'}`}>
                        {hoveredCell.value >= 0 ? '+' : ''}{hoveredCell.value.toFixed(1)}bps
                    </div>
                </div>
            )}

            <div className="heatmap-legend">
                <span className="legend-label">-10bps</span>
                <div className="legend-gradient"></div>
                <span className="legend-label">+10bps</span>
            </div>
        </div>
    );
};

export default InteractionHeatmap;
