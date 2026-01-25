# Phase 30: Legal Automation
> **Phase ID**: 30
> **Status**: Planning
> **Date**: 2026-01-20

## Overview
Implement automated tracking of legal agreements, including Terms of Service (TOS) and Liability Disclaimers. Ensure that users cannot access specific high-risk features (e.g., Options Trading) without explicitly accepting the relevant disclaimer versions.

## Objectives
- [ ] Implement `LegalComplianceService` to manage agreement versions and user acceptances.
- [ ] Create API endpoints for fetching and accepting legal documents.
- [ ] Add `TOS_ACCEPTED` flag to User Profile.
- [ ] Enforce **Disclaimer Gating** for high-risk trading features.
- [ ] Create `LegalAgreementWidget` for the frontend.

## Files to Modify/Create
1.  `services/system/legal_compliance_service.py` **[NEW]**
2.  `web/api/legal_api.py` **[NEW]**
3.  `plans/Performance_Security_GoingLive/Phase_30_ImplementationPlan.md` **[NEW]**

## Technical Design
- **Versioning**: Each legal document has a version (e.g., "v1.0", "v1.2"). If the system upgrades the required version, all users must re-accept.
- **Micro-Disclaimers**: Specific actions (like "Enable Margin") trigger disjoint legal acceptances stored separately.

## Verification Plan
### Automated Tests
- `tests/system/test_legal_compliance.py`: Verify that a user cannot perform an action if they haven't accepted the latest TOS version.

### Manual Verification
1. Attempt to access the "Trading" page. Verify it redirects to a TOS acceptance modal.
2. Accept the TOS.
3. Verify access is now granted.
