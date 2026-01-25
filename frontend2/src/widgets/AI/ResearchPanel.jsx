/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/AI/ResearchPanel.jsx
 * ROLE: AI Visualization Widget
 * PURPOSE: Interactive Q&A interface with real-time citations.
 * ==============================================================================
 */

import React, { useState } from 'react';
import PropTypes from 'prop-types';
import useResearchStore from '../../stores/researchStore';
import './ResearchPanel.css';

const ResearchPanel = ({ mock = true }) => {
    const { history, askQuestion, loading, error, clearHistory } = useResearchStore();
    const [query, setQuery] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (query.trim()) {
            askQuestion(query, mock);
            setQuery('');
        }
    };

    return (
        <div className="research-panel">
            <div className="research-header">
                <h3>🔍 Deep Research</h3>
                <button className="clear-btn" onClick={clearHistory} disabled={history.length === 0}>
                    Clear
                </button>
            </div>

            <div className="research-feed">
                {history.length === 0 && !loading && (
                    <div className="empty-state">
                        <p>Ask a question to begin research.</p>
                        <div className="suggestions">
                            <span onClick={() => setQuery("Why is NVDA up today?")}>Why is NVDA up?</span>
                            <span onClick={() => setQuery("Latest CPI inflation data")}>Latest CPI Data</span>
                            <span onClick={() => setQuery("Oil price outlook 2026")}>Oil Outlook</span>
                        </div>
                    </div>
                )}
                
                {history.map((item) => (
                    <div key={item.id} className="research-item">
                        <div className="question">
                            <span className="user-avatar">👤</span>
                            <p>{item.query}</p>
                            <span className="time">{item.timestamp}</span>
                        </div>
                        <div className="answer">
                            <span className="ai-avatar">🤖</span>
                            <div className="content">
                                <p>{item.answer}</p>
                                {item.citations && item.citations.length > 0 && (
                                    <div className="citations">
                                        <h6>Sources:</h6>
                                        <ul>
                                            {item.citations.map((cite, idx) => (
                                                <li key={idx}>
                                                    <a href={cite} target="_blank" rel="noopener noreferrer">
                                                        [{idx + 1}] {new URL(cite).hostname}
                                                    </a>
                                                </li>
                                            ))}
                                        </ul>
                                    </div>
                                )}
                            </div>
                        </div>
                    </div>
                ))}
                
                {loading && (
                    <div className="research-item loading">
                        <div className="question">
                            <span className="user-avatar">👤</span>
                            <p>Analyzing...</p>
                        </div>
                        <div className="answer">
                            <span className="ai-avatar pulse">🤖</span>
                            <div className="content">
                                <span className="typing-indicator">Searching sources...</span>
                            </div>
                        </div>
                    </div>
                )}
                
                {error && <div className="error-message">{error}</div>}
            </div>

            <form className="research-input" onSubmit={handleSubmit}>
                <input 
                    type="text" 
                    value={query} 
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Ask about markets, stocks, or economics..."
                    disabled={loading}
                />
                <button type="submit" disabled={loading || !query.trim()}>
                    ➤
                </button>
            </form>
            
            {mock && <div className="mock-label">POWERED BY PERPLEXITY (MOCK)</div>}
        </div>
    );
};

ResearchPanel.propTypes = {
    mock: PropTypes.bool
};

export default ResearchPanel;
