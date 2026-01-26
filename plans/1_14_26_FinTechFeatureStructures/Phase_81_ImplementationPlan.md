# Phase 81: Sentiment Analysis Engine (News/Social)

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: AI & Data Team

---

## 📋 Overview

**Description**: Ingest News (Bloomberg/Reuters) and Social (Twitter/Reddit) to gauge sentiment. "Buy the rumor, sell the news." Contrarian signals (Extreme Bullishness = Sell).

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 81

---

## 🎯 Sub-Deliverables

### 81.1 BERT Finetuned Sentiment Model `[ ]`

**Acceptance Criteria**: Deploy FinBERT (HuggingFace). Finetuned on financial text. Classify headlines as `POSITIVE`, `NEGATIVE`, `NEUTRAL`.

| Component | File Path | Status |
|-----------|-----------|--------|
| Model Service | `services/ai/finbert.py` | `[ ]` |

---

### 81.2 Twitter/X Firehose Filter `[ ]`

**Acceptance Criteria**: Ingest tweets for specific cashtags ($SPY, $TSLA). Filter out spam/bots (Phase 196 handles advanced bots, this is basic).

| Component | File Path | Status |
|-----------|-----------|--------|
| Twitter Ingest | `services/ingestion/twitter_stream.py` | `[ ]` |

---

### 81.3 Sentiment Divergence Signal `[ ]`

**Acceptance Criteria**: Signal when Price goes DOWN but Sentiment goes UP (Divergence = Bullish). Or Price UP but Sentiment DOWN.

| Component | File Path | Status |
|-----------|-----------|--------|
| Divergence | `services/strategies/sentiment_div.py` | `[ ]` |

---

### 81.4 'Fear & Greed' Index Calculator `[ ]`

**Acceptance Criteria**: Create custom Fear/Greed index. Inputs: VIX, Put/Call Ratio, Momemtum, Sentiment Score.

| Component | File Path | Status |
|-----------|-----------|--------|
| Index Calc | `services/analysis/fear_greed.py` | `[ ]` |

### 81.5 Real-Time Keyword Cloud `[ ]`

**Acceptance Criteria**: Word Cloud visualization of top trending financial terms. "Recession", "AI", "Inflation".

| Component | File Path | Status |
|-----------|-----------|--------|
| Word Cloud | `frontend2/src/components/Social/WordCloud.jsx` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py sentiment analyze <text>` | Run BERT | `[ ]` |
| `python cli.py sentiment stream <tag>` | Watch stream | `[ ]` |

---

*Last verified: 2026-01-25*
