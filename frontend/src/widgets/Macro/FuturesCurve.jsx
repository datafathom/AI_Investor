import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import './FuturesCurve.css';
import apiClient from '../../services/apiClient';

const FuturesCurve = () => {
    const d3Container = useRef(null);
    const [contracts, setContracts] = useState([]);
    const [commodity, setCommodity] = useState('CL'); // Default Crude Oil
    const [curveShape, setCurveShape] = useState('unknown');

    useEffect(() => {
        // Fetch real futures data
        const fetchData = async () => {
            try {
                const response = await apiClient.get(`/macro/futures/${commodity}`);
                const result = response.data;
                if (result.success) {
                    setContracts(result.data.contracts);
                    setCurveShape(result.data.curve_shape);
                }
            } catch (err) {
                console.error("Failed to fetch futures curve:", err);
            }
        };
        fetchData();
    }, [commodity]);

    useEffect(() => {
        if (d3Container.current && contracts.length > 0) {
            const width = d3Container.current.clientWidth;
            const height = 300;
            const margin = { top: 20, right: 30, bottom: 30, left: 40 };

            d3.select(d3Container.current).selectAll("*").remove();

            const svg = d3.select(d3Container.current)
                .append("svg")
                .attr("width", width)
                .attr("height", height)
                .append("g")
                .attr("transform", `translate(${margin.left},${margin.top})`);

            // Map API data to D3 format
            const data = contracts.map((c, i) => ({ month: i + 1, price: c.price }));

            const minPrice = d3.min(data, d => d.price) * 0.99;
            const maxPrice = d3.max(data, d => d.price) * 1.01;

            const x = d3.scaleLinear()
                .domain([1, data.length])
                .range([0, width - margin.left - margin.right]);

            const y = d3.scaleLinear()
                .domain([minPrice, maxPrice])
                .range([height - margin.top - margin.bottom, 0]);
            
            // Curve Line
            svg.append("path")
                .datum(data)
                .attr("fill", "none")
                .attr("stroke", curveShape === 'contango' ? "#ef4444" : "#22c55e") // Red for Contango (negative roll), Green for Backwardation
                .attr("stroke-width", 2)
                .attr("d", d3.line()
                    .x(d => x(d.month))
                    .y(d => y(d.price))
                    .curve(d3.curveMonotoneX)
                );

            // Add Axes
            svg.append("g")
                .attr("transform", `translate(0,${height - margin.top - margin.bottom})`)
                .call(d3.axisBottom(x).ticks(6));

            svg.append("g")
                .call(d3.axisLeft(y));

            // Labels
            svg.append("text")
                .attr("x", width / 2)
                .attr("y", -5)
                .style("text-anchor", "middle")
                .style("fill", "#ccc")
                .style("font-size", "12px")
                .text(`Term Structure (${commodity} - ${curveShape.toUpperCase()})`);

        }
    }, [contracts, commodity, curveShape]);

    return (
        <div className="futures-curve-widget h-full flex flex-col">
            <div className="flex justify-between items-center mb-2">
                <h3>Futures Term Structure</h3>
                <div className="flex gap-2">
                    <button onClick={() => setCommodity('CL')} className={`px-2 py-1 text-xs rounded ${commodity === 'CL' ? 'bg-blue-600' : 'bg-slate-700'}`}>Crude</button>
                    <button onClick={() => setCommodity('NG')} className={`px-2 py-1 text-xs rounded ${commodity === 'NG' ? 'bg-blue-600' : 'bg-slate-700'}`}>Nat Gas</button>
                </div>
            </div>
            <div ref={d3Container} className="d3-container flex-1 min-h-[200px]"></div>
            <div className="legend mt-2 flex justify-between text-xs text-slate-400">
                <span>Curve: <strong className={curveShape === 'contango' ? 'text-red-400' : 'text-green-400'}>{curveShape.toUpperCase()}</strong></span>
                <span>{contracts.length > 0 ? `Front: $${contracts[0].price}` : 'Loading...'}</span>
            </div>
        </div>
    );
};

export default FuturesCurve;
