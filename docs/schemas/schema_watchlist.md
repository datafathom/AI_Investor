# Schema: Watchlist

## File Location
`schemas/watchlist.py`

## Purpose
Pydantic models for user watchlists including watchlist management, watchlist items, and price alerts.

---

## Models

### Watchlist
**User-defined watchlist.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `watchlist_id` | `str` | *required* | Watchlist identifier | Primary key |
| `user_id` | `str` | *required* | Watchlist owner | Attribution |
| `watchlist_name` | `str` | *required* | Display name | Identification |
| `description` | `Optional[str]` | `None` | Watchlist description | Context |
| `symbols` | `List[str]` | `[]` | Watched symbols | Content |
| `is_default` | `bool` | `False` | Whether default list | User preference |
| `created_date` | `datetime` | *required* | Creation timestamp | Audit |
| `updated_date` | `datetime` | *required* | Last modification | Tracking |

---

### WatchlistItem
**Individual watchlist item with metadata.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `item_id` | `str` | *required* | Item identifier | Primary key |
| `watchlist_id` | `str` | *required* | Parent watchlist | Linking |
| `symbol` | `str` | *required* | Stock ticker | Identification |
| `added_date` | `datetime` | *required* | When added | Timing |
| `added_price` | `Optional[float]` | `None` | Price when added | Reference |
| `target_price` | `Optional[float]` | `None` | User price target | Alerts |
| `notes` | `Optional[str]` | `None` | User notes | Context |
| `alert_enabled` | `bool` | `False` | Whether alerts active | Alerting |

---

### PriceAlert
**Price alert configuration.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `alert_id` | `str` | *required* | Alert identifier | Primary key |
| `user_id` | `str` | *required* | Alert owner | Attribution |
| `symbol` | `str` | *required* | Stock ticker | Target |
| `alert_type` | `str` | *required* | Type: `above`, `below`, `percent_change` | Condition |
| `threshold` | `float` | *required* | Trigger value | Threshold |
| `is_active` | `bool` | `True` | Whether alert is active | Status |
| `triggered_count` | `int` | `0` | Times triggered | History |
| `last_triggered` | `Optional[datetime]` | `None` | Last trigger time | Timing |
| `created_date` | `datetime` | *required* | Creation timestamp | Audit |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `WatchlistService` | Watchlist management |
| `AlertService` | Price alert delivery |
| `MarketDataService` | Price monitoring |

## Frontend Components
- Watchlist dashboard (FrontendWatchlist)
- Watchlist manager
- Alert configuration
