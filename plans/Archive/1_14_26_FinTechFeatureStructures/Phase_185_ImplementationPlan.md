# Phase 185: Rule 144 Volume & Affiliate Restriction Engine

> **Status**: `[x]` Completed  
> **Last Updated**: 2026-01-30  
> **Owner**: Compliance Team

---

## 📋 Overview

**Description**: Manage Rule 144 "Dribble Out" limits for Affiliates.

**Parent Roadmap**: [ROADMAP_1_14_26.md](./ROADMAP_1_14_26.md)  
**Source**: JIRA_PLANNING_JSON_2.txt - Epoch X Phase 5

---

## 🎯 Sub-Deliverables

### 185.1 Postgres 1% Outstanding Shares Limit Table `[x]`

**Acceptance Criteria**: Track shares outstanding for limit calc.

| Component | File Path | Status |
|-----------|-----------|--------|
| Limit Calculator | `services/compliance/rule144_service.py` | `[x]` |

---

### 185.2 Kafka Trailing 4-Week Average Volume Consumer `[x]`

**Acceptance Criteria**: Volume tracking for AWTV limit.

| Component | File Path | Status |
|-----------|-----------|--------|
| Volume Consumer | `services/compliance/rule144_service.py` | `[x]` |

---

### 185.3 Neo4j Affiliate/Insider Rule 144 Node `[x]`

**Acceptance Criteria**: Affiliate flag (Control Person).

| Component | File Path | Status |
|-----------|-----------|--------|
| Affiliate Graph | `services/neo4j/affiliate_graph.py` | `[x]` |

---

### 185.4 Volume Promo Social Media Detector `[x]`

**Acceptance Criteria**: Detect solicitation / pumping.

| Component | File Path | Status |
|-----------|-----------|--------|
| Promo Monitor | `services/compliance/promo_monitor.py` | `[x]` |

---

### 185.5 IPO Lock-up Period Compliance Verifier `[x]`

**Acceptance Criteria**: Lock-up expiry tracking.

| Component | File Path | Status |
|-----------|-----------|--------|
| Lockup Verifier | `services/compliance/lockup_verifier.py` | `[x]` |

---

## 📊 Phase Status: `[x]` COMPLETED

---

## 🔧 CLI Commands

| Command | Description | Status |
|---------|-------------|--------|
| `python cli.py 144 check-limit <ticker>` | Show max sell qty | `[x]` |
| `python cli.py 144 status` | Are you an affiliate? | `[x]` |

---

*Last verified: 2026-01-30*

