# Schema: Marketplace

## File Location
`schemas/marketplace.py`

## Purpose
Pydantic models for the extension marketplace supporting custom plugins, strategy templates, and third-party integrations through a modular extension system.

---

## Enums

### ExtensionStatus
**Extension approval status.**

| Value | Description |
|-------|-------------|
| `PENDING` | Awaiting review |
| `APPROVED` | Approved for distribution |
| `REJECTED` | Failed review |
| `DEPRECATED` | No longer supported |

---

## Models

### Extension
**Marketplace extension/plugin.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `extension_id` | `str` | *required* | Unique extension ID | Primary key |
| `developer_id` | `str` | *required* | Extension creator | Attribution |
| `name` | `str` | *required* | Extension name | Display |
| `description` | `str` | *required* | Full description | Marketing |
| `category` | `str` | *required* | Category: `strategy`, `analysis`, `integration` | Classification |
| `version` | `str` | *required* | Current version | Version control |
| `status` | `ExtensionStatus` | `PENDING` | Approval status | Workflow |
| `price` | `float` | `0.0` | Price in dollars (0 = free) | Monetization |
| `downloads` | `int` | `0` | Download count | Popularity |
| `rating` | `float` | `0.0` | Average rating (0-5) | Quality indicator |
| `created_date` | `datetime` | *required* | Creation timestamp | Audit |
| `updated_date` | `datetime` | *required* | Last update | Freshness |

---

### ExtensionReview
**User review of an extension.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `review_id` | `str` | *required* | Unique review ID | Primary key |
| `extension_id` | `str` | *required* | Reviewed extension | Linking |
| `user_id` | `str` | *required* | Reviewer | Attribution |
| `rating` | `int` | *required, 1-5* | Star rating | Rating aggregation |
| `title` | `Optional[str]` | `None` | Review title | Display |
| `content` | `Optional[str]` | `None` | Review text | Feedback |
| `created_date` | `datetime` | *required* | Review timestamp | Ordering |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `MarketplaceService` | Extension management |
| `ExtensionReviewService` | Review management |
| `DeveloperService` | Developer portal |

## Frontend Components
- Marketplace dashboard (FrontendMarketplace)
- Extension catalog
- Developer submission portal
