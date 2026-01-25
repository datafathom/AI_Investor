import React from 'react';
import { Percent, TrendingUp, Briefcase, Loader2 } from 'lucide-react';
import useCashStore from '../../stores/cashStore';
import './CashOptimizer.css';

const CashOptimizer = () => {
    const { 
        sweepSuggestions, 
        getIdleCash, 
        executeSweep, 
        isLoading 
    } = useCashStore();

    const idleCash = getIdleCash();

    const handleAutoSweep = async () => {
        if (sweepSuggestions.length === 0) return;
        try {
            await executeSweep(sweepSuggestions[0].id);
            alert('Auto-sweep executed successfully');
        } catch (err) {
            alert(`Sweep failed: ${err.message}`);
        }
    };

    return (
        <div className={`cash-optimizer-widget ${isLoading ? 'loading-opacity' : ''}`}>
            <div className="widget-header">
                <h3><Percent size={18} /> Cash Optimization</h3>
            </div>

            <div className="idle-cash-banner">
                <span className="label">Idle Cash Detected</span>
                <span className="amount">${idleCash.toLocaleString()}</span>
                <button 
                    className="sweep-btn" 
                    onClick={handleAutoSweep}
                    disabled={isLoading || sweepSuggestions.length === 0}
                >
                    {isLoading ? <Loader2 className="spinning" size={14} /> : 'Auto-Sweep'}
                </button>
            </div>

            <div className="opportunities-list">
                <h4>Yield Opportunities via Sweep ({sweepSuggestions.length})</h4>
                {sweepSuggestions.length === 0 ? (
                    <div className="no-opportunities">All cash optimized</div>
                ) : (
                    sweepSuggestions.map((opp) => (
                        <div key={opp.id} className="opportunity-card">
                            <div className="opp-icon">
                                <TrendingUp size={16} />
                            </div>
                            <div className="opp-info">
                                <span className="opp-name">To: {opp.toVehicle}</span>
                                <span className="opp-meta">Amount: ${opp.amount.toLocaleString()}</span>
                            </div>
                            <div className="opp-yield">
                                {opp.projectedYield.toFixed(2)}% <span className="apy">APY</span>
                            </div>
                        </div>
                    ))
                )}
            </div>

            <div className="yield-chart-placeholder">
                <div className="chart-label">Historical Yield Curve (30D)</div>
                <div className="chart-mock">
                    <div className="bar" style={{ height: '60%' }}></div>
                    <div className="bar" style={{ height: '70%' }}></div>
                    <div className="bar" style={{ height: '85%' }}></div>
                    <div className="bar" style={{ height: '80%' }}></div>
                    <div className="bar active" style={{ height: '95%' }}></div>
                </div>
            </div>
        </div>
    );
};

export default CashOptimizer;
