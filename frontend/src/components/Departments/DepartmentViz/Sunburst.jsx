import React, { useRef, useEffect, useMemo } from 'react';
import * as d3 from 'd3';

/**
 * Sunburst - Hierarchical sunburst chart for department visualizations
 * Used by: Architect (2), Steward (9), Auditor (12)
 */
const Sunburst = ({ data, color = '#8b5cf6', width = 400, height = 400 }) => {
  const svgRef = useRef();
  
  // Generate stub hierarchical data if none provided
  const chartData = useMemo(() => data || {
    name: 'Root',
    children: [
      { 
        name: 'Category A', 
        children: [
          { name: 'A1', value: 100 },
          { name: 'A2', value: 80 },
          { name: 'A3', value: 60 }
        ] 
      },
      { 
        name: 'Category B', 
        children: [
          { name: 'B1', value: 120 },
          { name: 'B2', value: 90 }
        ] 
      },
      { 
        name: 'Category C', 
        value: 200 
      }
    ]
  }, [data]);

  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const radius = Math.min(width, height) / 2;
    const g = svg
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', `translate(${width / 2},${height / 2})`);

    // Create hierarchy
    const root = d3.hierarchy(chartData)
      .sum(d => d.value || 0)
      .sort((a, b) => b.value - a.value);

    // Create partition layout
    const partition = d3.partition()
      .size([2 * Math.PI, radius]);

    partition(root);

    // Color scale
    const colorScale = d3.scaleOrdinal()
      .domain(root.descendants().map(d => d.data.name))
      .range(d3.quantize(t => d3.interpolateRgb(color, '#1a1a2e')(t), root.descendants().length));

    // Arc generator
    const arc = d3.arc()
      .startAngle(d => d.x0)
      .endAngle(d => d.x1)
      .padAngle(0.01)
      .padRadius(radius / 2)
      .innerRadius(d => d.y0)
      .outerRadius(d => d.y1 - 1);

    // Draw arcs
    g.selectAll('path')
      .data(root.descendants().filter(d => d.depth))
      .enter()
      .append('path')
      .attr('fill', d => colorScale(d.data.name))
      .attr('fill-opacity', 0.8)
      .attr('d', arc)
      .style('cursor', 'pointer')
      .on('mouseenter', function() {
        d3.select(this).attr('fill-opacity', 1);
      })
      .on('mouseleave', function() {
        d3.select(this).attr('fill-opacity', 0.8);
      });

    // Center label
    g.append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', '0.35em')
      .attr('fill', color)
      .attr('font-size', '14px')
      .attr('font-weight', 'bold')
      .text('HIERARCHY');

  }, [chartData, color, width, height]);

  return (
    <svg 
      ref={svgRef} 
      style={{ 
        width: '100%', 
        height: '100%', 
        minHeight: '300px',
        background: 'transparent' 
      }} 
    />
  );
};

export default Sunburst;
