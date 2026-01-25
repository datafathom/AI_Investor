/**
 * BondLadder Widget - Draggable Bond Ladder Visualization
 * 
 * Phase 50: Interactive bond ladder builder with D3.js bars.
 * Supports drag to add/remove bonds, real-time WAL updates,
 * and liquidity gap indicators.
 */

import React, { useEffect, useRef, useState } from 'react';
import { useFixedIncomeStore } from '../../stores/fixedIncomeStore';
import * as d3 from 'd3';
import './BondLadder.css';

const BondLadder = () => {
  const svgRef = useRef(null);
  const {
    bondLadder,
    weightedAverageLife,
    liquidityGaps,
    addBond,
    removeBond,
    calculateWAL,
    fetchLiquidityGaps
  } = useFixedIncomeStore();
  
  const [showAddModal, setShowAddModal] = useState(false);
  const [newBond, setNewBond] = useState({ parValue: 10000, maturityYears: 5 });
  
  useEffect(() => {
    calculateWAL();
    fetchLiquidityGaps('default');
  }, [bondLadder.length]);
  
  useEffect(() => {
    renderLadder();
  }, [bondLadder, liquidityGaps]);
  
  const renderLadder = () => {
    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();
    
    const margin = { top: 20, right: 30, bottom: 50, left: 60 };
    const width = 600 - margin.left - margin.right;
    const height = 300 - margin.top - margin.bottom;
    
    const g = svg
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform', `translate(${margin.left},${margin.top})`);
    
    // Aggregate bonds by maturity year
    const maturities = {};
    bondLadder.forEach(bond => {
      const year = bond.maturityYears;
      maturities[year] = (maturities[year] || 0) + bond.parValue;
    });
    
    const data = Array.from({ length: 30 }, (_, i) => ({
      year: i + 1,
      value: maturities[i + 1] || 0,
      hasGap: liquidityGaps.some(g => g.year === i + 1)
    }));
    
    // Scales
    const xScale = d3.scaleBand()
      .domain(data.map(d => d.year))
      .range([0, width])
      .padding(0.1);
    
    const yScale = d3.scaleLinear()
      .domain([0, Math.max(d3.max(data, d => d.value), 50000)])
      .range([height, 0]);
    
    // Bars
    g.selectAll('.ladder-bar')
      .data(data)
      .enter()
      .append('rect')
      .attr('class', d => `ladder-bar ${d.value === 0 ? 'empty' : ''} ${d.hasGap ? 'gap' : ''}`)
      .attr('x', d => xScale(d.year))
      .attr('y', d => yScale(d.value))
      .attr('width', xScale.bandwidth())
      .attr('height', d => height - yScale(d.value))
      .attr('fill', d => {
        if (d.hasGap && d.value === 0) return 'rgba(239, 68, 68, 0.3)';
        if (d.value > 0) return 'rgba(96, 165, 250, 0.7)';
        return 'rgba(255, 255, 255, 0.05)';
      })
      .attr('stroke', d => d.hasGap ? '#ef4444' : 'transparent')
      .attr('stroke-width', 2)
      .attr('rx', 4);
    
    // Gap indicators (pulsing)
    g.selectAll('.gap-pulse')
      .data(data.filter(d => d.hasGap && d.value === 0))
      .enter()
      .append('circle')
      .attr('class', 'gap-pulse')
      .attr('cx', d => xScale(d.year) + xScale.bandwidth() / 2)
      .attr('cy', height - 10)
      .attr('r', 6)
      .attr('fill', '#ef4444');
    
    // X-axis
    g.append('g')
      .attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(xScale).tickValues([1, 5, 10, 15, 20, 25, 30]))
      .selectAll('text')
      .attr('fill', 'rgba(255,255,255,0.6)');
    
    // Y-axis
    g.append('g')
      .call(d3.axisLeft(yScale).ticks(5).tickFormat(d => `$${d/1000}k`))
      .selectAll('text')
      .attr('fill', 'rgba(255,255,255,0.6)');
    
    // Axis labels
    g.append('text')
      .attr('x', width / 2)
      .attr('y', height + 40)
      .attr('text-anchor', 'middle')
      .attr('fill', 'rgba(255,255,255,0.6)')
      .text('Years to Maturity');
  };
  
  const handleAddBond = () => {
    addBond(newBond);
    setShowAddModal(false);
    setNewBond({ parValue: 10000, maturityYears: 5 });
  };
  
  return (
    <div className="glass-panel bond-ladder-widget">
      <div className="widget-header">
        <h3 className="text-glow-cyan">🪜 Bond Ladder</h3>
        <div className="wal-display">
          <span className="wal-label">WAL:</span>
          <span className="wal-value">{weightedAverageLife.toFixed(1)} years</span>
        </div>
      </div>
      
      <div className="chart-container">
        <svg ref={svgRef}></svg>
      </div>
      
      {liquidityGaps.length > 0 && (
        <div className="gap-warnings">
          <span className="warning-icon">⚠️</span>
          <span>Liquidity gaps in years: {liquidityGaps.map(g => g.year).join(', ')}</span>
        </div>
      )}
      
      <div className="ladder-controls">
        <button className="add-bond-btn" onClick={() => setShowAddModal(true)}>
          + Add Bond
        </button>
        
        <div className="bond-list">
          {bondLadder.map(bond => (
            <div key={bond.id} className="bond-chip">
              <span>${(bond.parValue / 1000).toFixed(0)}k @ {bond.maturityYears}Y</span>
              <button onClick={() => removeBond(bond.id)}>×</button>
            </div>
          ))}
        </div>
      </div>
      
      {showAddModal && (
        <div className="modal-overlay">
          <div className="add-bond-modal">
            <h4>Add Bond to Ladder</h4>
            <div className="form-group">
              <label>Par Value ($)</label>
              <input
                type="number"
                value={newBond.parValue}
                onChange={e => setNewBond({ ...newBond, parValue: parseInt(e.target.value) || 0 })}
              />
            </div>
            <div className="form-group">
              <label>Maturity (Years)</label>
              <input
                type="number"
                min="1"
                max="30"
                value={newBond.maturityYears}
                onChange={e => setNewBond({ ...newBond, maturityYears: parseInt(e.target.value) || 1 })}
              />
            </div>
            <div className="modal-actions">
              <button onClick={() => setShowAddModal(false)}>Cancel</button>
              <button className="primary" onClick={handleAddBond}>Add</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default BondLadder;
