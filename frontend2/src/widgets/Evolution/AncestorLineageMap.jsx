import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import './AncestorLineageMap.css';

const AncestorLineageMap = ({ data }) => {
  const svgRef = useRef();

  const mockData = {
    name: "ROOT-0",
    id: "ROOT-0",
    children: [
      {
        name: "AGENT-A1",
        id: "A1",
        children: [
          { name: "AGENT-B1", id: "B1" },
          { name: "AGENT-B2", id: "B2" }
        ]
      },
      {
        name: "AGENT-A2",
        id: "A2",
        children: [
          { 
            name: "AGENT-C1", 
            id: "C1",
            children: [
              { name: "HYBRID-X1", id: "X1" }
            ]
          }
        ]
      }
    ]
  };

  useEffect(() => {
    if (!svgRef.current) return;

    const width = 600;
    const height = 300;
    const margin = { top: 20, right: 90, bottom: 30, left: 90 };

    // Clear previous SVG content
    d3.select(svgRef.current).selectAll("*").remove();

    const svg = d3.select(svgRef.current)
      .attr("width", width)
      .attr("height", height)
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    const treeData = d3.hierarchy(data || mockData);
    const treeLayout = d3.tree().size([height - margin.top - margin.bottom, width - margin.left - margin.right]);

    const nodes = treeLayout(treeData);

    // Links
    svg.selectAll(".link")
      .data(nodes.links())
      .enter()
      .append("path")
      .attr("class", "link")
      .attr("d", d3.linkHorizontal()
        .x(d => d.y)
        .y(d => d.x));

    // Nodes
    const node = svg.selectAll(".node")
      .data(nodes.descendants())
      .enter()
      .append("g")
      .attr("class", d => "node" + (d.children ? " node--internal" : " node--leaf"))
      .attr("transform", d => `translate(${d.y},${d.x})`);

    node.append("circle")
      .attr("r", 6);

    node.append("text")
      .attr("dy", ".35em")
      .attr("x", d => d.children ? -10 : 10)
      .style("text-anchor", d => d.children ? "end" : "start")
      .text(d => d.data.name);

  }, [data]);

  return (
    <div className="lineage-map-container">
      <div className="lineage-map-header">
        <h3>Genetic Heritage Map</h3>
      </div>
      <svg ref={svgRef} className="lineage-svg-container"></svg>
    </div>
  );
};

export default AncestorLineageMap;
