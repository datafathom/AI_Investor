# Implementation Plan - [x] Cycle M: Trading & Strategy Stabilization
- [x] Cycle N: Advanced Portfolio & Risk Analytics
- [ ] Cycle O: Market Data & Indicators

---

## Cycle O: Market Data & Indicators

### [Market Data API]
#### [MODIFY] [test_market_data_api.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/tests/api/test_market_data_api.py)
- Update `Quote` and `OHLCV` mocks to match Pydantic V2 fields (e.g., ensure `timestamp` is present).
- Standardize fixture names to `app` and `client`.
- Remove `async` from test methods.

### [News & Sentiment API]
#### [MODIFY] [test_news_api.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/tests/api/test_news_api.py)
- Correct model imports: `SentimentAnalysis` -> `NewsSentiment`.
- Update `NewsArticle` and `NewsSentiment` mocks with all required fields (e.g., `published_date`, `content`, `source`, `relevance_score`, `bullish_count`, `bearish_count`, `neutral_count`, `confidence`, `last_updated`).
- Remove `async` from test methods.

### [Charting & Technical Analysis API]
#### [MODIFY] [test_charting_api.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/tests/api/test_charting_api.py)
- Standardize mocks for `get_chart_data`, `calculate_indicators`, `recognize_patterns`, and `generate_signals`.
- Remove `async` from test methods.

### [Macro Data API]
#### [MODIFY] [test_macro_data_api.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/tests/api/test_macro_data_api.py)
- Verify and fix API route prefixes (check if `/api/v1/macro-data` or `/api/macro-data` is correct).
- Update FRED service mocks for `get_regime`, `get_yield_curve`, etc.
- Remove `async` from test methods.

### [Research & Reports API]
#### [MODIFY] [test_research_api.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/tests/api/test_research_api.py)
- Update `ResearchReport` mock with all required fields (e.g., `content`, `sections`, `charts`, `data`, `created_date`, `updated_date`).
- Remove `async` from test methods.

## Proposed Changes

### 1. Paper Trading API
#### [MODIFY] [test_paper_trading_api.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/tests/api/test_paper_trading_api.py)
- Update imports from `models.trading` to `models.paper_trading`.
- Remove `@pytest.mark.asyncio` and `async` keywords from synchronous test functions.
- (Wait, checking if they are actually async in the API first).

### 2. Strategy API
#### [MODIFY] [test_strategy_api.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/tests/api/test_strategy_api.py)
- Change import `from models.strategy import Strategy` to `from models.strategy import TradingStrategy`.
- Update `test_start_strategy_success` and `test_get_strategy_performance_success` to include all required Pydantic fields.
- Remove incorrect `async` markers.

### 3. Backtest & Margin APIs
#### [MODIFY] [test_backtest_api.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/tests/api/test_backtest_api.py)
#### [MODIFY] [test_margin_api.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/tests/api/test_margin_api.py)
- Replace `response.get_json()` with `response.json()` as these tests use FastAPI's `TestClient`.

### 4. Options API
#### [MODIFY] [test_options_api.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/tests/api/test_options_api.py)
- Update `PnLAnalysis` import to `StrategyPnL`.
- Populate missing fields in `OptionsStrategy` and `StrategyAnalysis` mocks.
- Fix async/sync markers.

### 5. Scenario API
#### [MODIFY] [test_scenario_api.py](file:///c:/Users/astir/Desktop/AI_Company/AI_Investor/tests/api/test_scenario_api.py)
- Update `ScenarioResult` mock instantiation to include `scenario_id` and `positions_affected`.
- Replace `response.get_json()` with `response.json()`.

## Verification Plan

### Automated Tests
Run the Cycle M test suite:
```powershell
python -m pytest tests/api/test_paper_trading_api.py tests/api/test_strategy_api.py tests/api/test_backtest_api.py tests/api/test_options_api.py tests/api/test_margin_api.py tests/api/test_scenario_api.py -vv
```
Target: 100% Pass Rate.
