# Phase 6 Implementation Plan: News & Sentiment Intelligence

> **Phase**: 6 of 33  
> **Status**: 🔴 Not Started  
> **Priority**: HIGH  
> **Estimated Duration**: 5 days  
> **Dependencies**: Phase 4, Phase 5

---

## Overview

Phase 6 builds the news and sentiment intelligence layer including multi-source news aggregation, social sentiment analysis, social trading feeds, trend detection, and rumor verification.

### Services Covered
| Service | Directory | Primary Files |
|---------|-----------|---------------|
| `news` | `services/news/` | `aggregator.py`, `rumor_classifier.py`, `nlp_tagger.py` |
| `social` | `services/social/` | `sentiment_analyzer.py`, `trend_detector.py` |
| `social_trading` | `services/social_trading/` | `feed.py`, `influencer_tracker.py` |

---

## Deliverable 1: News Aggregator Page

### 1.1 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `NewsAggregator.jsx` | `frontend/src/pages/hunter/NewsAggregator.jsx` | Page |
| `NewsCard.jsx` | `frontend/src/components/cards/NewsCard.jsx` | Card |
| `NewsFeedStream.jsx` | `frontend/src/components/streams/NewsFeedStream.jsx` | Stream |
| `NewsFilterBar.jsx` | `frontend/src/components/bars/NewsFilterBar.jsx` | Widget |
| `ArticleDetailPanel.jsx` | `frontend/src/components/panels/ArticleDetailPanel.jsx` | Panel |
| `SavedSearchesDrawer.jsx` | `frontend/src/components/drawers/SavedSearchesDrawer.jsx` | Drawer |

### 1.2 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/news/articles` | `get_news_articles()` |
| GET | `/api/v1/news/articles/{id}` | `get_article_details()` |
| GET | `/api/v1/news/sources` | `list_news_sources()` |
| POST | `/api/v1/news/saved-searches` | `create_saved_search()` |
| GET | `/api/v1/news/saved-searches` | `list_saved_searches()` |
| WS | `/ws/news/stream` | `stream_news()` |

### 1.3 End-to-End Acceptance Criteria

- [ ] **F6.1.1**: News feed shows articles from multiple sources (Reuters, Bloomberg, etc.)
- [ ] **F6.1.2**: NLP tags displayed (earnings, M&A, regulatory, macro, etc.)
- [ ] **F6.1.3**: Filter by source, tag, ticker, date range, sentiment
- [ ] **F6.1.4**: Article detail shows full text, related tickers, sentiment score
- [ ] **F6.1.5**: Save custom searches with email/Slack notification option
- [ ] **I6.1.1**: Real-time articles via WebSocket subscription
- [ ] **I6.1.2**: Pagination with cursor-based infinite scroll
- [ ] **R6.1.1**: Article schema: `{ id, title, source, tickers[], tags[], sentiment, published_at }`
- [ ] **R6.1.2**: 429 Too Many Requests with retry-after header

---

## Deliverable 2: Social Sentiment Radar Page

### 2.1 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `SocialSentimentRadar.jsx` | `frontend/src/pages/data-scientist/SocialSentimentRadar.jsx` | Page |
| `SentimentGauge.jsx` | `frontend/src/components/charts/SentimentGauge.jsx` | Chart |
| `PlatformBreakdown.jsx` | `frontend/src/components/charts/PlatformBreakdown.jsx` | Chart |
| `SentimentTimeSeries.jsx` | `frontend/src/components/charts/SentimentTimeSeries.jsx` | Chart |
| `TopMentionsTable.jsx` | `frontend/src/components/tables/TopMentionsTable.jsx` | Table |
| `CorrelationChart.jsx` | `frontend/src/components/charts/CorrelationChart.jsx` | Chart |

### 2.2 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/social/sentiment/{ticker}` | `get_ticker_sentiment()` |
| GET | `/api/v1/social/sentiment/top` | `get_top_sentiment_movers()` |
| GET | `/api/v1/social/platforms/{platform}/sentiment` | `get_platform_sentiment()` |
| GET | `/api/v1/social/sentiment/{ticker}/history` | `get_sentiment_history()` |
| GET | `/api/v1/social/correlation/{ticker}` | `get_sentiment_price_correlation()` |

### 2.3 End-to-End Acceptance Criteria

- [ ] **F6.2.1**: Gauge shows aggregate sentiment (-100 to +100)
- [ ] **F6.2.2**: Platform breakdown shows Twitter, Reddit, StockTwits separately
- [ ] **F6.2.3**: Time series overlays sentiment with price for correlation
- [ ] **F6.2.4**: Top mentions table shows most discussed tickers
- [ ] **F6.2.5**: Correlation chart shows historical sentiment vs price lead/lag
- [ ] **I6.2.1**: Sentiment aggregated from last 24 hours (configurable)
- [ ] **I6.2.2**: Historical data available for 90 days
- [ ] **R6.2.1**: Sentiment schema: `{ ticker, score, volume, platforms: { twitter, reddit, stocktwits } }`
- [ ] **R6.2.2**: Correlation schema: `{ correlation_coef, lead_days, significance }`

---

## Deliverable 3: Social Trading Feed Page

### 3.1 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `SocialTradingFeed.jsx` | `frontend/src/pages/hunter/SocialTradingFeed.jsx` | Page |
| `InfluencerCard.jsx` | `frontend/src/components/cards/InfluencerCard.jsx` | Card |
| `PositionFeed.jsx` | `frontend/src/components/streams/PositionFeed.jsx` | Stream |
| `TradeSignalBadge.jsx` | `frontend/src/components/badges/TradeSignalBadge.jsx` | Badge |
| `InfluencerProfilePanel.jsx` | `frontend/src/components/panels/InfluencerProfilePanel.jsx` | Panel |
| `FollowButton.jsx` | `frontend/src/components/buttons/FollowButton.jsx` | Button |

### 3.2 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/social-trading/feed` | `get_feed()` |
| GET | `/api/v1/social-trading/influencers` | `list_influencers()` |
| GET | `/api/v1/social-trading/influencers/{id}` | `get_influencer_profile()` |
| POST | `/api/v1/social-trading/influencers/{id}/follow` | `follow_influencer()` |
| GET | `/api/v1/social-trading/following` | `list_following()` |
| GET | `/api/v1/social-trading/influencers/{id}/performance` | `get_influencer_performance()` |

### 3.3 End-to-End Acceptance Criteria

- [ ] **F6.3.1**: Feed shows real-time position changes from influencers
- [ ] **F6.3.2**: Influencer card shows name, followers, win rate, avg return
- [ ] **F6.3.3**: Follow button subscribes to influencer's signals
- [ ] **F6.3.4**: Profile panel shows portfolio composition, trade history
- [ ] **F6.3.5**: Trade signal badge shows BUY/SELL with confidence
- [ ] **I6.3.1**: Feed filtered by followed influencers by default
- [ ] **I6.3.2**: Performance metrics calculated from verified trades
- [ ] **R6.3.1**: Influencer schema: `{ id, name, avatar, followers, win_rate, avg_return_pct }`
- [ ] **R6.3.2**: Position schema: `{ influencer_id, ticker, action, size, price, timestamp }`

---

## Deliverable 4: Trend Detection Widget

### 4.1 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `TrendDetectionWidget.jsx` | `frontend/src/components/widgets/TrendDetectionWidget.jsx` | Widget |
| `EmergingTopicCard.jsx` | `frontend/src/components/cards/EmergingTopicCard.jsx` | Card |
| `TrendVelocityChart.jsx` | `frontend/src/components/charts/TrendVelocityChart.jsx` | Chart |
| `TrendTickerList.jsx` | `frontend/src/components/lists/TrendTickerList.jsx` | List |

### 4.2 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/social/trends` | `get_trending_topics()` |
| GET | `/api/v1/social/trends/{topic}` | `get_topic_details()` |
| GET | `/api/v1/social/trends/tickers` | `get_trending_tickers()` |
| WS | `/ws/social/trends` | `stream_trends()` |

### 4.3 End-to-End Acceptance Criteria

- [ ] **F6.4.1**: Widget shows top 10 emerging topics with velocity
- [ ] **F6.4.2**: Velocity chart shows mention growth rate
- [ ] **F6.4.3**: Topic card shows related tickers, sample posts
- [ ] **F6.4.4**: Ticker list ranks by mention growth over 1h/4h/24h
- [ ] **F6.4.5**: Real-time updates for breaking topics
- [ ] **I6.4.1**: Topics detected from clustering algorithm
- [ ] **I6.4.2**: Velocity calculated as % change in mentions
- [ ] **R6.4.1**: Topic schema: `{ topic, velocity, mentions_1h, tickers[], sentiment }`

---

## Deliverable 5: Rumor Mill Page

### 5.1 Frontend Implementation

| Component | Path | Type |
|-----------|------|------|
| `RumorMill.jsx` | `frontend/src/pages/hunter/RumorMill.jsx` | Page |
| `RumorCard.jsx` | `frontend/src/components/cards/RumorCard.jsx` | Card |
| `VerificationStatusBadge.jsx` | `frontend/src/components/badges/VerificationStatusBadge.jsx` | Badge |
| `RumorTimeline.jsx` | `frontend/src/components/charts/RumorTimeline.jsx` | Chart |
| `RumorDetailPanel.jsx` | `frontend/src/components/panels/RumorDetailPanel.jsx` | Panel |
| `VoteButtons.jsx` | `frontend/src/components/buttons/VoteButtons.jsx` | Widget |

### 5.2 Backend Implementation

| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/news/rumors` | `list_rumors()` |
| GET | `/api/v1/news/rumors/{id}` | `get_rumor_details()` |
| POST | `/api/v1/news/rumors/{id}/vote` | `vote_on_rumor()` |
| GET | `/api/v1/news/rumors/types` | `list_rumor_types()` |
| GET | `/api/v1/news/rumors/{id}/timeline` | `get_rumor_timeline()` |

### 5.3 End-to-End Acceptance Criteria

- [ ] **F6.5.1**: Rumor cards show type (FDA, earnings, M&A), ticker, status
- [ ] **F6.5.2**: Status badge: UNVERIFIED (yellow), CONFIRMED (green), DEBUNKED (red)
- [ ] **F6.5.3**: Timeline shows rumor origin, spread, and resolution
- [ ] **F6.5.4**: Vote buttons allow users to rate rumor credibility
- [ ] **F6.5.5**: Filter by type, status, ticker, recency
- [ ] **I6.5.1**: ML classifier categorizes rumors by type
- [ ] **I6.5.2**: Votes contribute to verification confidence
- [ ] **R6.5.1**: Rumor schema: `{ id, type, ticker, status, confidence, source, votes }`
- [ ] **R6.5.2**: Vote POST requires user authentication

---

## Testing Requirements

| Test Suite | Description |
|------------|-------------|
| `test_phase6_news_e2e.py` | Feed load → filter → article detail → save search |
| `test_phase6_sentiment_e2e.py` | Ticker lookup → history → correlation |
| `test_phase6_social_trading_e2e.py` | Browse influencers → follow → view feed |
| `test_phase6_trends_e2e.py` | Widget load → topic drill-down → ticker list |
| `test_phase6_rumors_e2e.py` | List rumors → vote → verify status |

---

## Sign-Off

| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| Reviewer | | | |
| QA | | | |
| Product Owner | | | |

---

*Phase 6 Implementation Plan - Version 1.0*
