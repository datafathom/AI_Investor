import React, { useState, useEffect } from 'react';
import { Droplets, AlertOctagon, FileText, Loader2 } from 'lucide-react';
import useScenarioStore from '../../stores/scenarioStore';
import './BankRunSim.css';

const BankRunSim = () => {
    const { fetchBankRunDetails, impactResults, isSimulating } = useScenarioStore();
    const [stressLevel, setStressLevel] = useState(1.0);
    const bankRun = impactResults?.bankRun;

    useEffect(() => {
        const timer = setTimeout(() => {
            fetchBankRunDetails(stressLevel);
        }, 500);
        return () => clearTimeout(timer);
    }, [stressLevel]);

    return (
        <div className="bank-run-sim-widget">
            <div className="widget-header">
                <h3><Droplets size={18} className="text-cyan-500" /> Liquidity 'Bank Run' Simulator</h3>
                <div className="stress-control">
                    <label>Stress:</label>
                    <input 
                        type="range" 
                        min="1" 
                        max="5" 
                        step="0.5"
                        value={stressLevel} 
                        onChange={(e) => setStressLevel(parseFloat(e.target.value))} 
                    />
                    <span className="level-val">{stressLevel}x</span>
                </div>
            </div>

            <div className="liquidity-visualizer">
                <div className="viz-columns">
                    <div className="order-book-depth" style={{ height: `${bankRun ? 100 - (bankRun.system_stress_index * 100) : 50}%` }}>
                        <div className="depth-fill"></div>
                        <span className="depth-label">Depth</span>
                    </div>
                    <div className="spread-gap" style={{ height: `${bankRun ? bankRun.system_stress_index * 100 : 20}%` }}>
                        <div className="spread-fill"></div>
                        <span className="gap-label">Spread</span>
                    </div>
                </div>
                {isSimulating && <Loader2 className="animate-spin text-cyan-500 absolute top-1/2 left-1/2" />}
            </div>

            <div className="toxic-positions">
                <h4>Vulnerable Assets</h4>
                <div className="position-row header">
                    <span>Asset</span>
                    <span>Exit Days</span>
                    <span>Slippage</span>
                </div>
                {bankRun?.vulnerable_positions?.map((pos, i) => (
                    <div key={i} className={`position-row ${pos.exit_days > 10 ? 'critical' : 'warning'}`}>
                        <span className="symbol">{pos.asset}</span>
                        <span className="days">{pos.exit_days.toFixed(1)} Days</span>
                        <span className="slippage">{(pos.slippage * 100).toFixed(1)}%</span>
                    </div>
                ))}
            </div>

            <div className="action-footer">
                <div className="liquidity-metric">
                    <span>Coverage: </span>
                    <strong className={bankRun?.days_of_coverage < 30 ? 'text-red-500' : 'text-green-500'}>
                        {bankRun?.days_of_coverage || 0} Days
                    </strong>
                </div>
                <button className="playbook-btn">
                    <FileText size={14} /> Emergency Exit PDF
                </button>
            </div>
        </div>
    );
};

export default BankRunSim;
