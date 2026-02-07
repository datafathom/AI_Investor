# Backend Service: AI

## Overview
The **AI Service** is the core intelligence layer of the system. It abstracts multiple LLM providers (OpenAI, Anthropic, Google Gemini, Perplexity) and implements specialized financial analytical engines for sentiment analysis, market cycle classification, and executive briefing generation.

## LLM Gateway Clients
The service provides a unified interface to various state-of-the-art AI models, with built-in mock modes for development.

### OpenAI Client (`openai_client.py`)
- **Role**: Primary client for GPT-4o and embeddings.
- **Features**: Supports streaming, function calling, and token usage tracking.
- **Consumer**: `AutocoderAgent`, `CommandProcessor`.

### Anthropic Client (`anthropic_client.py`)
- **Role**: Client for Claude.
- **Features**: Specifically optimized for generating multi-persona responses in "Bull vs. Bear" debates.
- **Consumer**: `DebateChamberAgent`.

### Gemini Client (`gemini_client.py`)
- **Role**: Client for Google Gemini.
- **Features**: Focused on generating structured morning briefings and synthesizing market data.
- **Consumer**: `BriefingGenerator`.

### Perplexity Client (`perplexity_client.py`)
- **Role**: Real-time research client (Sonar models).
- **Features**: Provides citation-backed market research answers with verified news links.
- **Consumer**: `ResearchAgent`.

---

## Analytical Engines

### Business Cycle Classifier (`cycle_classifier.py`)
- **Purpose**: Classifies the current macroeconomic phase.
- **Inputs**: PMI, Yield Curve (10Y-2Y), CPI rate of change.
- **Phases**: CONTRACTION (Recession Risk), EXPANSION (Late Cycle), RECOVERY.

### Sentiment & Emotion Detection
- **Emotion Detector (`emotion_detector.py`)**: Identifies high-risk trading patterns based on keywords (e.g., "yolo", "revenge").
- **FinBERT Service (`finbert.py`)**: Uses a financial transformer model to classify headlines as Positive, Negative, or Neutral.
- **Sentiment Engine (`sentiment_engine.py`)**: Detects emotional "tilt" and irrationality in user commands.

### Executive & Strategic Intelligence
- **Master Objective Optimizer (`master_objective.py`)**: The system's ultimate utility function. Calculates **Return on Lifestyle (ROL)** and enforces survival constraints (e.g., Value at Risk < 25%).
- **Briefing Generator (`briefing_generator.py`)**: Orchestrates the assembly of daily market reports by synthesizing data through Gemini.
- **Exec Summary Service (`exec_summary.py`)**: Provides concise, voice-ready status briefings on portfolio and market status.

## Usage Examples

### Generating a Market Briefing
```python
from services.ai.briefing_generator import get_briefing_generator

generator = get_briefing_generator()
briefing = await generator.get_daily_briefing()
print(f"Market Outlook: {briefing['market_outlook']}")
```

### Checking Survival Constraints
```python
from services.ai.master_objective import MasterObjectiveOptimizer

ghost = MasterObjectiveOptimizer()
is_safe = ghost.check_survival_constraint(liquidity_ratio=0.15, value_at_risk=0.12)
if not is_safe:
    print("WARNING: Survival constraint violated!")
```
