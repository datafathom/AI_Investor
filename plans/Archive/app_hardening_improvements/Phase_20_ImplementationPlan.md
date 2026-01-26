# Phase 20: Community Forums & Discussion

## Phase Status: `NOT_STARTED` ⚠️
**Last Updated**: 2026-01-21
**Estimated Duration**: 8-12 days
**Priority**: MEDIUM (Community building)
**Started Date**: TBD
**Completion Status**: Not Started

---

## Phase Overview

Create community forums with discussion threads, expert Q&A, and knowledge sharing. This phase builds a vibrant community around the platform.

### Dependencies
- User service for user profiles
- Notification service for forum alerts
- Content moderation service
- Search service for forum content

---

## Deliverable 20.1: Forum Service

### Status: `NOT_STARTED` ⚠️

### Detailed Task Description

Build a comprehensive forum service with thread management, replies, upvoting, and moderation.

### Backend Implementation Details

**File**: `services/community/forum_service.py`

**Required Header Comment**:
```python
"""
==============================================================================
FILE: services/community/forum_service.py
ROLE: Community Forum Service
PURPOSE: Manages discussion forums with threads, replies, upvoting, and
         moderation capabilities.

INTEGRATION POINTS:
    - UserService: User profiles and authentication
    - NotificationService: Forum alerts and mentions
    - ModerationService: Content moderation
    - SearchService: Forum content search
    - ForumAPI: Forum endpoints

FEATURES:
    - Thread creation and management
    - Reply system with threading
    - Upvoting and downvoting
    - Content moderation
    - Search functionality

AUTHOR: AI Investor Team
CREATED: TBD
LAST_MODIFIED: TBD
==============================================================================
"""
```

### Acceptance Criteria

| ID | Criterion | Status | Verified By | Date |
|----|-----------|--------|-------------|------|
| AC-20.1.1 | Forum supports creation of threads with categories (General, Trading, Tax, etc.) | `NOT_STARTED` | | |
| AC-20.1.2 | Reply system supports nested replies with threading | `NOT_STARTED` | | |
| AC-20.1.3 | Upvoting/downvoting system ranks posts by popularity | `NOT_STARTED` | | |
| AC-20.1.4 | Content moderation allows flagging and removal of inappropriate content | `NOT_STARTED` | | |
| AC-20.1.5 | Search functionality allows searching threads and replies | `NOT_STARTED` | | |
| AC-20.1.6 | Forum supports rich text formatting, images, and code blocks | `NOT_STARTED` | | |
| AC-20.1.7 | Unit tests verify forum functionality | `NOT_STARTED` | | |

---

## Deliverable 20.2: Expert Q&A System

### Status: `NOT_STARTED` ⚠️

### Detailed Task Description

Build an expert Q&A system with expert verification, question routing, and answer quality scoring.

### Backend Implementation Details

**File**: `services/community/expert_qa_service.py`

### Acceptance Criteria

| ID | Criterion | Status | Verified By | Date |
|----|-----------|--------|-------------|------|
| AC-20.2.1 | Expert verification identifies verified experts (CFA, CFP, etc.) | `NOT_STARTED` | | |
| AC-20.2.2 | Question routing directs questions to appropriate experts | `NOT_STARTED` | | |
| AC-20.2.3 | Answer quality scoring ranks answers by helpfulness | `NOT_STARTED` | | |
| AC-20.2.4 | Best answer selection allows question askers to mark best answers | `NOT_STARTED` | | |

---

## Deliverable 20.3: Community Dashboard

### Status: `NOT_STARTED` ⚠️

### Detailed Task Description

Create a community dashboard with forum interface, trending topics, and user engagement metrics.

### Frontend Implementation Details

**Files**: 
- `frontend2/src/widgets/Community/ForumWidget.jsx`
- `frontend2/src/widgets/Community/ExpertQAWidget.jsx`
- `frontend2/src/widgets/Community/CommunityDashboard.jsx`

### Acceptance Criteria

| ID | Criterion | Status | Verified By | Date |
|----|-----------|--------|-------------|------|
| AC-20.3.1 | Forum interface displays threads with sorting and filtering | `NOT_STARTED` | | |
| AC-20.3.2 | Trending topics highlight popular discussions | `NOT_STARTED` | | |
| AC-20.3.3 | User engagement metrics show activity and contributions | `NOT_STARTED` | | |
| AC-20.3.4 | Dashboard is responsive and works on all device sizes | `NOT_STARTED` | | |

---

## Change Log

| Date | Author | Change Description |
|------|--------|-------------------|
| 2026-01-21 | System | Initial creation of Phase 20 implementation plan |
