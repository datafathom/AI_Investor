# Phase 20: Reddit OAuth - Sentiment Authentication

## Phase Status: `NOT_STARTED`
**Last Updated**: 2026-01-21
**Estimated Duration**: 4-5 days
**Priority**: MEDIUM (Enhanced sentiment access)

---

## Phase Overview

Reddit OAuth integration provides authenticated API access with higher rate limits (100 req/min vs 10 req/min unauthenticated) and enables user profiling based on Reddit activity.

---

## Deliverable 20.1: Reddit OAuth Service

### Status: `NOT_STARTED`

### Backend Implementation Details
**File**: `services/auth/reddit_auth.py`

### Acceptance Criteria

| ID | Criterion | Status | Verified By | Date |
|----|-----------|--------|-------------|------|
| AC-20.1.1 | OAuth flow completes with access/refresh token exchange | `NOT_STARTED` | | |
| AC-20.1.2 | User profile (username, karma) is retrieved | `NOT_STARTED` | | |
| AC-20.1.3 | Authenticated requests use OAuth tokens | `NOT_STARTED` | | |

---

## Deliverable 20.2: Reddit Sentiment Service Enhancement

### Status: `NOT_STARTED`

### Backend Implementation Details
Modify: `services/data/reddit_service.py`

### Acceptance Criteria

| ID | Criterion | Status | Verified By | Date |
|----|-----------|--------|-------------|------|
| AC-20.2.1 | Service uses OAuth tokens when available | `NOT_STARTED` | | |
| AC-20.2.2 | Rate limits increase from 10 req/min to 100 req/min | `NOT_STARTED` | | |
| AC-20.2.3 | Fallback to unauthenticated mode on token failure | `NOT_STARTED` | | |

---

## Deliverable 20.3: Reddit User Watchlist

### Status: `NOT_STARTED`

### Frontend Implementation Details
**File**: `frontend2/src/widgets/Social/RedditWatchlist.jsx`

### Acceptance Criteria

| ID | Criterion | Status | Verified By | Date |
|----|-----------|--------|-------------|------|
| AC-20.3.1 | Users can add Reddit usernames to watchlist | `NOT_STARTED` | | |
| AC-20.3.2 | Activity from watched users triggers alerts | `NOT_STARTED` | | |
| AC-20.3.3 | Watchlist syncs across devices | `NOT_STARTED` | | |

---

## Change Log

| Date | Author | Change Description |
|------|--------|-------------------|
| 2026-01-21 | System | Initial creation of Phase 20 implementation plan |
