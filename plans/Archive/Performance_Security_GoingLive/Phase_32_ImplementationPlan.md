# Phase 32: Blue/Green Deployment Infrastructure
> **Phase ID**: 32
> **Status**: Planning
> **Date**: 2026-01-20

## Overview
Implement a Blue/Green deployment strategy to achieve zero-downtime releases. This involves maintaining two identical production-like environments (Blue and Green) and using a load balancer to switch traffic between them after verifying the new version.

## Objectives
- [ ] Implement **Nginx Upstream Configuration** with `blue` and `green` targets.
- [ ] Create a **Deployment Swap Script** (`scripts/ops/swap_deploy.py`) that updates Nginx configuration to point to the active environment.
- [ ] Implement a **Pre-Flight Health Check** that ensures the "idle" environment is healthy before switching traffic.
- [ ] Add **Audit Logging** for deployment events.

## Files to Modify/Create
1.  `infra/nginx/blue_green.conf` **[NEW]**
2.  `scripts/ops/swap_deploy.py` **[NEW]**
3.  `plans/Performance_Security_GoingLive/Phase_32_ImplementationPlan.md` **[NEW]**

## Technical Design
- **Nginx**: Uses a `symlink` for the active upstream configuration. The swap script updates the symlink and reloads Nginx.
- **Failback**: If the new environment fails the health check post-swap (but before full commitment), the script can automatically revert.

## Verification Plan
### Automated Tests
- `tests/ops/test_swap_logic.py`: Verifies that the swap script correctly identifies the idle environment and updates the configuration.

### Manual Verification
1. Deploy v1 to Blue.
2. Deploy v2 to Green.
3. Run `python scripts/ops/swap_deploy.py --target green`.
4. Verify that traffic now reaches the Green environment without dropping connections.
