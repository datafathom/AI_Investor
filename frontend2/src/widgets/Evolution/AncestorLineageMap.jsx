import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import './AncestorLineageMap.css';

const AncestorLineageMap = ({ data, onSelect }) => {
  const svgRef = useRef();

  const mockData = {
    name: "ROOT-0",
    id: "ROOT-0",
    genes: { rsi_period: 14, rsi_buy: 30, rsi_sell: 70 },
    children: [
      {
        name: "AGENT-A1",
        id: "A1",
        genes: { rsi_period: 12, rsi_buy: 32, rsi_sell: 68 },
        children: [
          { name: "AGENT-B1", id: "B1", genes: { rsi_period: 11, rsi_buy: 34, rsi_sell: 65 } },
          { name: "AGENT-B2", id: "B2", genes: { rsi_period: 15, rsi_buy: 28, rsi_sell: 72 } }
        ]
      },
      {
        name: "AGENT-A2",
        id: "A2",
        genes: { rsi_period: 18, rsi_buy: 25, rsi_sell: 75 },
        children: [
          { 
            name: "AGENT-C1", 
            id: "C1",
            genes: { rsi_period: 20, rsi_buy: 20, rsi_sell: 80 },
            children: [
              { name: "HYBRID-X1", id: "X1", genes: { rsi_period: 16, rsi_buy: 27, rsi_sell: 73 } }
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
    const margin = { top: 20, right: 120, bottom: 30, left: 40 };

    d3.select(svgRef.current).selectAll("*").remove();

    const svg = d3.select(svgRef.current)
      .attr("width", width)
      .attr("height", height)
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);

    const treeData = d3.hierarchy(data || mockData);
    const treeLayout = d3.tree().size([height - margin.top - margin.bottom, width - margin.left - margin.right]);

    const nodes = treeLayout(treeData);

    // Filtered links for a glowing effect
    svg.selectAll(".link")
      .data(nodes.links())
      .enter()
      .append("path")
      .attr("class", "link")
      .attr("d", d3.linkHorizontal().x(d => d.y).y(d => d.x))
      .style("stroke-width", 2)
      .style("stroke", "rgba(0, 242, 255, 0.2)");

    const node = svg.selectAll(".node")
      .data(nodes.descendants())
      .enter()
      .append("g")
      .attr("class", d => `node ${d.children ? "internal" : "leaf"}`)
      .attr("transform", d => `translate(${d.y},${d.x})`)
      .style("cursor", "pointer")
      .on("click", (event, d) => {
          onSelect?.(d.data);
      });

    node.append("circle")
      .attr("r", 8)
      .style("fill", "#0f172a")
      .style("stroke", d => d.children ? "#0ea5e9" : "#06b6d4")
      .style("stroke-width", 2);

    node.append("text")
      .attr("dy", ".35em")
      .attr("x", d => d.children ? -12 : 12)
      .style("text-anchor", d => d.children ? "end" : "start")
      .style("fill", "#94a3b8")
      .style("font-size", "10px")
      .style("font-weight", "bold")
      .text(d => d.data.name);

  }, [data, onSelect]);

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
