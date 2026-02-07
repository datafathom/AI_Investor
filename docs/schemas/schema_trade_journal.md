# Schema: Trade Journal

## File Location
`schemas/trade_journal.py`

## Purpose
Pydantic models for trade journaling including trade entries, notes, emotional tracking, and performance reflection for trader development.

---

## Models

### TradeJournalEntry
**Trade journal entry for a completed trade.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `entry_id` | `str` | *required* | Entry identifier | Primary key |
| `user_id` | `str` | *required* | Trader | Attribution |
| `trade_id` | `str` | *required* | Associated trade | Trade linking |
| `symbol` | `str` | *required* | Stock ticker | Identification |
| `entry_date` | `datetime` | *required* | Trade entry date | Timing |
| `exit_date` | `Optional[datetime]` | `None` | Trade exit date | Timing |
| `entry_price` | `float` | *required* | Entry price | Execution |
| `exit_price` | `Optional[float]` | `None` | Exit price | Execution |
| `quantity` | `int` | *required* | Share quantity | Size |
| `pnl` | `Optional[float]` | `None` | Profit/loss | Performance |
| `setup_type` | `str` | *required* | Trade setup: `breakout`, `reversal`, `trend` | Pattern |
| `thesis` | `str` | *required* | Trade thesis | Rationale |
| `notes` | `Optional[str]` | `None` | Additional notes | Reflection |
| `emotion_before` | `Optional[str]` | `None` | Pre-trade emotion | Psychology |
| `emotion_after` | `Optional[str]` | `None` | Post-trade emotion | Psychology |
| `mistakes` | `List[str]` | `[]` | Identified mistakes | Learning |
| `lessons` | `List[str]` | `[]` | Lessons learned | Development |
| `rating` | `Optional[int]` | `None` | Trade execution rating (1-5) | Self-assessment |
| `created_date` | `datetime` | *required* | Entry creation | Audit |
| `updated_date` | `datetime` | *required* | Last update | Tracking |

---

### JournalStats
**Journal statistics summary.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `user_id` | `str` | *required* | Trader | Attribution |
| `total_trades` | `int` | *required* | Total journaled trades | Activity |
| `winning_trades` | `int` | *required* | Winning trade count | Performance |
| `losing_trades` | `int` | *required* | Losing trade count | Performance |
| `win_rate` | `float` | *required* | Win percentage | Quality |
| `total_pnl` | `float` | *required* | Total profit/loss | Performance |
| `average_winner` | `float` | *required* | Average winning trade | Analysis |
| `average_loser` | `float` | *required* | Average losing trade | Analysis |
| `profit_factor` | `float` | *required* | Gross profit / gross loss | Quality |
| `most_common_mistakes` | `List[str]` | `[]` | Frequent mistakes | Development |
| `best_setups` | `List[str]` | `[]` | Best performing setups | Strength |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `TradeJournalService` | Entry management |
| `JournalAnalyticsService` | Statistics |
| `TradeExecutionService` | Trade linking |

## Frontend Components
- Trade journal dashboard (FrontendJournal)
- Entry form
- Statistics dashboard
- Mistake tracker
