import React, { useEffect, useRef, useMemo, useCallback } from 'react';
import * as d3 from 'd3';

/**
 * ForceGraph - Network visualization of agents and topics
 * Optimized with useMemo and useCallback to prevent unnecessary re-renders.
 */
const ForceGraph = ({ data, color }) => {
  const svgRef = useRef();

  // Memoize node/link data to prevent D3 re-initialization on every render
  const graphData = useMemo(() => {
    if (!data) return null;
    return {
      nodes: data.nodes.map(n => ({ ...n })),
      links: data.links.map(l => ({ ...l }))
    };
  }, [data]);

  // Memoize drag behavior factory
  const createDrag = useCallback((simulation) => {
    function dragstarted(event) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      event.subject.fx = event.subject.x;
      event.subject.fy = event.subject.y;
    }

    function dragged(event) {
      event.subject.fx = event.x;
      event.subject.fy = event.y;
    }

    function dragended(event) {
      if (!event.active) simulation.alphaTarget(0);
      event.subject.fx = null;
      event.subject.fy = null;
    }

    return d3.drag()
      .on('start', dragstarted)
      .on('drag', dragged)
      .on('end', dragended);
  }, []);

  useEffect(() => {
    if (!graphData || !svgRef.current) return;

    const width = 600;
    const height = 400;

    const svg = d3.select(svgRef.current)
      .attr('viewBox', [0, 0, width, height])
      .attr('width', '100%')
      .attr('height', '100%');

    svg.selectAll('*').remove();

    const simulation = d3.forceSimulation(graphData.nodes)
      .force('link', d3.forceLink(graphData.links).id(d => d.id).distance(100))
      .force('charge', d3.forceManyBody().strength(-200))
      .force('center', d3.forceCenter(width / 2, height / 2));

    const link = svg.append('g')
      .attr('stroke', color)
      .attr('stroke-opacity', 0.6)
      .selectAll('line')
      .data(graphData.links)
      .join('line')
      .attr('stroke-width', d => Math.sqrt(d.value));

    const node = svg.append('g')
      .attr('stroke', '#fff')
      .attr('stroke-width', 1.5)
      .selectAll('circle')
      .data(graphData.nodes)
      .join('circle')
      .attr('r', d => d.group === 'hub' ? 12 : 8)
      .attr('fill', d => {
        if (d.group === 'hub') return '#fff';
        switch (d.status) {
          case 'busy': return '#3b82f6'; // Blue
          case 'error': return '#ef4444'; // Red
          case 'success': return '#22c55e'; // Green
          default: return color; // Department Color
        }
      })
      .call(createDrag(simulation));

    node.append('title')
      .text(d => d.id);

    simulation.on('tick', () => {
      link
        .attr('x1', d => d.source.x)
        .attr('y1', d => d.source.y)
        .attr('x2', d => d.target.x)
        .attr('y2', d => d.target.y);

      node
        .attr('cx', d => d.x)
        .attr('cy', d => d.y);
    });

    // Cleanup on unmount
    return () => simulation.stop();
  }, [graphData, color, createDrag]);

  return (
    <div className="d3-viz-wrapper" style={{ width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
      <svg ref={svgRef}></svg>
    </div>
  );
};

export default ForceGraph;
