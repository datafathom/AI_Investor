/**
 * ==============================================================================
 * FILE: frontend2/src/pages/NewsSentimentDashboard.jsx
 * ROLE: News & Sentiment Analysis Dashboard
 * PURPOSE:  - News Aggregation & Sentiment Analysis
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
import { StorageService } from '../utils/storageService';

import useNewsStore from '../stores/newsStore';
import './NewsSentimentDashboard.css';

const NewsSentimentDashboard = () => {
  const {
      headlines,
      analyzedTopics,
      loading,
      fetchHeadlines,
      analyzeTopic
  } = useNewsStore();

  const [selectedSymbol, setSelectedSymbol] = useState('AAPL');
  
  // Derived state for the selected symbol's sentiment
  const sentiment = analyzedTopics[selectedSymbol.toLowerCase()] || null;
  const isHeadlinesLoading = loading.headlines;

  useEffect(() => {
    fetchHeadlines();
    if (selectedSymbol) {
        analyzeTopic(selectedSymbol);
    }
  }, [fetchHeadlines, analyzeTopic]); // Initial load

  const handleAnalyze = () => {
      if (selectedSymbol) {
          analyzeTopic(selectedSymbol);
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
        <p className="subtitle">: News Aggregation & Sentiment Analysis</p>
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
            <button onClick={handleAnalyze}>Analyze</button>
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
          {isHeadlinesLoading ? (
            <div className="loading">Loading news...</div>
          ) : headlines.length > 0 ? (
            <div className="articles-list">
              {headlines.map((article, idx) => (
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
