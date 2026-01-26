# Phase 09: Supply Chain Security
> **Phase ID**: 09
> **Status**: Completed
> **Date**: 2026-01-19

## Overview
Secure the software supply chain by automating dependency auditing and generating a Software Bill of Materials (SBOM). This ensures we are aware of vulnerabilities in our dependency tree and maintain a clear inventory of all used packages.

## Objectives
- [ ] Add `pip-audit` to `requirements.txt`.
- [ ] Create `scripts/generate_sbom.py` to generate an SBOM (JSON format).
- [ ] Create `scripts/audit_dependencies.py` to run security scans.
- [ ] Implement `SupplyChainService` to read audit results.
- [ ] Add API endpoint `/api/v1/system/supply-chain`.
- [ ] Add "Supply Chain" status to `SystemHealthDashboard`.

## Files to Modify/Create
1.  `requirements.txt` (Add `pip-audit`)
2.  `scripts/generate_sbom.py` **[NEW]** (Wraps `pip freeze` or uses `cyclonedx-bom`)
3.  `services/system/supply_chain_service.py` **[NEW]**
4.  `web/api/wave_apis.py` (Expose status)
5.  `frontend2/src/pages/SystemHealthDashboard.jsx` (Add Widget)

## Technical Design

### Backend (`SupplyChainService`)
- Runs `pip-audit` periodically (or on startup/demand).
- Caches results to `audit_report.json`.
- Returns:
    - `vulnerabilities_found`: Integer
    - `last_scan`: Timestamp
    - `sbom_generated`: Boolean

### Frontend
- New Widget: `SupplyChainWidget`
    - Displays "Dependencies: Secure" (Green) or "Vulnerabilities Found" (Red).
    - Shows "Last Scan" time.

## Verification Plan
### Automated Tests
- `tests/system/test_supply_chain.py`:
    - Mock the audit output.
    - Verify service parses JSON correctly.

### Manual verification
- Run `python scripts/audit_dependencies.py`.
- Check Dashboard for "Secure" status.
