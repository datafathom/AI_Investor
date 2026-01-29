import React, { useRef, useEffect } from 'react';
import * as d3 from 'd3';

const LineageMap = ({ data, width = 600, height = 400 }) => {
  const svgRef = useRef(null);

  useEffect(() => {
    if (!data || !data.length) return;

    // Clear previous
    d3.select(svgRef.current).selectAll('*').remove();

    const svg = d3.select(svgRef.current)
      .attr('viewBox', `0 0 ${width} ${height}`)
      .style('background', '#111')
      .style('border-radius', '12px');

    // Convert flat data to hierarchy if needed, or assume tree structure
    // For now, demo a simple tree from the "child" upwards or a mock tree
    // Mock hierarchy for visualization if data is flat
    const rootData = {
      name: "Current Agent",
      children: [
        { name: "Parent A", children: [{ name: "Grandparent AA" }, { name: "Grandparent AB" }] },
        { name: "Parent B", children: [{ name: "Grandparent BA" }, { name: "Grandparent BB" }] }
      ]
    };

    const root = d3.hierarchy(rootData);
    const treeLayout = d3.tree().size([width - 100, height - 100]);
    treeLayout(root);

    const g = svg.append('g').attr('transform', 'translate(50, 50)');

    // Links
    g.selectAll('.link')
      .data(root.links())
      .enter().append('path')
      .attr('class', 'link')
      .attr('d', d3.linkVertical()
        .x(d => d.x)
        .y(d => d.y))
      .attr('fill', 'none')
      .attr('stroke', '#555')
      .attr('stroke-width', 2);

    // Nodes
    const nodes = g.selectAll('.node')
      .data(root.descendants())
      .enter().append('g')
      .attr('class', 'node')
      .attr('transform', d => `translate(${d.x},${d.y})`);

    nodes.append('circle')
      .attr('r', 10)
      .attr('fill', '#00ff88')
      .attr('stroke', '#fff')
      .attr('stroke-width', 2);

    nodes.append('text')
      .attr('dy', 25)
      .attr('text-anchor', 'middle')
      .text(d => d.data.name)
      .style('fill', '#ccc')
      .style('font-size', '12px');

  }, [data, width, height]);

  return <svg ref={svgRef} width="100%" height={height} />;
};

export default LineageMap;
