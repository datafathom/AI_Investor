# Phase 22: Emotional Feedback Loop Prevention

> **Status**: `[ ]` Not Started  
> **Last Updated**: 2026-01-25  
> **Owner**: Behavioral Finance Team

---

## 📋 Overview

**Description**: Implement behavioral locks and cooling-off periods to prevent "Internal Sepsis" and revenge trading after losses. This is the psychological firewall. If the user tries to override the system repeatedly, or inputs aggressive commands, the system detects "Tilt" and locks down.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON.txt - Phase 22

---

## 🎯 Sub-Deliverables

### 22.1 Mandatory 4-Hour Cooling-Off Timer `[ ]`

**Acceptance Criteria**: Establish a mandatory 4-hour lock on all trade entry buttons after any 3% Portfolio Freeze event.

#### Postgres Schema (Docker-compose: timescaledb service)

```sql
CREATE TABLE trading_locks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    lock_type VARCHAR(50),             -- CIRCUIT_BREAKER, TILT_DETECTED
    start_time TIMESTAMPTZ DEFAULT NOW(),
    duration_minutes INTEGER,
    
    unlock_time TIMESTAMPTZ GENERATED ALWAYS AS (start_time + (duration_minutes * INTERVAL '1 minute')) STORED,
    
    active BOOLEAN DEFAULT TRUE
);
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Migration | `migrations/22_trading_locks.sql` | `[ ]` |
| Lock Manager | `services/compliance/lock_manager.py` | `[ ]` |

---

### 22.2 Failed Override Frequency Detector `[ ]`

**Acceptance Criteria**: Disable 'Manual Override' capability when system telemetry detects high frequency of failed manual attempts (e.g., clicking "Buy" 10 times in 10 seconds while locked).

| Component | File Path | Status |
|-----------|-----------|--------|
| Spam Detector | `services/security/spam_detector.py` | `[ ]` |

---

### 22.3 Sentiment Analysis on User Logs `[ ]`

**Acceptance Criteria**: Implement a simple sentiment analysis (NLTK/VADER) on user notes/logs. Keywords like "Revenge", "Make it back", "Idiot" trigger a warning.

```python
class SentimentMonitor:
    def analyze_input(self, text: str) -> TiltScore:
        score = self.nlp.polarity_scores(text)
        if score['neg'] > 0.6:
            return TiltScore(level="HIGH", action="SUGGEST_BREAK")
        return TiltScore(level="NORMAL")
```

| Component | File Path | Status |
|-----------|-----------|--------|
| Sentiment Engine | `services/ai/sentiment_engine.py` | `[ ]` |

---

### 22.4 Behavioral Journal (Emotional Trades) `[ ]`

**Acceptance Criteria**: Log all "Prevented Emotional Trades" to a separate behavioral journal.

| Component | File Path | Status |
|-----------|-----------|--------|
| Journal Service | `services/journaling/behavioral_log.py` | `[ ]` |

---

### 22.5 React Interface "Zen Mode" Overlay `[ ]`

**Acceptance Criteria**: Frontend component that strictly overlays the trading UI with a calming interface (e.g., breathing exercise, countdown timer) when locked.

| Component | File Path | Status |
|-----------|-----------|--------|
| Zen Overlay | `frontend2/src/components/Risk/ZenOverlay.jsx` | `[ ]` |

## 📊 Phase Status: `[ ]` NOT STARTED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py behavior analyze-tilt` | Scan logs | `[ ]` |
| `python cli.py behavior lock-user <id>` | Manual lock | `[ ]` |

---

*Last verified: 2026-01-25*
