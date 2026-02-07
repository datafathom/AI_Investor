# Schema: Community

## File Location
`schemas/community.py`

## Purpose
Pydantic models for community forums, discussion threads, replies, and expert Q&A systems. Enables user engagement through discussion forums, knowledge sharing, and expert consultations.

---

## Enums

### ThreadCategory
**Forum thread categories.**

| Value | Description |
|-------|-------------|
| `GENERAL` | General financial discussions |
| `TRADING` | Trading strategies and ideas |
| `TAX` | Tax-related questions |
| `RETIREMENT` | Retirement planning discussions |
| `CRYPTO` | Cryptocurrency discussions |
| `OPTIONS` | Options trading |
| `EDUCATION` | Learning and tutorials |

---

## Models

### ForumThread
**A discussion thread in the community forum.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `thread_id` | `str` | *required* | Unique thread identifier | Primary key |
| `user_id` | `str` | *required* | Thread creator | Attribution |
| `category` | `ThreadCategory` | *required* | Topic category | Filtering, organization |
| `title` | `str` | *required* | Thread title | Display, search |
| `content` | `str` | *required* | Initial post content | Thread body |
| `upvotes` | `int` | `0` | Positive votes | Ranking |
| `downvotes` | `int` | `0` | Negative votes | Quality filtering |
| `reply_count` | `int` | `0` | Number of replies | Engagement metric |
| `views` | `int` | `0` | View count | Popularity |
| `is_pinned` | `bool` | `False` | Whether pinned to top | Moderation |
| `is_locked` | `bool` | `False` | Whether new replies allowed | Moderation |
| `created_date` | `datetime` | *required* | Creation timestamp | Ordering |
| `updated_date` | `datetime` | *required* | Last modification | Activity tracking |
| `last_reply_date` | `Optional[datetime]` | `None` | Most recent reply time | Sorting by activity |

---

### ThreadReply
**A reply to a forum thread.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `reply_id` | `str` | *required* | Unique reply identifier | Primary key |
| `thread_id` | `str` | *required* | Parent thread | Links reply to thread |
| `user_id` | `str` | *required* | Reply author | Attribution |
| `content` | `str` | *required* | Reply content | Display |
| `parent_reply_id` | `Optional[str]` | `None` | Parent reply for nesting | Threaded replies |
| `upvotes` | `int` | `0` | Positive votes | Quality ranking |
| `downvotes` | `int` | `0` | Negative votes | Quality filtering |
| `is_best_answer` | `bool` | `False` | Marked as best answer | Expert answer designation |
| `created_date` | `datetime` | *required* | Creation timestamp | Ordering |
| `updated_date` | `datetime` | *required* | Last edit time | Change tracking |

---

### ExpertQuestion
**Question submitted to expert Q&A system.**

| Field | Type | Default | Description | Usage |
|-------|------|---------|-------------|-------|
| `question_id` | `str` | *required* | Unique question identifier | Primary key |
| `user_id` | `str` | *required* | Question asker | Attribution |
| `title` | `str` | *required* | Question title | Display, search |
| `content` | `str` | *required* | Detailed question | Expert review |
| `category` | `str` | *required* | Topic category | Expert routing |
| `expert_id` | `Optional[str]` | `None` | Assigned expert | Expert assignment |
| `best_answer_id` | `Optional[str]` | `None` | Selected best answer | Answer designation |
| `answer_count` | `int` | `0` | Number of answers | Engagement |
| `status` | `str` | `"open"` | Status: `open`, `answered`, `closed` | Workflow state |
| `created_date` | `datetime` | *required* | Creation timestamp | Ordering |
| `updated_date` | `datetime` | *required* | Last activity | Freshness |

---

## Integration Points

| Service | Usage |
|---------|-------|
| `ForumService` | Thread management |
| `ExpertQAService` | Expert question routing |
| `ModerationService` | Content moderation |
| `NotificationService` | Reply notifications |

## Frontend Components
- Forum thread list (FrontendCommunity)
- Thread view with replies
- Expert Q&A submission form
- User reputation display
