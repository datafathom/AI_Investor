# Persona Agents (`personas/`)

Persona agents are biased AI models that simulate specific market viewpoints. They are used in adversarial debates to challenge or support trade proposals.

## Bull Persona Agent (`bull_agent.py`)
### Description
The `BullAgent` is structurally biased toward long positions. It prioritizes momentum, growth narrative, and impulsive price action.

### Reasoning Style
- Focuses on trend continuation.
- Heavily weights "Buy the Dip" logic and breakout patterns.

---

## Bear Persona Agent (`bear_agent.py`)
### Description
The `BearAgent` is the "Skeptic." It looks for overextension, technical divergence, and macroeconomic headwinds.

### Reasoning Style
- Focuses on risk of reversal.
- Highlights daily resistance levels and overbought indicators (e.g., high RSI).
