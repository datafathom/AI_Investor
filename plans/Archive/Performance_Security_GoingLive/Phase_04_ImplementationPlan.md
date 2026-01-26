# Phase 04: Guardian & Architecture Tutorials
> **Phase ID**: 04
> **Status**: Completed
> **Date**: 2026-01-19

## Overview
Implement interactive tutorials for the **Guardian** (Compliance, Margin) and **Architect** (System Health) workspaces. This completes the "Educational Overlay" phase group. The process mirrors previous phases: adding `data-tour-id` attributes to React components and defining the tutorial steps in the registry.

## Objectives
- [ ] Add `data-tour-id` to `ComplianceDashboard.jsx` (KYC, Vault, Filing).
- [ ] Add `data-tour-id` to `SystemHealthDashboard.jsx` (Kafka, Database, Load Balancer).
- [ ] Add `data-tour-id` to `MarginDashboard.jsx` (Danger Zone, Collateral, Liquidation).
- [ ] Update `tutorialContent.js` with steps for:
    - `/guardian/compliance`
    - `/guardian/margin`
    - `/architect/system`
- [ ] Verify functionality via Browser and capture screenshots.

## Files to Modify
1.  `frontend2/src/pages/ComplianceDashboard.jsx`
2.  `frontend2/src/pages/SystemHealthDashboard.jsx`
3.  `frontend2/src/pages/MarginDashboard.jsx`
4.  `frontend2/src/data/tutorialContent.js`

## Tutorial Content Draft

### Compliance Dashboard (`/guardian/compliance`)
1.  **KYC Portal**: "Identity verification center for institutional clients."
2.  **Document Vault**: "Secure, immutable storage for all regulatory filings and audit trails."
3.  **Filing Tracker**: "Real-time status of SEC Forms 13F, 10-K, and other mandatory disclosures."

### System Health (`/architect/system`)
1.  **Kafka Streams**: "Monitor the throughput of high-frequency market data ingestion pipelines."
2.  **Database Telemetry**: "Real-time metrics for TimescaleDB (Time-series) and Neo4j (Graph) clusters."
3.  **Agent Load Balancer**: "Distribution of computational tasks across the AI swarm nodes."

### Margin Dashboard (`/guardian/margin`)
1.  **Danger Zone**: "Critical alerts for positions approaching liquidation thresholds."
2.  **Collateral Priority**: "Visual hierarchy of assets available for margin calls."
3.  **Liquidation Editor**: "Configure the specific logic for forced liquidations in extreme volatility."

## Verification Plan
1.  Navigate to `/guardian/compliance` -> Verify tutorial.
2.  Navigate to `/architect/system` -> Verify tutorial.
3.  Navigate to `/guardian/margin` -> Verify tutorial.
