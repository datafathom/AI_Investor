/**
 * ==============================================================================
 * FILE: frontend2/src/pages/NewsSentimentDashboard.jsx
 * ROLE: News & Sentiment Analysis Dashboard
 * PURPOSE: Phase 16 - News Aggregation & Sentiment Analysis
 *          Displays news articles, sentiment scores, and market impact analysis.
 * 
 * INTEGRATION POINTS:
 *    - NewsAPI: /api/news endpoints
 *    - NewsStore: News state management
 * 
 * FEATURES:
 *    - News article feed
 *    - Sentiment analysis by symbol
 *    - Market impact assessment
 *    - Trending news
 * 
 * AUTHOR: AI Investor Team
 * CREATED: 2026-01-21
 * LAST_MODIFIED: 2026-01-21
 * ==============================================================================
 */

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './NewsSentimentDashboard.css';

const BACKEND_PORT = import.meta.env.VITE_BACKEND_PORT || '5050';
const API_BASE = `http://localhost:${BACKEND_PORT}`;

const NewsSentimentDashboard = () => {
  const [articles, setArticles] = useState([]);
  const [sentiment, setSentiment] = useState(null);
  const [selectedSymbol, setSelectedSymbol] = useState('AAPL');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadTrendingNews();
    loadSentiment(selectedSymbol);
  }, [selectedSymbol]);

  const loadTrendingNews = async () => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_BASE}/api/news/trending`, {
        params: { limit: 20 }
      });
      setArticles(res.data.data || []);
    } catch (error) {
      console.error('Error loading news:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadSentiment = async (symbol) => {
    try {
      const res = await axios.get(`${API_BASE}/api/news/sentiment/${symbol}`);
      setSentiment(res.data.data);
    } catch (error) {
      console.error('Error loading sentiment:', error);
    }
  };

  const getSentimentColor = (score) => {
    if (score > 0.3) return '#00ff88';
    if (score > 0.1) return '#88ff00';
    if (score < -0.3) return '#ff4444';
    if (score < -0.1) return '#ff8844';
    return '#888888';
  };

  return (
    <div className="news-sentiment-dashboard">
      <div className="dashboard-header">
        <h1>News & Sentiment Analysis</h1>
        <p className="subtitle">Phase 16: News Aggregation & Sentiment Analysis</p>
      </div>

      <div className="dashboard-content">
        {/* Sentiment Analysis */}
        <div className="sentiment-panel">
          <h2>Sentiment Analysis</h2>
          <div className="symbol-selector">
            <input
              type="text"
              value={selectedSymbol}
              onChange={(e) => setSelectedSymbol(e.target.value.toUpperCase())}
              placeholder="Enter symbol"
              className="symbol-input"
            />
            <button onClick={() => loadSentiment(selectedSymbol)}>Analyze</button>
          </div>
          
          {sentiment && (
            <div className="sentiment-results">
              <div className="sentiment-score" style={{ color: getSentimentColor(sentiment.overall_sentiment) }}>
                <div className="score-value">{(sentiment.overall_sentiment * 100).toFixed(1)}%</div>
                <div className="score-label">{sentiment.sentiment_label?.replace('_', ' ').toUpperCase()}</div>
              </div>
              <div className="sentiment-stats">
                <div className="stat">
                  <span className="stat-label">Articles:</span>
                  <span className="stat-value">{sentiment.article_count}</span>
                </div>
                <div className="stat">
                  <span className="stat-label">Bullish:</span>
                  <span className="stat-value">{sentiment.bullish_count}</span>
                </div>
                <div className="stat">
                  <span className="stat-label">Bearish:</span>
                  <span className="stat-value">{sentiment.bearish_count}</span>
                </div>
                <div className="stat">
                  <span className="stat-label">Confidence:</span>
                  <span className="stat-value">{(sentiment.confidence * 100).toFixed(0)}%</span>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* News Feed */}
        <div className="news-feed">
          <h2>Trending News</h2>
          {loading ? (
            <div className="loading">Loading news...</div>
          ) : articles.length > 0 ? (
            <div className="articles-list">
              {articles.map((article, idx) => (
                <div key={idx} className="article-card">
                  <div className="article-header">
                    <span className="article-source">{article.source}</span>
                    <span className="article-date">
                      {new Date(article.published_date).toLocaleDateString()}
                    </span>
                  </div>
                  <h3 className="article-title">{article.title}</h3>
                  <p className="article-content">{article.content?.substring(0, 200)}...</p>
                  {article.symbols && article.symbols.length > 0 && (
                    <div className="article-symbols">
                      {article.symbols.map((sym, i) => (
                        <span key={i} className="symbol-tag">{sym}</span>
                      ))}
                    </div>
                  )}
                  {article.sentiment_score !== null && (
                    <div className="article-sentiment">
                      <span>Sentiment: </span>
                      <span style={{ color: getSentimentColor(article.sentiment_score) }}>
                        {(article.sentiment_score * 100).toFixed(0)}%
                      </span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="no-data">No news articles available</div>
          )}
        </div>
      </div>
    </div>
  );
};

export default NewsSentimentDashboard;
