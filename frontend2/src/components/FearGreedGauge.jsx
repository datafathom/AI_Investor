/**
 * ==============================================================================
 * FILE: frontend2/src/components/FearGreedGauge.jsx
 * ROLE: D3.js Gauge Visualization
 * PURPOSE: Renders a semi-circular gauge using D3.js and Framer Motion for 
 *          smooth needle transitions representing market sentiment.
 * ==============================================================================
 */
import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import { motion } from 'framer-motion';

const FearGreedGauge = ({ score = 50 }) => {
    const svgRef = useRef(null);
    const width = 300;
    const height = 160; // Semi-circle
    const radius = 140;

    useEffect(() => {
        if (!svgRef.current) return;

        const svg = d3.select(svgRef.current);
        svg.selectAll('*').remove(); // Clear prev

        const g = svg.append('g')
            .attr('transform', `translate(${width / 2}, ${height - 10})`);

        // Arc Generator
        const arc = d3.arc()
            .innerRadius(60)
            .outerRadius(radius)
            .startAngle(-Math.PI / 2)
            .endAngle(Math.PI / 2);

        // Gradient Definitions
        const defs = svg.append('defs');
        
        // Zones (0-25, 25-45, 45-55, 55-75, 75-100)
        // We can draw segments or use a linear gradient across the arc
        const colorScale = d3.scaleLinear()
            .domain([0, 25, 50, 75, 100])
            .range(['#ff4757', '#ffba0a', '#a4b0be', '#2ecc71', '#00ff88']);

        // Draw Background Arc
        // To make it look like segments, we can append multiple arcs
        const segments = [
            { min: 0, max: 25, color: '#ff4757', label: 'Ext Fear' },
            { min: 25, max: 45, color: '#ff7f50', label: 'Fear' },
            { min: 45, max: 55, color: '#dcdde1', label: 'Neutral' },
            { min: 55, max: 75, color: '#3adb6a', label: 'Greed' },
            { min: 75, max: 100, color: '#00fa9a', label: 'Ext Greed' }
        ];

        segments.forEach(seg => {
             // Convert scale to radians
             const startRad = (-Math.PI / 2) + (seg.min / 100) * Math.PI;
             const endRad = (-Math.PI / 2) + (seg.max / 100) * Math.PI;

             const segArc = d3.arc()
                .innerRadius(60)
                .outerRadius(radius)
                .startAngle(startRad)
                .endAngle(endRad)
                .cornerRadius(2);
            
             g.append('path')
                .attr('d', segArc)
                .attr('fill', seg.color)
                .attr('stroke', '#0A0A0B')
                .attr('stroke-width', 2);
        });
        
    }, []);

    // Needle Calculation
    // -90deg to +90deg
    const angle = (score / 100) * 180 - 90;

    return (
        <div style={{ position: 'relative', width, height, margin: '0 auto' }}>
            <svg ref={svgRef} width={width} height={height} style={{ overflow: 'visible' }} />
            
            {/* Needle via Framer Motion */}
            <motion.div
                initial={{ rotate: -90 }}
                animate={{ rotate: angle }}
                transition={{ type: "spring", stiffness: 60, damping: 15 }}
                style={{
                    position: 'absolute',
                    bottom: 10,
                    left: '50%',
                    width: 4,
                    height: 120,
                    background: '#fff',
                    borderRadius: '2px',
                    transformOrigin: 'bottom center',
                    boxShadow: '0 0 10px rgba(0,0,0,0.5)',
                    zIndex: 10
                }}
            >
                <div style={{
                    position: 'absolute',
                    width: 16,
                    height: 16,
                    background: '#fff',
                    borderRadius: '50%',
                    bottom: -8,
                    left: -6,
                    border: '4px solid #0A0A0B'
                }} />
            </motion.div>
            
            <div style={{ 
                position: 'absolute', 
                bottom: 20, 
                width: '100%', 
                textAlign: 'center', 
                color: 'white', 
                fontWeight: 'bold',
                textShadow: '0 2px 4px rgba(0,0,0,0.8)'
            }}>
                <div style={{ fontSize: '2em' }}>{Math.round(score)}</div>
                <div style={{ fontSize: '0.8em', textTransform: 'uppercase', letterSpacing: '1px' }}>Sentiment</div>
            </div>
        </div>
    );
};

export default FearGreedGauge;
