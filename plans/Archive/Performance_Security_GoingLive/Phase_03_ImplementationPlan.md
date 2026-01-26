# Phase 03: Analyst & Strategist Tutorials
> **Phase ID**: 03
> **Status**: Completed
> **Date**: 2026-01-19

## Overview
Implement interactive tutorials for the **Analyst** (Backtesting) and **Strategist** (Estate & Corporate) workspaces. This involves adding `data-tour-id` attributes to `BacktestPortfolio.jsx` and `CorporateDashboard.jsx` (Estate was partially done, but will be standardized). Then, populate `tutorialContent.js` with specific guides for these complex financial modules.

## Objectives
- [ ] Add `data-tour-id` to `BacktestPortfolio.jsx` (Monte Carlo, Overfit, Drawdown).
- [ ] Add `data-tour-id` to `CorporateDashboard.jsx` (Calendar, DRIP, Corporate Actions).
- [ ] Refine `EstateDashboard.jsx` (if needed) and ensure `tutorialContent.js` follows the new standard.
- [ ] Update `tutorialContent.js` with steps for:
    - `/analyst/backtest`
    - `/strategist/corporate`
    - `/strategist/estate` (Refine existing)
- [ ] Verify via Browser.

## Files to Modify
1.  `frontend2/src/pages/BacktestPortfolio.jsx`
2.  `frontend2/src/pages/CorporateDashboard.jsx`
3.  `frontend2/src/data/tutorialContent.js`

## Tutorial Content Draft

### Backtest Portfolio (`/analyst/backtest`)
1.  **Monte Carlo**: "Simulates 10,000 parallel market realities to stress-test your strategy."
2.  **Overfit Warning**: "Detects if your strategy is 'memorizing' past data rather than learning patterns."
3.  **Drawdown Timeline**: "Visualizes the deepest historical losses to help you gauge risk tolerance."

### Corporate Dashboard (`/strategist/corporate`)
1.  **Earnings Calendar**: "Track upcoming earnings reports for portfolio companies."
2.  **DRIP Console**: "Manage Dividend Reinvestment Plans to compound returns automatically."
3.  **Corporate Actions**: "Vote on proxies, handle splits, and manage tender offers."

## Verification Plan
1.  Navigate to `/analyst/backtest`.
2.  Verify Ghost Cursor visits all 3 widgets.
3.  Navigate to `/strategist/corporate`.
4.  Verify Ghost Cursor visits all 3 widgets.
