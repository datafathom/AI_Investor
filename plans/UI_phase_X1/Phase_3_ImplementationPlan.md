# Phase 3: Social & Sentiment Intelligence

> **Phase 8.1** | Status: `[ ]` Not Started  
> Last Updated: 2026-01-18

---

## Overview

Implements a high-density trade tape for social sentiment using the HypeMeter Engine to track "Meme Velocity" via Reddit and Twitter monitoring with FinBERT NLP analysis.

---

## 8.1: Social NLP Pipeline & HypeMeter Tape

### 8.1.1 Real-Time Scrolling Tape

**Files to Create/Modify:**
- `[NEW]` `frontend2/src/widgets/HypeMeterTape.jsx`
- `[NEW]` `frontend2/src/widgets/HypeMeterTape.css`
- `[NEW]` `frontend2/src/hooks/useSocialStream.js`

**Acceptance Criteria:**
- [ ] Real-time scrolling tape of social "trade ideas"
- [ ] Each item displays: Ticker, Sentiment Score (-1 to +1), Platform Icon, Timestamp
- [ ] Color gradient: Red (-1) → White (0) → Green (+1)
- [ ] Virtualized list for 1000+ items
- [ ] Click ticker to trigger symbol linking

**Jest Tests Required:**
- [ ] `HypeMeterTape.test.jsx`: Renders items, scroll behavior, click handler
- [ ] `useSocialStream.test.js`: WebSocket connection, message parsing

---

### 8.1.2 Viral Alert Badge

**Files to Create/Modify:**
- `[NEW]` `frontend2/src/components/ViralAlertBadge.jsx`

**Acceptance Criteria:**
- [ ] Badge appears when ticker exceeds 5 standard deviations in mention velocity
- [ ] Pulsing animation with glow effect
- [ ] Badge text: "🔥 VIRAL" or "🚀 TRENDING"
- [ ] Auto-dismiss after 30 seconds or user click

**Jest Tests Required:**
- [ ] `ViralAlertBadge.test.jsx`: Visibility toggle, animation class applies

---

### 8.1.3 NLP Keyword Extraction

**Files to Create/Modify:**
- `[MODIFY]` `frontend2/src/widgets/HypeMeterTape.jsx`

**Acceptance Criteria:**
- [ ] Extract and highlight key thematic keywords:
  - "Gamma Squeeze", "Short Interest", "Diamond Hands"
  - Political figures: "Nancy Pelosi", "Congress"
- [ ] Keywords displayed as colored chips below each item
- [ ] Filter by keyword on click

**Jest Tests Required:**
- [ ] `HypeMeterTape.test.jsx`: Keywords render, filter applies

---

### 8.1.4 HypeMeter Engine Integration

**Files to Create/Modify:**
- `[NEW]` `frontend2/src/services/hypeMeterService.js`

**Acceptance Criteria:**
- [ ] API integration with `/api/v1/social/hype-score`
- [ ] Hype Score calculation: platform-weighted engagement (views/shares)
- [ ] Score range: 0-100 displayed as progress bar
- [ ] Refresh every 30 seconds

**Jest Tests Required:**
- [ ] `hypeMeterService.test.js`: API calls, score calculation logic

---

## Backend Requirements

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/social/stream` | WS | Real-time social mention stream |
| `/api/v1/social/hype-score` | GET | Current hype scores by ticker |
| `/api/v1/social/trending` | GET | Top trending tickers |

---

## Widget Registry Entry

```javascript
{
  id: 'hype-meter-tape',
  name: 'Social HypeMeter Tape',
  component: HypeMeterTape,
  category: 'Social',
  defaultSize: { width: 400, height: 500 }
}
```

---

## Test Coverage Requirements

| Component | Unit Tests | Integration Tests |
|-----------|------------|-------------------|
| HypeMeterTape | ✓ | ✓ |
| ViralAlertBadge | ✓ | - |
| useSocialStream | ✓ | - |
| hypeMeterService | ✓ | ✓ |

**Minimum Coverage Target:** 80%

---

## Change Log

| Date | Item | Status | Notes |
|------|------|--------|-------|
| 2026-01-18 | Plan Created | Draft | Initial specification |

