# Script: full_system_audit.py

## Overview
`full_system_audit.py` is a deep-level technical audit that verifies the structural integrity of the application's database and knowledge graph.

## Core Functionality
- **Postgres Trigger Audit**: Scans the relational database schema to identify high trigger density and potential circular logic loops that could cause performance degradation or data corruption.
- **Neo4j Integrity Check**:
  - Orphan Discovery: Identifies nodes in the graph that have no relationships.
  - Client-Portfolio Gap: Specifically checks for Clients who lack an associated Financial Plan or Portfolio, highlighting potential data ingestion failures.
- **System Health Report**: Provides an overall status of "OPERATIONAL" or "DEGRADED" based on the severity of the findings.

## Status
**Essential (Data Integrity)**: Critical for maintaining the long-term health of the complex relational-graph hybrid data model.
