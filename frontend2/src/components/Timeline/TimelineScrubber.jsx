import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import useTimelineStore from '../../stores/timelineStore';
import { Play, Pause, FastForward, SkipBack, Zap } from 'lucide-react';
import './TimelineScrubber.css';

const TimelineScrubber = () => {
    const svgRef = useRef(null);
    const { 
        currentTime, 
        setCurrentTime, 
        events, 
        isPlaying, 
        togglePlayback,
        isHistoricalMode,
        goLive
    } = useTimelineStore();

    useEffect(() => {
        if (!svgRef.current) return;

        const margin = { top: 10, right: 20, bottom: 20, left: 20 };
        const width = svgRef.current.clientWidth - margin.left - margin.right;
        const height = 40 - margin.top - margin.bottom;

        const svg = d3.select(svgRef.current)
            .attr('height', 40 + margin.top + margin.bottom);
        
        svg.selectAll("*").remove(); // Clear previous

        const g = svg.append('g')
            .attr('transform', `translate(${margin.left},${margin.top})`);

        // Time window: Last 24 hours to Now
        const timeEnd = Date.now();
        const timeStart = timeEnd - 24 * 60 * 60 * 1000;

        const x = d3.scaleTime()
            .domain([timeStart, timeEnd])
            .range([0, width]);

        // Draw Axis
        g.append('g')
            .attr('class', 'axis axis-x')
            .attr('transform', `translate(0,${height})`)
            .call(d3.axisBottom(x).ticks(5).tickSize(-height).tickFormat(d3.timeFormat('%H:%M')));

        // Draw Event Dots
        g.selectAll('.event-dot')
            .data(events)
            .enter()
            .append('circle')
            .attr('class', (d) => `event-dot ${d.type}`)
            .attr('cx', (d) => x(d.timestamp))
            .attr('cy', height / 2)
            .attr('r', 3);

        // Current Time Needle
        const needle = g.append('line')
            .attr('class', 'timeline-needle')
            .attr('x1', x(currentTime))
            .attr('x2', x(currentTime))
            .attr('y1', 0)
            .attr('y2', height + 5);

        // Brush for scrubbing
        const brush = d3.brushX()
            .extent([[0, 0], [width, height]])
            .on('brush', (event) => {
                if (event.sourceEvent) {
                    const selection = event.selection;
                    const time = x.invert(selection[1]);
                    setCurrentTime(time.getTime());
                }
            });

        g.append('g')
            .attr('class', 'brush')
            .call(brush);

    }, [events, currentTime]);

    return (
        <div className="timeline-scrubber-container">
            <div className="timeline-controls">
                <button onClick={togglePlayback} className="control-btn">
                    {isPlaying ? <Pause size={16} /> : <Play size={16} />}
                </button>
                <div className="time-display">
                    {new Date(currentTime).toLocaleTimeString()}
                    {isHistoricalMode && <span className="historical-label">HISTORICAL</span>}
                </div>
                {isHistoricalMode && (
                    <button onClick={goLive} className="live-btn">
                        <Zap size={14} /> GO LIVE
                    </button>
                )}
            </div>
            <div className="timeline-viz">
                <svg ref={svgRef} style={{ width: '100%' }}></svg>
            </div>
        </div>
    );
};

export default TimelineScrubber;
