import React, { useState } from "react";
import {
  Zap,
  TrendingDown,
  TrendingUp,
  Play,
  RotateCcw,
  AlertTriangle,
  RefreshCw,
} from "lucide-react";
import useScenarioStore from "../../stores/scenarioStore";
import "./WhatIfSimulator.css";

/**
 * StressTest - Refactored multi-event simulator.
 * Phase 60: Supports multi-event selection and backend revaluation.
 */
const StressTest = () => {
  const { presetScenarios, runScenario, isSimulating, impactResults, reset } =
    useScenarioStore();
  const [selectedId, setSelectedId] = useState(null);

  const handleRun = () => {
    if (selectedId) runScenario(selectedId);
  };

  return (
    <div className="what-if-simulator stress-test">
      <div className="widget-header">
        <Zap size={16} className="text-yellow-500" />
        <h3>Macro Stress Test</h3>
        <button
          className="reset-btn"
          onClick={() => {
            setSelectedId(null);
            reset();
          }}
        >
          <RotateCcw size={12} /> Reset
        </button>
      </div>

      <div className="scenarios-grid">
        {presetScenarios.map((scenario) => (
          <div
            key={scenario.id}
            className={`scenario-card ${selectedId === scenario.id ? "active" : ""} ${scenario.equityDrop < 0 ? "bearish" : "bullish"}`}
            onClick={() => setSelectedId(scenario.id)}
          >
            <div className="scenario-header">
              {scenario.equityDrop < 0 ? (
                <TrendingDown size={14} />
              ) : (
                <TrendingUp size={14} />
              )}
              <span className="scenario-name">{scenario.name}</span>
            </div>
            <div className="scenario-impact">
              Equity: {scenario.equityDrop}% | Bond: {scenario.bondDrop}%
            </div>
          </div>
        ))}
      </div>

      {impactResults?.portfolio_impact_pct !== undefined && (
        <div className="impact-summary-p60">
          <div className="impact-stat">
            <label>Net Impact</label>
            <span
              className={
                impactResults.portfolio_impact_pct < 0 ? "negative" : "positive"
              }
            >
              {impactResults.portfolio_impact_pct?.toFixed(2)}%
            </span>
          </div>
          <div className="impact-stat">
            <label>New Portfolio Value</label>
            <span>${(impactResults.new_value / 1000000)?.toFixed(2)}M</span>
          </div>
        </div>
      )}

      <button
        className={`run-simulation-btn ${isSimulating ? "loading" : ""}`}
        onClick={handleRun}
        disabled={!selectedId || isSimulating}
      >
        {isSimulating ? (
          <RefreshCw className="animate-spin" size={14} />
        ) : (
          <Play size={14} />
        )}
        {isSimulating ? "Simulating..." : "Run Stress Test"}
      </button>

      {selectedId === "bankrun" && (
        <div className="p60-warning">
          <AlertTriangle size={14} /> Liquidity crisis detected. Open Bank Run
          Sim.
        </div>
      )}
    </div>
  );
};

export default StressTest;
