import React, { useState, useEffect } from 'react';
import { politicsService } from '../services/politicsService';
import './PoliticalAlpha.css';

/**
 * Political Alpha Dashboard Page
 * Visualizes congressional trades and lobbying correlations.
 */
const PoliticalAlpha = () => {
    const [disclosures, setDisclosures] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                const result = await politicsService.getDisclosures();
                setDisclosures(result.data || []);
            } catch (err) {
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) return <div className="loading">Analyzing Capitol Hill...</div>;
    if (error) return <div className="error">Error: {error}</div>;

    return (
        <div className="political-alpha-container">
            <h1> Political Alpha Tracker</h1>
            <p className="subtitle">Tracking Congressional Disclosure & Lobbying Correlation</p>

            <div className="disclosures-grid">
                {disclosures.map((d, index) => (
                    <div key={index} className={`disclosure-card ${d.transaction}`}>
                        <div className="card-header">
                            <span className="member-name">{d.member}</span>
                            <span className={`transaction-badge ${d.transaction}`}>{d.transaction}</span>
                        </div>
                        <div className="card-body">
                            <div className="ticker-info">
                                <span className="ticker-symbol">{d.ticker}</span>
                                <span className="sector">{d.sector}</span>
                            </div>
                            <div className="amount">{d.amount_range}</div>
                            <div className="date">{d.date}</div>
                        </div>
                        <div className="card-footer">
                            <button
                                onClick={() => alert(`Analyzing Alpha for ${d.ticker}...`)}
                                className="analyze-btn"
                            >
                                Analyze Alpha
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default PoliticalAlpha;
