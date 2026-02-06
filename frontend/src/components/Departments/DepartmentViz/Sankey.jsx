import React, { useRef, useEffect, useMemo } from 'react';
import * as d3 from 'd3';
import { sankey as d3Sankey, sankeyLinkHorizontal } from 'd3-sankey';

/**
 * Sankey - Flow diagram for capital/resource flows
 * Used by: Guardian (10), Banker (18)
 */
const Sankey = ({ data, color = '#14b8a6', width = 600, height = 400 }) => {
  const svgRef = useRef();
  
  // Generate stub flow data if none provided
  const chartData = useMemo(() => data || {
    nodes: [
      { id: 'Income' },
      { id: 'Investments' },
      { id: 'Expenses' },
      { id: 'Savings' },
      { id: 'Taxes' },
      { id: 'Growth' }
    ],
    links: [
      { source: 'Income', target: 'Investments', value: 40 },
      { source: 'Income', target: 'Expenses', value: 30 },
      { source: 'Income', target: 'Savings', value: 20 },
      { source: 'Income', target: 'Taxes', value: 10 },
      { source: 'Investments', target: 'Growth', value: 35 }
    ]
  }, [data]);

  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const margin = { top: 20, right: 20, bottom: 20, left: 20 };
    const innerWidth = width - margin.left - margin.right;
    const innerHeight = height - margin.top - margin.bottom;

    const g = svg
      .attr('width', width)
      .attr('height', height)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);

    // Create node index map
    const nodeMap = new Map(chartData.nodes.map((n, i) => [n.id, i]));

    // Prepare data for d3-sankey
    const sankeyData = {
      nodes: chartData.nodes.map(n => ({ name: n.id })),
      links: chartData.links.map(l => ({
        source: nodeMap.get(l.source),
        target: nodeMap.get(l.target),
        value: l.value
      }))
    };

    // Create sankey generator
    const sankeyGen = d3Sankey()
      .nodeWidth(15)
      .nodePadding(10)
      .extent([[0, 0], [innerWidth, innerHeight]]);

    const { nodes, links } = sankeyGen(sankeyData);

    // Color scale
    const colorScale = d3.scaleOrdinal()
      .domain(nodes.map(d => d.name))
      .range(d3.schemeTableau10);

    // Draw links
    g.append('g')
      .attr('fill', 'none')
      .attr('stroke-opacity', 0.4)
      .selectAll('path')
      .data(links)
      .enter()
      .append('path')
      .attr('d', sankeyLinkHorizontal())
      .attr('stroke', d => colorScale(d.source.name))
      .attr('stroke-width', d => Math.max(1, d.width))
      .style('mix-blend-mode', 'multiply');

    // Draw nodes
    g.append('g')
      .selectAll('rect')
      .data(nodes)
      .enter()
      .append('rect')
      .attr('x', d => d.x0)
      .attr('y', d => d.y0)
      .attr('height', d => d.y1 - d.y0)
      .attr('width', d => d.x1 - d.x0)
      .attr('fill', d => colorScale(d.name))
      .attr('stroke', '#000')
      .attr('stroke-width', 0.5);

    // Add labels
    g.append('g')
      .attr('font-size', '10px')
      .attr('font-family', 'sans-serif')
      .selectAll('text')
      .data(nodes)
      .enter()
      .append('text')
      .attr('x', d => d.x0 < innerWidth / 2 ? d.x1 + 6 : d.x0 - 6)
      .attr('y', d => (d.y1 + d.y0) / 2)
      .attr('dy', '0.35em')
      .attr('text-anchor', d => d.x0 < innerWidth / 2 ? 'start' : 'end')
      .attr('fill', '#888')
      .text(d => d.name);

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

export default Sankey;
