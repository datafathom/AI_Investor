/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/News/NewsFeed.jsx
 * ROLE: Information Display Widget
 * PURPOSE: Displays a real-time feed of news articles with sentiment analysis.
 *          Supports filtering by ticker and sentiment.
 *          
 * INTEGRATION POINTS:
 *     - newsStore: Zustand state management for news articles.
 *     - SentimentResult: Displays sentiment badges (BULLISH/BEARISH).
 *     
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * ==============================================================================
 */

import React, { useEffect, useState } from 'react';
import useNewsStore from '../../stores/newsStore';
import './NewsFeed.css';

const NewsFeed = ({ topic = null, mock = false }) => {
    const { 
        headlines, 
        marketSentiment, 
        analyzedTopics, 
        fetchHeadlines, 
        analyzeTopic, 
        loading, 
        error 
    } = useNewsStore();

    const [filter, setFilter] = useState('ALL');

    useEffect(() => {
        if (topic) {
            analyzeTopic(topic, mock);
        } else {
            fetchHeadlines(mock);
        }
    }, [topic, mock, fetchHeadlines, analyzeTopic]);

    const articles = topic ? (analyzedTopics[topic.toLowerCase()] || []) : headlines;

    const filteredArticles = articles.filter(art => {
        if (filter === 'ALL') return true;
        return art.label === filter;
    });

    if (loading.headlines || loading.topics) {
        return (
            <div className="news-feed news-feed--loading">
                <div className="news-feed__skeleton-header"></div>
                <div className="news-feed__skeleton-article"></div>
                <div className="news-feed__skeleton-article"></div>
            </div>
        );
    }

    const getSentimentColor = (label) => {
        switch (label) {
            case 'BULLISH': return 'sentiment--bullish';
            case 'BEARISH': return 'sentiment--bearish';
            default: return 'sentiment--neutral';
        }
    };

    return (
        <div className="news-feed">
            <div className="news-feed__header">
                <div className="news-feed__title">
                    {topic ? `News: ${topic}` : 'Market Headlines'}
                </div>
                {!topic && (
                    <div className={`news-feed__market-status ${getSentimentColor(marketSentiment.label)}`}>
                        {marketSentiment.label} ({marketSentiment.average_score.toFixed(2)})
                    </div>
                )}
            </div>

            <div className="news-feed__filters">
                {['ALL', 'BULLISH', 'NEUTRAL', 'BEARISH'].map(f => (
                    <button 
                        key={f}
                        className={`filter-btn ${filter === f ? 'active' : ''}`}
                        onClick={() => setFilter(f)}
                    >
                        {f}
                    </button>
                ))}
            </div>

            <div className="news-feed__content">
                {filteredArticles.length === 0 ? (
                    <div className="news-feed__empty">No articles found matching filters.</div>
                ) : (
                    filteredArticles.map((res, idx) => (
                        <div key={idx} className="news-article">
                            <div className="news-article__meta">
                                <span className={`news-article__sentiment ${getSentimentColor(res.label)}`}>
                                    {res.label}
                                </span>
                                <span className="news-article__source">{res.article.source_name}</span>
                                <span className="news-article__date">
                                    {new Date(res.article.publishedAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                </span>
                            </div>
                            <h4 className="news-article__title">
                                <a href={res.article.url} target="_blank" rel="noopener noreferrer">
                                    {res.article.title}
                                </a>
                            </h4>
                            <p className="news-article__description">{res.article.description}</p>
                            {res.indicators.length > 0 && (
                                <div className="news-article__indicators">
                                    {res.indicators.map(ind => (
                                        <span key={ind} className="indicator-tag">{ind}</span>
                                    ))}
                                </div>
                            )}
                        </div>
                    ))
                )}
            </div>

            <div className="news-feed__footer">
                <span>Source: NewsAPI.org</span>
                {mock && <span className="mock-tag">Simulation Mode</span>}
            </div>
        </div>
    );
};

export default NewsFeed;
