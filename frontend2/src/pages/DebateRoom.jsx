/**
 * DebateRoom.jsx
 * 
 * A dashboard view where multiple AI personas debate a market entry.
 */

import React, { useState } from 'react';
import debateService from '../services/debateService';
import './DebateRoom.css';
import { MessageSquare, ShieldCheck, TrendingUp, TrendingDown, Users, Play } from 'lucide-react';

const DebateRoom = () => {
    const [ticker, setTicker] = useState('SPY');
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const runDebate = async () => {
        setLoading(true);
        try {
            const data = await debateService.triggerDebate(ticker, `Analyzing ${ticker} for potential trade entry.`);
            setResult(data);
        } catch (error) {
            console.error('Debate failed:', error);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="debate-container glass">
            <header className="debate-header">
                <div className="header-title">
                    <Users className="icon-main" />
                    <h1>The Debate Chamber</h1>
                    <span className="badge">Phase 38: Multi-Persona Consensus</span>
                </div>
                <div className="debate-controls">
                    <input
                        type="text"
                        value={ticker}
                        onChange={(e) => setTicker(e.target.value.toUpperCase())}
                        placeholder="Enter Ticker..."
                        className="ticker-input"
                    />
                    <button onClick={runDebate} disabled={loading} className="btn-run">
                        {loading ? 'Debating...' : <><Play size={16} /> Run Committee</>}
                    </button>
                </div>
            </header>

            <main className="debate-grid">
                {result ? (
                    <>
                        <div className="debate-feed">
                            <h2>Committee Arguments</h2>
                            <div className="arguments-list">
                                {result.responses.map((resp, idx) => (
                                    <div key={idx} className={`argument-card ${resp.signal.toLowerCase()}`}>
                                        <div className="persona-info">
                                            {resp.persona === 'The Bull' && <TrendingUp className="persona-icon bullish" />}
                                            {resp.persona === 'The Bear' && <TrendingDown className="persona-icon bearish" />}
                                            {resp.persona === 'The Risk Manager' && <ShieldCheck className="persona-icon safety" />}
                                            <h3>{resp.persona}</h3>
                                            <span className={`signal-tag ${resp.signal.toLowerCase()}`}>{resp.signal}</span>
                                        </div>
                                        <p className="reasoning">{resp.reasoning}</p>
                                    </div>
                                ))}
                            </div>
                        </div>

                        <div className="consensus-panel card glass">
                            <h2>Final Verdict</h2>
                            <div className={`verdict-display ${result.consensus.decision.toLowerCase()}`}>
                                <div className="verdict-value">{result.consensus.decision}</div>
                                <p>Consensus: {(result.consensus.buy_ratio * 100).toFixed(0)}% Approval</p>
                            </div>

                            <div className="consensus-metrics">
                                <div className="metric">
                                    <label>Avg Conviction</label>
                                    <span>{result.consensus.avg_score}</span>
                                </div>
                                <div className="metric">
                                    <label>Approved?</label>
                                    <span className={result.consensus.is_approved ? 'text-success' : 'text-danger'}>
                                        {result.consensus.is_approved ? 'YES' : 'NO'}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </>
                ) : (
                    <div className="empty-state">
                        <Users size={64} className="faint" />
                        <p>Initiate a Ticker to summon the Investment Committee.</p>
                    </div>
                )}
            </main>
        </div>
    );
};

export default DebateRoom;
