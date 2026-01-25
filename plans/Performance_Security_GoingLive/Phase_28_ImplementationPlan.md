# Phase 28: Data Privacy Engine (GDPR/CCPA)
> **Phase ID**: 28
> **Status**: Completed
> **Date**: 2026-01-20

## Overview
Implement the core logic for user data privacy compliance, specifically addressing GDPR and CCPA requirements. This includes the 'Right to be Forgotten' (data deletion) and the 'Right to Access' (data export in JSON format).

## Objectives
- [ ] Implement `PrivacyService` to handle data lifecycle management.
- [ ] Create a **Data Export Engine** that aggregates all user-related data into a portable JSON format.
- [ ] Implement **Irreversible Data Deletion** logic across PostgreSQL and Neo4j.
- [ ] Add internal **Audit Logging** for every privacy-related request (integrated with Phase 18/24).
- [ ] Create a `PrivacyDashboard` in the frontend (User Settings) to trigger these requests.

## Files to Modify/Create
1.  `services/system/privacy_service.py` **[NEW]**
2.  `web/api/privacy_api.py` **[NEW]**
3.  `plans/Performance_Security_GoingLive/Phase_28_ImplementationPlan.md` **[NEW]**

## Technical Design
- **Export**: Queries all tables (users, portfolio, transactions, events) filtered by `user_id` and creates a single JSON blob.
- **Deidentification**: When a user is deleted, we must also purge their associations in the Neo4j graph and any cached data in Redis.

## Verification Plan
### Automated Tests
- `tests/system/test_privacy_service.py`: Verify that exporting a user's data contains their known records and that deletion actually removes them from the DB.

### Manual Verification
1. Log in as a demo user.
2. Go to Settings > Privacy.
3. Click "Export My Data" and verify the downloaded JSON.
4. Click "Delete My Account" and verify that subsequent login attempts fail and the DB record is gone.
