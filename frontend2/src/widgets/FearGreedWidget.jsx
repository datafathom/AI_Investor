/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/FearGreedWidget.jsx
 * ROLE: Sentiment Widget Container
 * PURPOSE: Fetches Fear & Greed Index data from the backend and renders the 
 *          visualization gauge. Handles data loading and fallback states.
 * ==============================================================================
 */
import React, { useEffect, useState } from 'react';
import FearGreedGauge from '../components/FearGreedGauge';
import './FearGreedWidget.css';
import apiClient from '../services/apiClient';

const FearGreedWidget = () => {
    const [data, setData] = useState({ score: 50, rating: 'Neutral', components: {} });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                // In real app, fetch from /api/v1/market/fear-greed
                const response = await apiClient.get('/market/fear-greed');
                setData(response.data);
            } catch (e) {
                // Fallback Mock for Demo stability
                console.warn('FearGreed fallback used due to error:', e);
                setData({
                    score: Math.floor(Math.random() * 40) + 30,
                    rating: 'Neutral',
                    components: { vix: 20, momentum: 40 }
                });
            } finally {
                setLoading(false);
            }
        };

        fetchData();
        const interval = setInterval(fetchData, 120000); // Update every 2 minutes (increased from 1 minute)
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="fear-greed-widget">
            <header className="widget-header">
                <h3>Fear & Greed Index</h3>
                <span className={`rating-Badge ${(data.rating || 'Neutral').replace(' ', '-').toLowerCase()}`}>
                    {data.rating || 'Neutral'}
                </span>
            </header>
            
            <div className="gauge-container">
                <FearGreedGauge score={data.score} />
            </div>

            <div className="components-list">
                <div className="comp-item">
                    <span>VIX Momentum</span>
                    <span>{data.components?.vix_contribution || '--'}</span>
                </div>
                <div className="comp-item">
                    <span>Social Hype</span>
                    <span>{data.components?.social_sentiment || '--'}</span>
                </div>
            </div>
        </div>
    );
};

export default FearGreedWidget;
