import React, { useState } from 'react';
import { Check, X, AlertTriangle, HelpCircle } from 'lucide-react';
import './ConsensusBar.css';

/**
 * Consensus Progress Bar 
 * 
 * Shows voting agreement among AI agents with 70% threshold.
 */
const ConsensusBar = ({ votes = [], threshold = 70, onApprove }) => {
    const [showBreakdown, setShowBreakdown] = useState(false);

    // Mock votes if not provided
    const defaultVotes = [
        { agent: 'Bull', vote: 'for', reason: 'Strong momentum signals' },
        { agent: 'Bear', vote: 'against', reason: 'Overvalued sector' },
        { agent: 'Neutral', vote: 'for', reason: 'Risk/reward favorable' },
        { agent: 'Risk Officer', vote: 'for', reason: 'Within position limits' },
        { agent: 'Momentum', vote: 'for', reason: 'Trend alignment' },
    ];

    const activeVotes = votes.length > 0 ? votes : defaultVotes;
    
    const forVotes = activeVotes.filter(v => v.vote === 'for').length;
    const againstVotes = activeVotes.filter(v => v.vote === 'against').length;
    const abstainVotes = activeVotes.filter(v => v.vote === 'abstain').length;
    const totalVotes = activeVotes.length;
    
    const consensusPercent = (forVotes / totalVotes) * 100;
    const isApproved = consensusPercent >= threshold;

    const getBarColor = () => {
        if (consensusPercent >= 70) return 'var(--color-success)';
        if (consensusPercent >= 50) return 'var(--color-warning)';
        return 'var(--color-danger)';
    };

    return (
        <div className="consensus-bar-widget">
            <div className="widget-header">
                <h3>Voting Consensus</h3>
                <span className={`consensus-badge ${isApproved ? 'approved' : 'pending'}`}>
                    {isApproved ? 'APPROVED' : 'PENDING'}
                </span>
            </div>

            <div className="progress-section">
                <div className="progress-bar">
                    <div 
                        className="progress-fill" 
                        style={{ width: `${consensusPercent}%`, background: getBarColor() }}
                    ></div>
                    <div className="threshold-marker" style={{ left: `${threshold}%` }}></div>
                </div>
                <div className="progress-labels">
                    <span>{consensusPercent.toFixed(0)}% Consensus</span>
                    <span className="threshold-label">{threshold}% Required</span>
                </div>
            </div>

            <div className="vote-summary">
                <div className="vote-count for">
                    <Check size={14} />
                    <span>{forVotes} For</span>
                </div>
                <div className="vote-count against">
                    <X size={14} />
                    <span>{againstVotes} Against</span>
                </div>
                <div className="vote-count abstain">
                    <HelpCircle size={14} />
                    <span>{abstainVotes} Abstain</span>
                </div>
            </div>

            {activeVotes.filter(v => v.vote === 'against').length > 0 && (
                <div className="dissenters">
                    <div className="dissenters-header" onClick={() => setShowBreakdown(!showBreakdown)}>
                        <AlertTriangle size={12} />
                        <span>Dissenting Agents</span>
                    </div>
                    {showBreakdown && (
                        <div className="dissent-list">
                            {activeVotes.filter(v => v.vote === 'against').map((v, i) => (
                                <div key={i} className="dissent-item">
                                    <span className="dissent-agent">{v.agent}</span>
                                    <span className="dissent-reason">{v.reason}</span>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            )}

            <button 
                className={`approve-btn ${isApproved ? 'enabled' : 'disabled'}`}
                disabled={!isApproved}
                onClick={onApprove}
            >
                {isApproved ? 'Approve Execution' : 'Awaiting Consensus'}
            </button>
        </div>
    );
};

export default ConsensusBar;
