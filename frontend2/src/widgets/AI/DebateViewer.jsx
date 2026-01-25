/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/AI/DebateViewer.jsx
 * ROLE: AI Visualization Widget
 * PURPOSE: Visualizes the multi-persona debate (Bull vs. Bear).
 * ==============================================================================
 */

import React, { useState } from 'react';
import PropTypes from 'prop-types';
import useDebateStore from '../../stores/debateStore';
import './DebateViewer.css';

const DebateViewer = ({ initialTicker = 'SPY', mock = true }) => {
    const { debateResult, runDebate, loading, error } = useDebateStore();
    const [ticker, setTicker] = useState(initialTicker);

    const handleStart = () => {
        if (ticker) runDebate(ticker, mock);
    };

    return (
        <div className="debate-viewer">
            <div className="debate-header">
                <h3>🏛️ Debate Chamber</h3>
                <div className="debate-controls">
                    <input 
                        type="text" 
                        value={ticker} 
                        onChange={(e) => setTicker(e.target.value.toUpperCase())}
                        placeholder="TICKER"
                        maxLength={5}
                    />
                    <button onClick={handleStart} disabled={loading || !ticker}>
                        {loading ? 'CONVENING...' : 'START DEBATE'}
                    </button>
                </div>
            </div>

            {error && <div className="debate-error">{error}</div>}

            <div className="debate-stage">
                {/* BULL PODIUM */}
                <div className="podium bull">
                    <div className="avatar">🐂</div>
                    <h4>The Bull</h4>
                    <div className={`speech-bubble ${debateResult ? 'visible' : ''}`}>
                        {loading ? <span className="typing">Thinking...</span> : (debateResult?.bull_thesis || "Ready to debate.")}
                    </div>
                </div>

                {/* MODERATOR / CONSENSUS */}
                <div className="podium moderator">
                    <div className="avatar">⚖️</div>
                    <h4>Consensus</h4>
                    {debateResult && (
                        <div className="consensus-card">
                            <div className={`verdict ${debateResult.verdict.toLowerCase()}`}>
                                {debateResult.verdict}
                            </div>
                            <div className="confidence">
                                Confidence: {debateResult.score}%
                            </div>
                            <p className="summary">{debateResult.consensus}</p>
                        </div>
                    )}
                </div>

                {/* BEAR PODIUM */}
                <div className="podium bear">
                    <div className="avatar">🐻</div>
                    <h4>The Bear</h4>
                    <div className={`speech-bubble ${debateResult ? 'visible' : ''}`}>
                        {loading ? <span className="typing">Thinking...</span> : (debateResult?.bear_thesis || "Ready to debate.")}
                    </div>
                </div>
            </div>

            {mock && <div className="mock-badge">SIMULATION MODE</div>}
        </div>
    );
};

DebateViewer.propTypes = {
    initialTicker: PropTypes.string,
    mock: PropTypes.bool
};

export default DebateViewer;
