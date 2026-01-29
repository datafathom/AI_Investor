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

const FearGreedWidget = () => {
    const [data, setData] = useState({ score: 50, rating: 'Neutral', components: {} });
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                // In real app, fetch from /api/v1/market/fear-greed
                // For MVP without backend running perfectly on same port/proxy yet, mock if fetch fails?
                // Or try fetch.
                const res = await fetch('http://localhost:5050/api/v1/market/fear-greed', {
                     headers: { 'Authorization': `Bearer ${localStorage.getItem('widget_os_token')}` }
                });
                
                if (res.ok) {
                    const json = await res.json();
                    setData(json);
                } else {
                    // Fallback Mock for Demo stability
                    setData({
                        score: Math.floor(Math.random() * 40) + 30,
                        rating: 'Neutral',
                        components: { vix: 20, momentum: 40 }
                    });
                }
            } catch (e) {
                 setData({
                    score: 65,
                    rating: 'Greed',
                    components: { vix: 15, momentum: 60 }
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
