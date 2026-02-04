import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

const SentimentChart = ({ data }) => {
    const svgRef = useRef();
    const containerRef = useRef();

    useEffect(() => {
        if (!data || data.length === 0) return;

        // Get container dimensions or fallback
        const containerWidth = containerRef.current ? containerRef.current.offsetWidth : 600;

        const margin = { top: 20, right: 30, bottom: 40, left: 50 };
        const width = containerWidth - margin.left - margin.right;
        const height = 300 - margin.top - margin.bottom;

        // Clear existing
        d3.select(svgRef.current).selectAll("*").remove();

        const svg = d3.select(svgRef.current)
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom)
            .append("g")
            .attr("transform", `translate(${margin.left},${margin.top})`);

        const x = d3.scaleTime()
            .domain(d3.extent(data, d => new Date(d.timestamp)))
            .range([0, width]);

        const y = d3.scaleLinear()
            .domain([-1, 1]) // Sentiment scope -1 to +1
            .range([height, 0]);

        // Grid lines
        svg.append("g")
            .attr("class", "grid")
            .attr("opacity", 0.1)
            .call(d3.axisLeft(y).tickSize(-width).tickFormat(""));

        // Axes
        svg.append("g")
            .attr("transform", `translate(0,${height})`)
            .call(d3.axisBottom(x).ticks(5))
            .attr("color", "#94a3b8");

        svg.append("g")
            .call(d3.axisLeft(y))
            .attr("color", "#94a3b8");

        // Line
        const line = d3.line()
            .x(d => x(new Date(d.timestamp)))
            .y(d => y(d.score))
            .curve(d3.curveCardinal);

        svg.append("path")
            .datum(data)
            .attr("fill", "none")
            .attr("stroke", "#00f2ff")
            .attr("stroke-width", 2)
            .attr("d", line)
            .style("filter", "drop-shadow(0 0 5px rgba(0, 242, 255, 0.6))");

        // Area
        const area = d3.area()
            .x(d => x(new Date(d.timestamp)))
            .y0(y(0))
            .y1(d => y(d.score))
            .curve(d3.curveCardinal);

        svg.append("path")
            .datum(data)
            .attr("fill", "url(#sentiment-gradient)")
            .attr("opacity", 0.2)
            .attr("d", area);

        // Gradient
        const defs = svg.append("defs");
        const gradient = defs.append("linearGradient")
            .attr("id", "sentiment-gradient")
            .attr("x1", "0%").attr("y1", "0%")
            .attr("x2", "0%").attr("y2", "100%");

        gradient.append("stop").attr("offset", "0%").attr("stop-color", "#00f2ff");
        gradient.append("stop").attr("offset", "100%").attr("stop-color", "transparent");

    }, [data]);

    return (
        <div className="glass-card w-full" ref={containerRef}>
            <h3 className="neon-text mb-4">Sentiment Entropy (24h)</h3>
            <svg ref={svgRef} className="w-full"></svg>
        </div>
    );
};

export default SentimentChart;
