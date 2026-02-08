# Phase 24 Implementation Plan: Banking & Treasury Management

> **Phase**: 24 of 33 | **Status**: 🔴 Not Started | **Priority**: HIGH  
> **Duration**: 5 days | **Dependencies**: Phase 22, Phase 16

---

## Services Covered
| Service | Primary Files |
|---------|---------------|
| `banking` | `cash_manager.py`, `bank_connector.py` |
| `treasury` | `yield_optimizer.py`, `liquidity_monitor.py` |
| `payments` | `transfer_service.py` |

---

## Deliverable 1: Design Corporate Treasury Dashboard

### Frontend: `TreasuryDashboard.jsx`, `CashFlowChart.jsx`, `LiquidityGauge.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/treasury/summary` | `get_cash_summary()` |
| GET | `/api/v1/treasury/forecast` | `get_cash_forecast()` |

### Acceptance Criteria
- [ ] **F24.1.1**: Total cash view across all accounts (Bank + Brokerage)
- [ ] **F24.1.2**: Buying power vs Settled cash distinction
- [ ] **F24.1.3**: 30-day cash flow forecast visualization
- [ ] **F24.1.4**: Liquidity coverage ratio indicator
- [ ] **F24.1.5**: Alert on low operational cash

---

## Deliverable 2: Yield Optimizer Page

### Frontend: `YieldOptimizer.jsx`, `OpportunityTable.jsx`, `AllocationPie.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/treasury/yield/opportunities` | `get_yield_options()` |
| POST | `/api/v1/treasury/allocations` | `optimize_allocations()` |

### Acceptance Criteria
- [ ] **F24.2.1**: Scan for idle cash > threshold
- [ ] **F24.2.2**: Compare yields (MMF, T-Bills, HYS)
- [ ] **F24.2.3**: Recommendations to move cash for higher yield
- [ ] **F24.2.4**: Risk-free rate benchmark comparison
- [ ] **F24.2.5**: One-click sweep configuration

---

## Deliverable 3: Transfer Center Page

### Frontend: `TransferCenter.jsx`, `TransferForm.jsx`, `HistoryTable.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| POST | `/api/v1/payments/transfer` | `initiate_transfer()` |
| GET | `/api/v1/payments/history` | `get_transfer_history()` |
| GET | `/api/v1/banking/accounts` | `get_linkable_accounts()` |

### Acceptance Criteria
- [ ] **F24.3.1**: Initiate ACH/Wire between linked accounts
- [ ] **F24.3.2**: Approval workflow for large amounts
- [ ] **F24.3.3**: Scheduled recurring transfers
- [ ] **F24.3.4**: Status tracking (Pending, Cleared, Failed)
- [ ] **F24.3.5**: Fee estimation per transfer type

---

## Deliverable 4: Expense Management Page

### Frontend: `ExpenseManager.jsx`, `ExpenseChart.jsx`, `PaymentTable.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/banking/expenses` | `get_expenses()` |
| POST | `/api/v1/banking/expenses/categorize` | `categorize_transaction()` |

### Acceptance Criteria
- [ ] **F24.4.1**: Tracking operational expenses (Data feeds, Cloud costs)
- [ ] **F24.4.2**: Categorization by cost center
- [ ] **F24.4.3**: Budget vs Actuals comparison
- [ ] **F24.4.4**: Vendor payment scheduling
- [ ] **F24.4.5**: Invoice attachment support

---

## Deliverable 5: Bank Relationship Manager

### Frontend: `BankManager.jsx`, `BankCard.jsx`, `FeeSchedule.jsx`

### Backend Endpoints
| Method | Endpoint | Handler |
|--------|----------|---------|
| GET | `/api/v1/banking/relationships` | `list_banks()` |
| GET | `/api/v1/banking/fees/{bank_id}` | `get_bank_fees()` |

### Acceptance Criteria
- [ ] **F24.5.1**: Manage multiple bank connections
- [ ] **F24.5.2**: Credential status monitoring
- [ ] **F24.5.3**: Fee schedule repository
- [ ] **F24.5.4**: Contact info for bank reps
- [ ] **F24.5.5**: FDICE insurance coverage tracking per bank

---

## Sign-Off
| Role | Name | Date | Signature |
|------|------|------|-----------|
| Developer | | | |
| QA | | | |

*Phase 24 - Version 1.0*
