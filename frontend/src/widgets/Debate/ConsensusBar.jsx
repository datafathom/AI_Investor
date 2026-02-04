import React from 'react';
import { CheckCircle, AlertTriangle, XCircle, Users } from 'lucide-react';
import useDebateStore from '../../stores/debateStore';
import './ConsensusBar.css';

/**
 * ConsensusBar - Voting Consensus Progress Visualization
 * 
 * : Displays real-time voting consensus with 70% threshold,
 * dissent highlighting, and approval status.
 */
const ConsensusBar = () => {
    const {
        consensus,
        personas,
        isDebating,
        getConsensusPercentage,
        isConsensusReached,
        getDissentingPersonas
    } = useDebateStore();
    
    const consensusPercentage = getConsensusPercentage();
    const consensusReached = isConsensusReached();
    const dissentingPersonas = getDissentingPersonas();
    const threshold = 70;
    
    const getStatusIcon = () => {
        if (!consensus) return <Users size={16} />;
        if (consensus.isApproved) return <CheckCircle size={16} />;
        if (consensusReached) return <AlertTriangle size={16} />;
        return <XCircle size={16} />;
    };
    
    const getStatusText = () => {
        if (!consensus) return 'Awaiting Debate';
        if (consensus.isApproved) return 'Execution Approved';
        if (consensusReached) return 'Consensus Reached (Low Confidence)';
        return 'No Consensus';
    };
    
    const getStatusClass = () => {
        if (!consensus) return 'status-pending';
        if (consensus.isApproved) return 'status-approved';
        if (consensusReached) return 'status-warning';
        return 'status-rejected';
    };
    
    const getVoteClass = (vote) => {
        switch (vote) {
            case 'BUY': return 'vote-buy';
            case 'SELL': return 'vote-sell';
            case 'HOLD': return 'vote-hold';
            default: return '';
        }
    };
    
    return (
        <div className="consensus-bar-widget">
            <div className="consensus-header">
                <h3>Voting Consensus</h3>
                <div className={`status-badge ${getStatusClass()}`}>
                    {getStatusIcon()}
                    <span>{getStatusText()}</span>
                </div>
            </div>
            
            <div className="progress-section">
                <div className="progress-labels">
                    <span>Agreement</span>
                    <span className="percentage">{consensusPercentage}%</span>
                </div>
                
                <div className="progress-track">
                    <div 
                        className={`progress-fill ${consensusReached ? 'reached' : ''}`}
                        style={{ width: `${consensusPercentage}%` }}
                    />
                    <div 
                        className="threshold-marker"
                        style={{ left: `${threshold}%` }}
                    >
                        <span className="threshold-label">{threshold}%</span>
                    </div>
                </div>
                
                <div className="progress-sublabel">
                    {consensusPercentage < threshold 
                        ? `${threshold - consensusPercentage}% more needed for consensus`
                        : 'Threshold met'
                    }
                </div>
            </div>
            
            <div className="votes-section">
                <h4>Individual Votes</h4>
                <div className="votes-grid">
                    {personas.map(persona => (
                        <div 
                            key={persona.id} 
                            className={`vote-card ${persona.currentVote ? getVoteClass(persona.currentVote) : 'no-vote'}`}
                        >
                            <span className="vote-avatar">{persona.avatar}</span>
                            <div className="vote-info">
                                <span className="vote-name">{persona.name}</span>
                                <span className="vote-signal">
                                    {persona.currentVote || 'Pending'}
                                </span>
                            </div>
                            {persona.currentVote && (
                                <div className="confidence-bar">
                                    <div 
                                        className="confidence-fill"
                                        style={{ width: `${persona.confidence * 100}%` }}
                                    />
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>
            
            {dissentingPersonas.length > 0 && (
                <div className="dissent-section">
                    <h4>
                        <AlertTriangle size={14} />
                        Dissenting Voices
                    </h4>
                    <div className="dissent-list">
                        {dissentingPersonas.map(persona => (
                            <div 
                                key={persona.id} 
                                className="dissent-item"
                                title={`${persona.name} voted ${persona.currentVote}`}
                            >
                                <span className="dissent-avatar">{persona.avatar}</span>
                                <span className="dissent-name">{persona.name}</span>
                                <span className={`dissent-vote ${getVoteClass(persona.currentVote)}`}>
                                    {persona.currentVote}
                                </span>
                            </div>
                        ))}
                    </div>
                </div>
            )}
            
            {consensus && (
                <div className="metrics-section">
                    <div className="metric">
                        <span className="metric-label">Decision</span>
                        <span className={`metric-value decision-${consensus.decision.toLowerCase()}`}>
                            {consensus.decision === 'NO_CONSENSUS' ? 'NO CONSENSUS' : consensus.decision}
                        </span>
                    </div>
                    <div className="metric">
                        <span className="metric-label">Avg Confidence</span>
                        <span className="metric-value">
                            {Math.round(consensus.avgScore * 100)}%
                        </span>
                    </div>
                    <div className="metric">
                        <span className="metric-label">Buy Ratio</span>
                        <span className="metric-value">
                            {Math.round(consensus.buyRatio * 100)}%
                        </span>
                    </div>
                </div>
            )}
            
            {consensus?.isApproved && (
                <button className="approve-btn" disabled={isDebating}>
                    <CheckCircle size={16} />
                    Approve Execution
                </button>
            )}
            
            {consensus && !consensus.isApproved && (
                <div className="locked-notice">
                    <XCircle size={14} />
                    <span>Execution locked until 70% consensus with &gt;60% confidence</span>
                </div>
            )}
        </div>
    );
};

export default ConsensusBar;
