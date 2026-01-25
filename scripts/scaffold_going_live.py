
import os

base_dir = r"c:\Users\astir\Desktop\AI_Company\AI_Investor\plans\Performance_Security_GoingLive"
if not os.path.exists(base_dir):
    os.makedirs(base_dir)

phases = [
    (1, "Education Mode Engine"),
    (2, "Core Workspace Tutorials"),
    (3, "Analyst & Strategist Tutorials"),
    (4, "Guardian & Architecture Tutorials"),
    (5, "Secrets Management & Vault Integration"),
    (6, "Advanced Authentication (MFA/YubiKey)"),
    (7, "API Security Gateway & WAF"),
    (8, "RBAC Enforcement Middleware"),
    (9, "Supply Chain Security & SBOM"),
    (10, "Banking Connectivity (Plaid Link)"),
    (11, "Transaction Reconciliation Engine"),
    (12, "Brokerage OAuth & Market Data"),
    (13, "Live Order Execution Router"),
    (14, "Payment Gateway Integration"),
    (15, "Real-Chain Crypto Wallet Connectivity"),
    (16, "Multi-Currency Settlement System"),
    (17, "Redis Caching Layer"),
    (18, "Database Optimization (TimescaleDB)"),
    (19, "Frontend Performance Optimization"),
    (20, "CDN & Static Asset Distribution"),
    (21, "WebSocket Horizontal Scaling"),
    (22, "Load Testing & Capacity Planning"),
    (23, "Distributed Tracing (OpenTelemetry)"),
    (24, "Centralized Logging (ELK/Loki)"),
    (25, "Advanced Metric Alerting"),
    (26, "Chaos Engineering Resilience"),
    (27, "Disaster Recovery & Backup Drills"),
    (28, "Data Privacy Engine (GDPR/CCPA)"),
    (29, "Immutable Audit Trail"),
    (30, "Legal Automation & TOS"),
    (31, "Staging Environment & CICD"),
    (32, "Blue/Green Deployment Infrastructure"),
    (33, "Production Capture & Go-Live")
]

template = """# Phase {phase_id:02d}: {title}
> **Phase ID**: {phase_id:02d}
> **Status**: Planning
> **Date**: 2026-01-19

## Overview
Detailed plan for **{title}**. This phase focuses on moving the AI Investor platform towards production readiness.

## Objectives
- [ ] Define specific requirements for {title}
- [ ] Architecture design for {title} component
- [ ] Implementation of core logic
- [ ] Integration with existing systems

## Files to Create/Modify
- [ ] `TBD`

## Verification Plan
### Automated Tests
- [ ] Unit tests for new components
- [ ] Integration tests

### Manual Verification
- [ ] Step 1: ...
"""

for pid, title in phases:
    # Skip Phase 1 as we manually created a detailed one
    if pid == 1:
        continue
        
    filename = f"Phase_{pid:02d}_ImplementationPlan.md"
    filepath = os.path.join(base_dir, filename)
    
    # Don't overwrite if exists (preserves manual edits)
    if not os.path.exists(filepath):
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(template.format(phase_id=pid, title=title))
        print(f"Created {filename}")
    else:
        print(f"Skipped {filename} (already exists)")
