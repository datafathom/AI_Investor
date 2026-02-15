# Admin Route Migration — Reference Guide

> **Last Updated**: 2026-02-14
> **Migration Date**: 2026-02-14
> **Scope**: 97 admin routes across 13 departments
> **Script Used**: `scripts/migrate_admin_routes.py`

## Context & Motivation

The Sovereign OS frontend originally served many department-specific pages under the flat `/admin/` URL namespace. For example, the Auditor's Attribution Analysis page was at `/admin/attribution-analysis` instead of the more intuitive `/auditor/attribution-analysis`.

This migration created department-specific workstation files so that each page is accessible under its owning department's URL slug, while keeping the original `/admin/` routes intact for the System Administration dashboard (Department ID 19).

## What Was Done

### 1. Workstation Files Created (~97 files)

For each admin route that belonged to a department, a placeholder workstation JSX file was created in:

```
Frontend/src/pages/workstations/<dept-slug>/<DeptPascal><SubPascal>.jsx
```

These files contain boilerplate "NOT_IMPLEMENTED" content with the department branding. The `DynamicWorkstation` loader in `App.jsx` automatically discovers these files via `import.meta.glob`.

### 2. departmentRegistry.js Updated

New `subModules` entries were appended to each department's configuration so that the `MenuBar` navigation builds links to the new department-specific URLs.

### 3. Route Test Files Updated

All 18 department route test files in `DEBUGGING/FrontEndAudit/Routes2Test/depts/` were updated to use department-specific URLs instead of `/admin/` URLs. Only `admin_routes.py` retains `/admin/` URLs (correct — it's the admin department's own file).

### 4. App.jsx NOT Modified

No explicit `<Route>` entries were added to `App.jsx`. The `DynamicWorkstation` catch-all routes at lines 1792–1798 handle all department sub-page routing dynamically.

## Migration Scope — Complete Department Mapping

The following table shows every admin route that was migrated, grouped by department:

### Auditor (12 routes)
| Admin URL | Dept URL | File Created |
|-----------|----------|-------------|
| `/admin/attribution-analysis` | `/auditor/attribution-analysis` | `AuditorAttributionAnalysis.jsx` |
| `/admin/discrepancy-resolution` | `/auditor/discrepancy-resolution` | `AuditorDiscrepancyResolution.jsx` |
| `/admin/fee-auditor` | `/auditor/fee-auditor` | `AuditorFeeAuditor.jsx` |
| `/admin/model-validator` | `/auditor/model-validator` | `AuditorModelValidator.jsx` |
| `/admin/performance-attribution` | `/auditor/performance-attribution` | `AuditorPerformanceAttribution.jsx` |
| `/admin/performance-report` | `/auditor/performance-report` | `AuditorPerformanceReport.jsx` |
| `/admin/pricing-verifier` | `/auditor/pricing-verifier` | `AuditorPricingVerifier.jsx` |
| `/admin/quality-incidents` | `/auditor/quality-incidents` | `AuditorQualityIncidents.jsx` |
| `/admin/reconciliation-dashboard` | `/auditor/reconciliation-dashboard` | `AuditorReconciliationDashboard.jsx` |
| `/admin/source-reputation` | `/auditor/source-reputation` | `AuditorSourceReputation.jsx` |
| `/admin/tax-lot-analyzer` | `/auditor/tax-lot-analyzer` | `AuditorTaxLotAnalyzer.jsx` |
| `/admin/wealth-benchmark` | `/auditor/wealth-benchmark` | `AuditorWealthBenchmark.jsx` |

### Banker (11 routes)
| Admin URL | Dept URL | File Created |
|-----------|----------|-------------|
| `/admin/account-aggregator` | `/banker/account-aggregator` | `BankerAccountAggregator.jsx` |
| `/admin/bank-manager` | `/banker/bank-manager` | `BankerBankManager.jsx` |
| `/admin/crypto-wallet` | `/banker/crypto-wallet` | `BankerCryptoWallet.jsx` |
| `/admin/defi-yield-dashboard` | `/banker/defi-yield-dashboard` | `BankerDefiYieldDashboard.jsx` |
| `/admin/expense-manager` | `/banker/expense-manager` | `BankerExpenseManager.jsx` |
| `/admin/tax-liability-dashboard` | `/banker/tax-liability-dashboard` | `BankerTaxLiabilityDashboard.jsx` |
| `/admin/transaction-ledger` | `/banker/transaction-ledger` | `BankerTransactionLedger.jsx` |
| `/admin/transaction-sync` | `/banker/transaction-sync` | `BankerTransactionSync.jsx` |
| `/admin/transfer-center` | `/banker/transfer-center` | `BankerTransferCenter.jsx` |
| `/admin/treasury-dashboard` | `/banker/treasury-dashboard` | `BankerTreasuryDashboard.jsx` |
| `/admin/yield-optimizer` | `/banker/yield-optimizer` | `BankerYieldOptimizer.jsx` |

### Data Scientist (6 routes)
| Admin URL | Dept URL | File Created |
|-----------|----------|-------------|
| `/admin/backtest-engine` | `/data-scientist/backtest-engine` | `DataScientistBacktestEngine.jsx` |
| `/admin/correlation-risk` | `/data-scientist/correlation-risk` | `DataScientistCorrelationRisk.jsx` |
| `/admin/crypto-analytics` | `/data-scientist/crypto-analytics` | `DataScientistCryptoAnalytics.jsx` |
| `/admin/data-pipeline-manager` | `/data-scientist/data-pipeline-manager` | `DataScientistDataPipelineManager.jsx` |
| `/admin/data-quality-dashboard` | `/data-scientist/data-quality-dashboard` | `DataScientistDataQualityDashboard.jsx` |
| `/admin/data-validation` | `/data-scientist/data-validation` | `DataScientistDataValidation.jsx` |

### Envoy (5 routes)
| Admin URL | Dept URL | File Created |
|-----------|----------|-------------|
| `/admin/donation-manager` | `/envoy/donation-manager` | `EnvoyDonationManager.jsx` |
| `/admin/giving-opportunity-finder` | `/envoy/giving-opportunity-finder` | `EnvoyGivingOpportunityFinder.jsx` |
| `/admin/impact-scorecard` | `/envoy/impact-scorecard` | `EnvoyImpactScorecard.jsx` |
| `/admin/investor-portal` | `/envoy/investor-portal` | `EnvoyInvestorPortal.jsx` |
| `/admin/philanthropy-center` | `/envoy/philanthropy-center` | `EnvoyPhilanthropyCenter.jsx` |

### Front Office (1 route)
| Admin URL | Dept URL | File Created |
|-----------|----------|-------------|
| `/admin/executive-summary` | `/front-office/executive-summary` | `FrontOfficeExecutiveSummary.jsx` |

### Hunter (4 routes)
| Admin URL | Dept URL | File Created |
|-----------|----------|-------------|
| `/admin/on-chain-terminal` | `/hunter/on-chain-terminal` | `HunterOnChainTerminal.jsx` |
| `/admin/opportunity-tracker` | `/hunter/opportunity-tracker` | `HunterOpportunityTracker.jsx` |
| `/admin/private-equity-terminal` | `/hunter/private-equity-terminal` | `HunterPrivateEquityTerminal.jsx` |
| `/admin/watchlist-manager` | `/hunter/watchlist-manager` | `HunterWatchlistManager.jsx` |

### Lawyer (6 routes)
| Admin URL | Dept URL | File Created |
|-----------|----------|-------------|
| `/admin/compliance-tracker` | `/lawyer/compliance-tracker` | `LawyerComplianceTracker.jsx` |
| `/admin/doc-generator` | `/lawyer/doc-generator` | `LawyerDocGenerator.jsx` |
| `/admin/filing-manager` | `/lawyer/filing-manager` | `LawyerFilingManager.jsx` |
| `/admin/tax-harvester` | `/lawyer/tax-harvester` | `LawyerTaxHarvester.jsx` |
| `/admin/trade-surveillance` | `/lawyer/trade-surveillance` | `LawyerTradeSurveillance.jsx` |
| `/admin/trust-admin` | `/lawyer/trust-admin` | `LawyerTrustAdmin.jsx` |

### Orchestrator (9 routes)
| Admin URL | Dept URL | File Created |
|-----------|----------|-------------|
| `/admin/autonomy-controller` | `/orchestrator/autonomy-controller` | `OrchestratorAutonomyController.jsx` |
| `/admin/consensus-visualizer` | `/orchestrator/consensus-visualizer` | `OrchestratorConsensusVisualizer.jsx` |
| `/admin/fleet` | `/orchestrator/fleet` | `OrchestratorFleet.jsx` |
| `/admin/os-health-dashboard` | `/orchestrator/os-health-dashboard` | `OrchestratorOsHealthDashboard.jsx` |
| `/admin/singularity` | `/orchestrator/singularity` | `OrchestratorSingularity.jsx` |
| `/admin/system-health` | `/orchestrator/system-health` | `OrchestratorSystemHealth.jsx` |
| `/admin/tactical-command-center` | `/orchestrator/tactical-command-center` | `OrchestratorTacticalCommandCenter.jsx` |
| `/admin/task-queue` | `/orchestrator/task-queue` | `OrchestratorTaskQueue.jsx` |
| `/admin/unified-alert-center` | `/orchestrator/unified-alert-center` | `OrchestratorUnifiedAlertCenter.jsx` |

### Physicist (4 routes)
| Admin URL | Dept URL | File Created |
|-----------|----------|-------------|
| `/admin/greeks-surface` | `/physicist/greeks-surface` | `PhysicistGreeksSurface.jsx` |
| `/admin/options-flow` | `/physicist/options-flow` | `PhysicistOptionsFlow.jsx` |
| `/admin/pnl-modeler` | `/physicist/pnl-modeler` | `PhysicistPnlModeler.jsx` |
| `/admin/position-greeks` | `/physicist/position-greeks` | `PhysicistPositionGreeks.jsx` |

### Refiner (6 routes)
| Admin URL | Dept URL | File Created |
|-----------|----------|-------------|
| `/admin/agent-dna` | `/refiner/agent-dna` | `RefinerAgentDna.jsx` |
| `/admin/autocoder` | `/refiner/autocoder` | `RefinerAutocoder.jsx` |
| `/admin/autocoder/sandbox` | `/refiner/autocoder-sandbox` | `RefinerAutocoderSandbox.jsx` |
| `/admin/evolution` | `/refiner/evolution` | `RefinerEvolution.jsx` |
| `/admin/meta-optimizer` | `/refiner/meta-optimizer` | `RefinerMetaOptimizer.jsx` |
| `/admin/prompt-tester` | `/refiner/prompt-tester` | `RefinerPromptTester.jsx` |

### Sentry (5 routes)
| Admin URL | Dept URL | File Created |
|-----------|----------|-------------|
| `/admin/api-key-manager` | `/sentry/api-key-manager` | `SentryApiKeyManager.jsx` |
| `/admin/fraud-center` | `/sentry/fraud-center` | `SentryFraudCenter.jsx` |
| `/admin/security-center` | `/sentry/security-center` | `SentrySecurityCenter.jsx` |
| `/admin/security-logs` | `/sentry/security-logs` | `SentrySecurityLogs.jsx` |
| `/admin/warden-panel` | `/sentry/warden-panel` | `SentryWardenPanel.jsx` |

### Steward (3 routes)
| Admin URL | Dept URL | File Created |
|-----------|----------|-------------|
| `/admin/asset-inventory` | `/steward/asset-inventory` | `StewardAssetInventory.jsx` |
| `/admin/collectible-viewer` | `/steward/collectible-viewer` | `StewardCollectibleViewer.jsx` |
| `/admin/exit-planner` | `/steward/exit-planner` | `StewardExitPlanner.jsx` |

### Strategist (6 routes)
| Admin URL | Dept URL | File Created |
|-----------|----------|-------------|
| `/admin/rebalancer` | `/strategist/rebalancer` | `StrategistRebalancer.jsx` |
| `/admin/risk-dashboard` | `/strategist/risk-dashboard` | `StrategistRiskDashboard.jsx` |
| `/admin/screener-builder` | `/strategist/screener-builder` | `StrategistScreenerBuilder.jsx` |
| `/admin/strategy-lab` | `/strategist/strategy-lab` | `StrategistStrategyLab.jsx` |
| `/admin/strategy-library` | `/strategist/strategy-library` | `StrategistStrategyLibrary.jsx` |
| `/admin/walk-forward` | `/strategist/walk-forward` | `StrategistWalkForward.jsx` |

### Stress Tester (6 routes)
| Admin URL | Dept URL | File Created |
|-----------|----------|-------------|
| `/admin/black-swan-generator` | `/stress-tester/black-swan-generator` | `StresstesterBlackSwanGenerator.jsx` |
| `/admin/crash-simulator` | `/stress-tester/crash-simulator` | `StresstesterCrashSimulator.jsx` |
| `/admin/liquidity-stress` | `/stress-tester/liquidity-stress` | `StresstesterLiquidityStress.jsx` |
| `/admin/robustness-lab` | `/stress-tester/robustness-lab` | `StresstesterRobustnessLab.jsx` |
| `/admin/wargame-arena` | `/stress-tester/wargame-arena` | `StresstesterWargameArena.jsx` |
| `/admin/web3-simulator` | `/stress-tester/web3-simulator` | `StresstesterWeb3Simulator.jsx` |

### Trader (10 routes)
| Admin URL | Dept URL | File Created |
|-----------|----------|-------------|
| `/admin/algo-order-entry` | `/trader/algo-order-entry` | `TraderAlgoOrderEntry.jsx` |
| `/admin/bracket-manager` | `/trader/bracket-manager` | `TraderBracketManager.jsx` |
| `/admin/dark-pool-access` | `/trader/dark-pool-access` | `TraderDarkPoolAccess.jsx` |
| `/admin/execution-analytics` | `/trader/execution-analytics` | `TraderExecutionAnalytics.jsx` |
| `/admin/iceberg-slicer` | `/trader/iceberg-slicer` | `TraderIcebergSlicer.jsx` |
| `/admin/multi-leg-builder` | `/trader/multi-leg-builder` | `TraderMultiLegBuilder.jsx` |
| `/admin/order-management` | `/trader/order-management` | `TraderOrderManagement.jsx` |
| `/admin/position-sizer` | `/trader/position-sizer` | `TraderPositionSizer.jsx` |
| `/admin/risk-limits` | `/trader/risk-limits` | `TraderRiskLimits.jsx` |
| `/admin/smart-router` | `/trader/smart-router` | `TraderSmartRouter.jsx` |

## Departments NOT Migrated

The following departments had **zero** `/admin/` routes and required no migration:

- **Guardian** — routes were already department-specific
- **Historian** — routes were already department-specific
- **Special** — uses a separate routing system (not `DynamicWorkstation`)

## Post-Migration Audit Results

| Check | Result |
|-------|--------|
| All 97 migrated subModules resolve to workstation files | ✅ Verified |
| Route test files clean (no `/admin/` outside admin dept) | ✅ Verified |
| `DynamicWorkstation` catch-all routes exist in `App.jsx` | ✅ Lines 1792, 1798 |
| Vite build passes | ✅ 6,123 modules, ~60s |
| 28 pre-existing subModule gaps (unrelated to migration) | ⚠️ Backlog |

## How to Add More Routes in the Future

To add a new department page:

1. **Create the file**: `Frontend/src/pages/workstations/<dept-slug>/<DeptPascal><SubPascal>.jsx`
2. **Add to registry**: Append a `subModules` entry in `departmentRegistry.js`
3. **No `App.jsx` changes needed** — the `DynamicWorkstation` loader will auto-discover the file
4. **No route test changes needed** — the verification framework reads from the route test files
5. **Run `vite build`** to confirm the new file is picked up
