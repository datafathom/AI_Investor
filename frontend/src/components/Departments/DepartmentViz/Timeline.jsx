import React, { useRef, useEffect, useMemo } from 'react';
import * as d3 from 'd3';

/**
 * Timeline - Horizontal timeline for historical events
 * Used by: Historian (15)
 */
const Timeline = ({ data, color = '#78716c', width = 600, height = 300 }) => {
  const svgRef = useRef();
  
  // Generate stub timeline data if none provided
  const chartData = useMemo(() => data || [
    { date: new Date('2024-01-15'), label: 'Strategy Deployed', type: 'success' },
    { date: new Date('2024-02-20'), label: 'Market Correction', type: 'warning' },
    { date: new Date('2024-03-10'), label: 'Rebalance Event', type: 'info' },
    { date: new Date('2024-04-05'), label: 'Peak Performance', type: 'success' },
    { date: new Date('2024-05-18'), label: 'Risk Alert', type: 'error' },
    { date: new Date('2024-06-01'), label: 'Recovery Phase', type: 'info' }
  ], [data]);

  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const margin = { top: 40, right: 40, bottom: 40, left: 40 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const g = svg
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Time scale
    const xScale = d3.scaleTime()
      .domain(d3.extent(chartData, d => d.date))
      .range([0, innerWidth]);

    // Type colors
    const typeColors = {
      success: '#22c55e',
      warning: '#f59e0b',
      error: '#ef4444',
      info: color
    };

    // Draw timeline axis
    g.append('line')
      .attr('x1', 0)
      .attr('y1', innerHeight / 2)
      .attr('x2', innerWidth)
      .attr('y2', innerHeight / 2)
      .attr('stroke', '#444')
      .attr('stroke-width', 2);

    // Draw events
    const events = g.selectAll('.event')
      .data(chartData)
      .enter()
      .append('g')
      .attr('class', 'event')
      .attr('transform', d => `translate(${xScale(d.date)},${innerHeight / 2})`);

    // Event circles
    events.append('circle')
      .attr('r', 8)
      .attr('fill', d => typeColors[d.type] || color)
      .attr('stroke', '#fff')
      .attr('stroke-width', 2)
      .style('cursor', 'pointer');

    // Event labels (alternating above/below)
    events.append('text')
      .attr('y', (d, i) => i % 2 === 0 ? -20 : 25)
      .attr('text-anchor', 'middle')
      .attr('fill', '#888')
      .attr('font-size', '10px')
      .text(d => d.label);

    // Date labels
    events.append('text')
      .attr('y', (d, i) => i % 2 === 0 ? -35 : 40)
      .attr('text-anchor', 'middle')
      .attr('fill', '#666')
      .attr('font-size', '8px')
      .text(d => d.date.toLocaleDateString());

    // Axis
    g.append('g')
      .attr('transform', `translate(0,${innerHeight - 10})`)
      .call(d3.axisBottom(xScale).ticks(5).tickFormat(d3.timeFormat('%b %Y')))
      .selectAll('text')
      .attr('fill', '#666')
      .attr('font-size', '9px');

  }, [chartData, color, width, height]);

  return (
    <svg 
      ref={svgRef} 
      style={{ 
        width: '100%', 
        height: '100%', 
        minHeight: '250px',
        background: 'transparent' 
      }} 
    />
  );
};

export default Timeline;
