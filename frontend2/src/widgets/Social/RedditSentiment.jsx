/**
 * ==============================================================================
 * FILE: frontend2/src/widgets/Social/RedditSentiment.jsx
 * ROLE: Social Data Widget
 * PURPOSE: Displays Reddit hype, sentiment scores, and top posts.
 * ==============================================================================
 */

import React, { useEffect, useState } from 'react';
import PropTypes from 'prop-types';
import useSocialStore from '../../stores/socialStore';
import './RedditSentiment.css';

const RedditSentiment = ({ subreddit = 'wallstreetbets', initialTicker = 'NVDA', mock = true }) => {
    const { posts, sentimentData, fetchPosts, analyzeSentiment, loading } = useSocialStore();
    const [activeTicker, setActiveTicker] = useState(initialTicker);

    useEffect(() => {
        fetchPosts(subreddit, 10, mock);
        analyzeSentiment(activeTicker, mock);
        
        // Refresh every 30s
        const interval = setInterval(() => {
            fetchPosts(subreddit, 10, mock);
            analyzeSentiment(activeTicker, mock);
        }, 30000);
        return () => clearInterval(interval);
    }, [subreddit, activeTicker, mock, fetchPosts, analyzeSentiment]);

    const sentiment = sentimentData[activeTicker] || {};
    
    const getSentimentColor = (label) => {
        if (label === 'BULLISH') return '#10b981'; // Green
        if (label === 'BEARISH') return '#ef4444'; // Red
        return '#9ca3af'; // Grey
    };

    return (
        <div className="reddit-sentiment-widget">
            <div className="widget-header">
                <h3>r/{subreddit} Pulse</h3>
                <div className="ticker-selector">
                    {['NVDA', 'TSLA', 'GME'].map(t => (
                        <button 
                            key={t} 
                            className={activeTicker === t ? 'active' : ''}
                            onClick={() => setActiveTicker(t)}
                        >
                            ${t}
                        </button>
                    ))}
                </div>
            </div>

            <div className="sentiment-dashboard">
                <div className="metric-card">
                    <span className="label">Hype Score</span>
                    <div className="value hype">
                        {sentiment.hype_score ?? '--'}
                        <span className="unit">/100</span>
                    </div>
                </div>

                <div className="metric-card">
                    <span className="label">Sentiment</span>
                    <div 
                        className="value sentiment"
                        style={{ color: getSentimentColor(sentiment.sentiment_label) }}
                    >
                        {sentiment.sentiment_label ?? 'ANALYZING...'}
                    </div>
                </div>
            </div>

            <div className="feed-container">
                <h4>Trending Posts</h4>
                {loading.posts && posts.length === 0 ? (
                    <div className="loading">Loading posts...</div>
                ) : (
                    <ul className="posts-list">
                        {posts.map(post => (
                            <li key={post.id} className="post-item">
                                <div className="post-score">
                                    ⬆ {post.score > 1000 ? `${(post.score/1000).toFixed(1)}k` : post.score}
                                </div>
                                <div className="post-content">
                                    <a href={post.url} target="_blank" rel="noopener noreferrer" className="post-title">
                                        {post.title}
                                    </a>
                                    <div className="post-meta">
                                        <span>u/{post.author}</span>
                                        <span>💬 {post.num_comments}</span>
                                        <span className="sentiment-dot" style={{ 
                                            backgroundColor: post.sentiment_score > 0 ? '#10b981' : (post.sentiment_score < 0 ? '#ef4444' : '#6b7280') 
                                        }} title={`Score: ${post.sentiment_score}`} />
                                    </div>
                                </div>
                            </li>
                        ))}
                    </ul>
                )}
            </div>
            
            {mock && <div className="mock-badge">MOCK MODE</div>}
        </div>
    );
};

RedditSentiment.propTypes = {
    subreddit: PropTypes.string,
    initialTicker: PropTypes.string,
    mock: PropTypes.bool
};

export default RedditSentiment;
