import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

/**
 * FlowChart - Sequential flow visualization for Banker/Guardian/Lawyer
 */
const FlowChart = ({ data, color }) => {
  const svgRef = useRef();

  useEffect(() => {
    if (!data || !svgRef.current) return;

    const width = 600;
    const height = 400;

    const svg = d3.select(svgRef.current)
      .attr('viewBox', [0, 0, width, height])
      .attr('width', '100%')
      .attr('height', '100%');

    svg.selectAll('*').remove();

    const nodeWidth = 80;
    const nodeHeight = 30;
    const margin = { top: 20, right: 20, bottom: 20, left: 20 };

    const nodes = data.nodes.map((d, i) => ({
      ...d,
      x: margin.left + (i % 3) * 200,
      y: margin.top + Math.floor(i / 3) * 100
    }));

    // Draw links
    svg.append('g')
      .attr('fill', 'none')
      .attr('stroke', color)
      .attr('stroke-opacity', 0.3)
      .attr('stroke-width', 2)
      .selectAll('path')
      .data(data.links)
      .join('path')
      .attr('d', d => {
        const source = nodes.find(n => n.id === d.source);
        const target = nodes.find(n => n.id === d.target);
        if (!source || !target) return '';
        
        const sx = source.x + nodeWidth;
        const sy = source.y + nodeHeight / 2;
        const tx = target.x;
        const ty = target.y + nodeHeight / 2;
        
        return `M${sx},${sy} C${(sx + tx) / 2},${sy} ${(sx + tx) / 2},${ty} ${tx},${ty}`;
      });

    // Draw nodes
    const node = svg.append('g')
      .selectAll('g')
      .data(nodes)
      .join('g')
      .attr('transform', d => `translate(${d.x},${d.y})`);

    node.append('rect')
      .attr('width', nodeWidth)
      .attr('height', nodeHeight)
      .attr('rx', 4)
      .attr('fill', 'rgba(0,0,0,0.4)')
      .attr('stroke', color)
      .attr('stroke-width', 1.5);

    node.append('text')
      .attr('x', nodeWidth / 2)
      .attr('y', nodeHeight / 2)
      .attr('dy', '0.35em')
      .attr('text-anchor', 'middle')
      .attr('font-size', '10px')
      .attr('fill', '#fff')
      .text(d => d.name);

    // Animated dots on paths
    svg.append('g')
      .selectAll('circle')
      .data(data.links)
      .join('circle')
      .attr('r', 2)
      .attr('fill', color)
      .append('animateMotion')
      .attr('dur', '3s')
      .attr('repeatCount', 'indefinite')
      .attr('path', d => {
        const source = nodes.find(n => n.id === d.source);
        const target = nodes.find(n => n.id === d.target);
        if (!source || !target) return '';
        const sx = source.x + nodeWidth;
        const sy = source.y + nodeHeight / 2;
        const tx = target.x;
        const ty = target.y + nodeHeight / 2;
        return `M${sx},${sy} C${(sx + tx) / 2},${sy} ${(sx + tx) / 2},${ty} ${tx},${ty}`;
      });

  }, [data, color]);

  return (
    <div className="d3-viz-wrapper" style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <svg ref={svgRef}></svg>
    </div>
  );
};

export default FlowChart;
