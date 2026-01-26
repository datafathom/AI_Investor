# Phase 02: Core Workspace Tutorials
> **Phase ID**: 02
> **Status**: Completed
> **Date**: 2026-01-19

## Overview
Implement interactive tutorials for the "Core" workspaces: **Terminal Workspace** (the main landing page) and **Mission Control**. This involves adding robust DOM selectors (IDs) to key UI elements and populating the `tutorialContent.js` registry with detailed steps.

## Objectives
- [ ] Add `data-tour-id` attributes to `TerminalWorkspace.jsx` elements (Notifications, etc.).
- [ ] Add `data-tour-id` attributes to `MissionControl.jsx` elements (Threat Level, Capital, Logs).
- [ ] Define tutorial steps in `tutorialContent.js` for:
    - `/workspace/terminal`
    - `/workspace/mission-control`
- [ ] Verify functionality in browser.

## Files to Modify
1.  `frontend2/src/pages/TerminalWorkspace.jsx`
    - Add ID to Notification Bell.
2.  `frontend2/src/pages/MissionControl.jsx`
    - Add IDs to Threat Level Panel, Capital Allocation, Live Logs, Network Map.
3.  `frontend2/src/data/tutorialContent.js`
    - Add specific content.

## Tutorial Content Draft

### Terminal Workspace (`/workspace/terminal`)
1.  **Welcome**: "This is your primary workspace. Manage windows and execute trades here."
2.  **Notifications**: "System alerts and trade confirmations appear here."
3.  **Command Palette**: "Press Ctrl+K to open the Omni-Bar for rapid navigation."

### Mission Control (`/workspace/mission-control`)
1.  **Threat Level**: "Real-time DEFCON status based on market volatility and system health."
2.  **Capital Allocation**: "Live breakdown of your portfolio across Shield (Bonds), Alpha (Equities), and Cash."
3.  **Risk Governor**: "Monitors Var (Value at Risk) and strictly enforces leverage limits."
4.  **Live Logs**: "Raw feed of every decision made by the AI Agent swarm."

## Verification Plan
### Manual Verification
1.  Navigate to `/workspace/terminal`.
2.  Verify "Ghost Cursor" targets the Notification Bell.
3.  Navigate to `/workspace/mission-control`.
4.  Verify "Ghost Cursor" visits Threat Level -> Capital -> Logs -> Risk.
