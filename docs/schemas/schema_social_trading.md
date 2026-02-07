# Schema: Social Trading

## File Location
`schemas/social_trading.py`

## Purpose
Pydantic models for social trading features including copy trading, leader portfolios, follower relationships, and performance leaderboards.

---

## Models

### TradeLeader
**Social trading leader profile.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `leader_id` | `str` | *required* | Leader identifier | Primary key |
| `user_id` | `str` | *required* | User account | Linking |
| `display_name` | `str` | *required* | Public name | Display |
| `avatar_url` | `Optional[str]` | `None` | Profile image | Display |
| `bio` | `Optional[str]` | `None` | Leader description | Profile |
| `strategy_description` | `str` | *required* | Trading approach | Transparency |
| `follower_count` | `int` | `0` | Number of followers | Popularity |
| `is_verified` | `bool` | `False` | Verified status | Trust |
| `created_date` | `datetime` | *required* | Profile creation | Audit |

---

### LeaderPerformance
**Leader's trading performance metrics.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `leader_id` | `str` | *required* | Leader identifier | Linking |
| `total_return` | `float` | *required* | All-time return | Performance |
| `ytd_return` | `float` | *required* | Year-to-date return | Performance |
| `win_rate` | `float` | *required* | Winning trade percentage | Quality |
| `sharpe_ratio` | `float` | *required* | Risk-adjusted return | Quality |
| `max_drawdown` | `float` | *required* | Largest drawdown | Risk |
| `trade_count` | `int` | *required* | Total trades | Activity |
| `updated_date` | `datetime` | *required* | Last updated | Freshness |

---

### CopyTrade
**Copy trading relationship.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `copy_id` | `str` | *required* | Copy relationship ID | Primary key |
| `follower_id` | `str` | *required* | Follower user | Attribution |
| `leader_id` | `str` | *required* | Copied leader | Linking |
| `allocated_amount` | `float` | *required* | Capital allocated | Sizing |
| `copy_ratio` | `float` | `1.0` | Trade size multiplier | Scaling |
| `max_trade_size` | `Optional[float]` | `None` | Per-trade limit | Risk control |
| `is_active` | `bool` | `True` | Whether active | Status |
| `created_date` | `datetime` | *required* | Start date | Timing |
| `pnl` | `float` | `0.0` | Profit/loss from copying | Performance |

---

### SocialFeed
**Social trading activity feed item.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `feed_id` | `str` | *required* | Feed item ID | Primary key |
| `leader_id` | `str` | *required* | Source leader | Attribution |
| `activity_type` | `str` | *required* | Type: `trade`, `comment`, `milestone` | Classification |
| `content` | `Dict` | *required* | Activity content | Display |
| `timestamp` | `datetime` | *required* | Activity time | Ordering |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `SocialTradingService` | Copy trading engine |
| `LeaderboardService` | Ranking system |
| `SocialFeedService` | Activity feed |

## Frontend Components
- Social trading dashboard (FrontendSocial)
- Leader profiles
- Copy trading configuration
- Activity feed
