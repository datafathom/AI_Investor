import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

/**
 * BubbleChart - Visualization for clusters (Hunter, Strategist)
 */
const BubbleChart = ({ data, color }) => {
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

    const pack = d3.pack()
      .size([width, height])
      .padding(3);

    const root = d3.hierarchy({ children: data })
      .sum(d => d.value);

    const nodes = pack(root).leaves();

    const leaf = svg.selectAll('g')
      .data(nodes)
      .join('g')
      .attr('transform', d => `translate(${d.x},${d.y})`);

    leaf.append('circle')
      .attr('r', d => d.r)
      .attr('fill', color)
      .attr('fill-opacity', 0.6)
      .attr('stroke', color)
      .attr('stroke-width', 1);

    leaf.append('text')
      .selectAll('tspan')
      .data(d => d.data.name.split(/(?=[A-Z][a-z])|\s+/g))
      .join('tspan')
      .attr('x', 0)
      .attr('y', (d, i, nodes) => `${i - nodes.length / 2 + 0.8}em`)
      .attr('font-size', '8px')
      .attr('fill', '#fff')
      .attr('text-anchor', 'middle')
      .text(d => d);

    leaf.append('title')
      .text(d => `${d.data.name}\n${d.data.value}`);

  }, [data, color]);

  return (
    <div className="d3-viz-wrapper" style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <svg ref={svgRef}></svg>
    </div>
  );
};

export default BubbleChart;
