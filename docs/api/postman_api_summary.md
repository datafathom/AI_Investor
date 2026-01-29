================================================================================
POSTMAN COLLECTION API STRUCTURE
Total Endpoints: 404
Total Top-Level Folders: 10
================================================================================


## ? AI & Automation (24 endpoints)
------------------------------------------------------------

  ### Ai Assistant
    [POST  ] /api/ai-assistant/conversation/create
    [GET   ] /api/ai-assistant/conversation/<conversation_id>
    [POST  ] /api/ai-assistant/conversation/<conversation_id>/message
    [GET   ] /api/ai-assistant/recommendations/<user_id>

  ### Ai Autocoder
    [POST  ] /api/v1/ai/autocoder/generate
    [POST  ] /api/v1/ai/autocoder/execute
    [GET   ] /api/v1/ai/autocoder/status

  ### Autocoder
    [POST  ] /api/v1/dev/generate
    [POST  ] /api/v1/dev/validate
    [POST  ] /api/v1/dev/deploy
    [GET   ] /api/v1/dev/status

  ### Evolution
    [POST  ] /api/v1/evolution/start
    [GET   ] /api/v1/evolution/status

  ### Ml Training
    [POST  ] /api/ml/training/job/create
    [POST  ] /api/ml/training/job/<job_id>/start
    [POST  ] /api/ml/training/job/<job_id>/complete
    [POST  ] /api/ml/deployment/deploy
    [GET   ] /api/ml/deployment/<model_id>/performance

  ### Research
    [POST  ] /api/v1/ai/portfolio-report
    [POST  ] /api/v1/ai/company-research
    [GET   ] /api/v1/ai/report/<report_id>
    [GET   ] /api/v1/ai/report/<report_id>/pdf
    [GET   ] /api/v1/ai/report/<report_id>/html
    [GET   ] /api/v1/ai/report/<report_id>/excel

## ? Authentication & Identity (19 endpoints)
------------------------------------------------------------

  ### Auth
    [POST  ] /api/auth/login
    [POST  ] /api/auth/register
    [GET   ] /api/auth/verify-email
    [POST  ] /api/auth/add-password
    [POST  ] /api/auth/mfa/setup
    [POST  ] /api/auth/mfa/verify
    [GET   ] /api/auth/social/login/<provider>
    [POST  ] /api/auth/social/callback/<provider>

  ### Facebook Auth
    [GET   ] /api/v1/auth/facebook/login
    [GET   ] /api/v1/auth/facebook/callback
    [POST  ] /api/v1/auth/facebook/callback
    [POST  ] /api/v1/auth/facebook/long-lived-token
    [POST  ] /api/v1/auth/facebook/revoke

  ### Google Auth
    [GET   ] /api/v1/auth/google/login
    [GET   ] /api/v1/auth/google/callback
    [POST  ] /api/v1/auth/google/callback
    [POST  ] /api/v1/auth/google/refresh
    [POST  ] /api/v1/auth/google/revoke
    [GET   ] /api/v1/auth/google/profile

## ? Communication (13 endpoints)
------------------------------------------------------------

  ### Communication
    [GET   ] /api/v1/communication/briefing
    [POST  ] /api/v1/communication/test-alert

  ### Discord
    [GET   ] /api/v1/discord/mentions/<ticker>
    [GET   ] /api/v1/discord/hype/<ticker>
    [POST  ] /api/v1/discord/webhook/test
    [POST  ] /api/v1/discord/webhook/alert

  ### Gmail
    [POST  ] /api/v1/gmail/send
    [POST  ] /api/v1/gmail/send-template
    [GET   ] /api/v1/gmail/preview
    [GET   ] /api/v1/gmail/stats

  ### Youtube
    [GET   ] /api/v1/youtube/search
    [GET   ] /api/v1/youtube/transcript/<video_id>
    [GET   ] /api/v1/youtube/analyze/<video_id>

## ? Financial Planning (33 endpoints)
------------------------------------------------------------

  ### Billing
    [POST  ] /api/billing/bill/create
    [GET   ] /api/billing/bill/upcoming/<user_id>
    [POST  ] /api/billing/payment/schedule
    [GET   ] /api/billing/payment/history/<user_id>
    [POST  ] /api/billing/reminder/create
    [POST  ] /api/billing/reminder/send/<user_id>

  ### Budgeting
    [POST  ] /api/budgeting/budget/create
    [GET   ] /api/budgeting/budget/<budget_id>/analyze
    [POST  ] /api/budgeting/expense/add
    [GET   ] /api/budgeting/expense/<user_id>
    [GET   ] /api/budgeting/trends/<user_id>

  ### Credit
    [POST  ] /api/credit/score/track
    [GET   ] /api/credit/score/history/<user_id>
    [GET   ] /api/credit/factors/<user_id>
    [GET   ] /api/credit/recommendations/<user_id>
    [POST  ] /api/credit/simulate/<user_id>

  ### Financial Planning
    [POST  ] /api/planning/plan/create
    [GET   ] /api/planning/plan/<user_id>
    [POST  ] /api/planning/goal/project/<goal_id>
    [POST  ] /api/planning/goal/optimize/<plan_id>
    [GET   ] /api/planning/goal/<goal_id>/progress
    [PUT   ] /api/planning/goal/<goal_id>/update

  ### Retirement
    [POST  ] /api/retirement/project
    [POST  ] /api/retirement/compare
    [POST  ] /api/retirement/withdrawal/plan
    [GET   ] /api/retirement/rmd/<user_id>
    [POST  ] /api/retirement/withdrawal/optimize

  ### Tax Optimization
    [GET   ] /api/v1/tax-optimization/harvest/opportunities/<portfolio_id>
    [POST  ] /api/v1/tax-optimization/harvest/batch/<portfolio_id>
    [POST  ] /api/v1/tax-optimization/harvest/execute/<portfolio_id>
    [POST  ] /api/v1/tax-optimization/optimize/lot_selection/<portfolio_id>
    [POST  ] /api/v1/tax-optimization/optimize/project/<portfolio_id>
    [POST  ] /api/v1/tax-optimization/optimize/withdrawal/<portfolio_id>

## ? Market Data & Analysis (23 endpoints)
------------------------------------------------------------

  ### Macro
    [GET   ] /api/v1/macro/insider-trades
    [GET   ] /api/v1/macro/cpi/<country>
    [GET   ] /api/v1/macro/correlations
    [GET   ] /api/v1/macro/world-map
    [GET   ] /api/v1/macro/calendar
    [GET   ] /api/v1/macro/futures/<commodity>
    [GET   ] /api/v1/macro/futures
    [GET   ] /api/v1/macro/crack-spread
    [GET   ] /api/v1/macro/dashboard

  ### Macro Data
    [GET   ] /api/v1/macro-data/regime
    [GET   ] /api/v1/macro-data/yield-curve
    [GET   ] /api/v1/macro-data/series/<series_id>
    [GET   ] /api/v1/macro-data/indicators
    [GET   ] /api/v1/macro-data/health

  ### News
    [GET   ] /api/v1/news/articles
    [GET   ] /api/v1/news/symbol/<symbol>
    [GET   ] /api/v1/news/trending
    [GET   ] /api/v1/news/sentiment/<symbol>
    [GET   ] /api/v1/news/impact/<symbol>

  ### Stocktwits
    [GET   ] /api/v1/stocktwits/stream/<symbol>
    [GET   ] /api/v1/stocktwits/trending
    [GET   ] /api/v1/stocktwits/sentiment/<symbol>
    [GET   ] /api/v1/stocktwits/volume-spike/<symbol>

## ? Other (212 endpoints)
------------------------------------------------------------

  ### Advanced Risk
    [GET   ] /api/v1/advanced-risk/metrics/<portfolio_id>
    [POST  ] /api/v1/advanced-risk/stress/historical/<portfolio_id>
    [POST  ] /api/v1/advanced-risk/stress/monte_carlo/<portfolio_id>
    [POST  ] /api/v1/advanced-risk/stress/custom/<portfolio_id>

  ### Ai Predictions
    [POST  ] /api/ai-predictions/price
    [POST  ] /api/ai-predictions/trend
    [GET   ] /api/ai-predictions/regime
    [POST  ] /api/ai-predictions/news-impact

  ### Analytics
    [GET   ] /api/v1/analytics/attribution/<portfolio_id>
    [GET   ] /api/v1/analytics/contribution/<portfolio_id>
    [GET   ] /api/v1/analytics/risk/factor/<portfolio_id>
    [GET   ] /api/v1/analytics/risk/concentration/<portfolio_id>
    [GET   ] /api/v1/analytics/risk/correlation/<portfolio_id>
    [GET   ] /api/v1/analytics/risk/tail/<portfolio_id>

  ### Backtest Api V1
    [POST  ] /api/v1/backtest/monte-carlo
    [GET   ] /api/v1/backtest/overfit

  ### Banking Api
    [POST  ] /api/v1/banking/plaid/create-link-token
    [POST  ] /api/v1/banking/plaid/exchange-public-token
    [GET   ] /api/v1/banking/accounts
    [POST  ] /api/v1/banking/sync
    [GET   ] /api/v1/banking/reconciliation

  ### Binance Bp
    [GET   ] /api/v1/binance/ticker/<symbol>
    [GET   ] /api/v1/binance/depth/<symbol>
    [POST  ] /api/v1/binance/order

  ### Briefing Bp
    [GET   ] /api/v1/ai/briefing/daily

  ### Brokerage Api
    [GET   ] /api/v1/brokerage/status
    [GET   ] /api/v1/brokerage/providers
    [GET   ] /api/v1/brokerage/positions
    [POST  ] /api/v1/brokerage/connect

  ### Calendar
    [POST  ] /api/v1/calendar/events
    [GET   ] /api/v1/calendar/events
    [PUT   ] /api/v1/calendar/events/<event_id>
    [DELETE] /api/v1/calendar/events/<event_id>
    [POST  ] /api/v1/calendar/sync/earnings

  ### Cash Api
    [GET   ] /api/v1/cash/dashboard
    [GET   ] /api/v1/cash/fx/rates
    [POST  ] /api/v1/cash/fx/convert
    [GET   ] /api/v1/cash/sweep/suggestions

  ### Coinbase Bp
    [POST  ] /api/v1/wallet/coinbase/connect
    [GET   ] /api/v1/wallet/coinbase/balance
    [GET   ] /api/v1/wallet/coinbase/transactions

  ### Compliance Api V1
    [GET   ] /api/v1/compliance/overview
    [GET   ] /api/v1/compliance/audit
    [GET   ] /api/v1/compliance/sar
    [POST  ] /api/v1/compliance/sar/<sap_id>/status
    [GET   ] /api/v1/compliance/verify

  ### Corporate Api V1
    [GET   ] /api/v1/corporate/earnings

  ### Crypto Api Bp
    [GET   ] /api/v1/market/crypto/price
    [GET   ] /api/v1/market/crypto/volume/<symbol>

  ### Debate Bp
    [POST  ] /api/v1/ai/debate/start
    [GET   ] /api/v1/ai/debate/stream
    [POST  ] /api/v1/ai/debate/inject
    [POST  ] /api/v1/ai/debate/run/<ticker>

  ### Documents
    [POST  ] /api/v1/documents
    [GET   ] /api/v1/documents
    [GET   ] /api/v1/documents/<document_id>
    [DELETE] /api/v1/documents/<document_id>

  ### Economics
    [GET   ] /api/v1/economics/clew
    [GET   ] /api/v1/economics/cpi

  ### Education
    [POST  ] /api/v1/education/course/create
    [GET   ] /api/v1/education/courses
    [POST  ] /api/v1/education/enroll
    [PUT   ] /api/v1/education/enrollment/<enrollment_id>/progress
    [POST  ] /api/v1/education/enrollment/<enrollment_id>/certificate

  ### Email Api Bp
    [POST  ] /api/v1/notifications/email/send
    [POST  ] /api/v1/notifications/email/subscribe

  ### Estate Api V1
    [GET   ] /api/v1/estate/heartbeat

  ### Facebook Hype
    [POST  ] /api/v1/facebook/monitor
    [GET   ] /api/v1/facebook/aggregates
    [POST  ] /api/v1/facebook/check-spike

  ### Fixed Income
    [GET   ] /api/v1/fixed-income/yield-curve
    [GET   ] /api/v1/fixed-income/yield-curve/history
    [POST  ] /api/v1/fixed-income/rate-shock
    [POST  ] /api/v1/fixed-income/duration
    [POST  ] /api/v1/fixed-income/wal
    [GET   ] /api/v1/fixed-income/gaps/<portfolio_id>
    [GET   ] /api/v1/fixed-income/inversion

  ### Forum
    [POST  ] /api/forum/thread/create
    [GET   ] /api/forum/threads
    [POST  ] /api/forum/thread/<thread_id>/reply
    [POST  ] /api/forum/thread/<thread_id>/upvote

  ### Homeostasis Api
    [GET   ] /api/v1/homeostasis/status
    [POST  ] /api/v1/homeostasis/update
    [POST  ] /api/v1/homeostasis/donate

  ### Ibkr
    [GET   ] /api/v1/ibkr/account-summary
    [GET   ] /api/v1/ibkr/positions
    [GET   ] /api/v1/ibkr/orders
    [POST  ] /api/v1/ibkr/orders
    [DELETE] /api/v1/ibkr/orders/<int:order_id>
    [GET   ] /api/v1/ibkr/margin
    [GET   ] /api/v1/ibkr/currency-exposure
    [GET   ] /api/v1/ibkr/gateway/status

  ### Identity Api
    [GET   ] /api/v1/identity/profile
    [POST  ] /api/v1/identity/reconcile
    [POST  ] /api/v1/identity/manual-verify

  ### Incident Api Bp
    [POST  ] /api/v1/ops/incidents/trigger
    [GET   ] /api/v1/ops/incidents

  ### Integration
    [POST  ] /api/integration/create
    [GET   ] /api/integration/user/<user_id>
    [POST  ] /api/integration/<integration_id>/sync

  ### Integrations Api V1
    [GET   ] /api/v1/integrations/connectors

  ### Kyc Api
    [GET   ] /api/v1/kyc/status
    [GET   ] /api/v1/kyc/documents
    [POST  ] /api/v1/kyc/documents/upload
    [GET   ] /api/v1/kyc/filings/calendar
    [POST  ] /api/v1/kyc/verify

  ### Legal
    [GET   ] /api/v1/legal/documents
    [GET   ] /api/v1/legal/documents/<document_id>
    [POST  ] /api/v1/legal/accept
    [GET   ] /api/v1/legal/acceptance-status
    [GET   ] /api/v1/legal/acceptance-history
    [GET   ] /api/v1/legal/check-updates

  ### Margin Api V1
    [GET   ] /api/v1/margin/status

  ### Market Bp
    [GET   ] /api/v1/market/fear-greed
    [GET   ] /api/v1/market/hypemeter
    [GET   ] /api/v1/market/hypemeter/top
    [GET   ] /api/v1/market/options/<symbol>
    [GET   ] /api/v1/market/dom/<symbol>

  ### Market Data
    [GET   ] /api/v1/market/quote/<symbol>
    [GET   ] /api/v1/market/history/<symbol>
    [GET   ] /api/v1/market/intraday/<symbol>
    [GET   ] /api/v1/market/short-interest/<symbol>
    [GET   ] /api/v1/market/earnings
    [GET   ] /api/v1/market/health

  ### Marketplace
    [POST  ] /api/marketplace/extension/create
    [GET   ] /api/marketplace/extensions
    [POST  ] /api/marketplace/extension/<extension_id>/install
    [POST  ] /api/marketplace/extension/<extension_id>/review

  ### Mobile Api V1
    [POST  ] /api/v1/mobile/kill-switch

  ### Onboarding
    [GET   ] /api/v1/onboarding/status
    [POST  ] /api/v1/onboarding/step
    [POST  ] /api/v1/onboarding/complete
    [GET   ] /api/v1/onboarding/preferences
    [PUT   ] /api/v1/onboarding/preferences
    [POST  ] /api/v1/onboarding/skip
    [POST  ] /api/v1/onboarding/reset

  ### Optimization
    [POST  ] /api/v1/optimization/optimize/<portfolio_id>
    [GET   ] /api/v1/optimization/rebalancing/check/<portfolio_id>
    [POST  ] /api/v1/optimization/rebalancing/recommend/<portfolio_id>
    [POST  ] /api/v1/optimization/rebalancing/execute/<portfolio_id>
    [GET   ] /api/v1/optimization/rebalancing/history/<portfolio_id>

  ### Paypal Bp
    [POST  ] /api/v1/payment/paypal/create-order
    [POST  ] /api/v1/payment/paypal/capture-order

  ### Philanthropy Api V1
    [POST  ] /api/v1/philanthropy/donate
    [GET   ] /api/v1/philanthropy/history
    [GET   ] /api/v1/philanthropy/esg
    [GET   ] /api/v1/philanthropy/carbon

  ### Politics
    [GET   ] /api/v1/politics/disclosures
    [GET   ] /api/v1/politics/alpha/<ticker>

  ### Privacy Api
    [GET   ] /api/v1/privacy/export
    [DELETE] /api/v1/privacy/forget-me

  ### Public Api
    [POST  ] /api/public/api-key/create
    [GET   ] /api/public/api-key/<api_key_id>
    [GET   ] /api/public/documentation
    [GET   ] /api/public/sdks

  ### Qa
    [POST  ] /api/qa/question/create
    [POST  ] /api/qa/question/<question_id>/best-answer

  ### Risk Api
    [GET   ] /api/v1/risk/status
    [POST  ] /api/v1/risk/kill-switch
    [POST  ] /api/v1/risk/preview

  ### Robinhood
    [POST  ] /api/v1/robinhood/connect
    [GET   ] /api/v1/robinhood/holdings
    [GET   ] /api/v1/robinhood/orders
    [GET   ] /api/v1/robinhood/transactions
    [GET   ] /api/v1/robinhood/cost-basis

  ### Scanner Api
    [GET   ] /api/v1/scanner/matches
    [GET   ] /api/v1/scanner/galaxy
    [GET   ] /api/v1/scanner/pulse

  ### Scenario Api V1
    [POST  ] /api/v1/scenario/simulate
    [GET   ] /api/v1/scenario/monte-carlo-refined
    [GET   ] /api/v1/scenario/bank-run

  ### Settlement Api V1
    [GET   ] /api/v1/settlement/balances
    [GET   ] /api/v1/settlement/rates
    [POST  ] /api/v1/settlement/convert

  ### Simulation
    [POST  ] /api/simulation/run

  ### Social Bp
    [GET   ] /api/v1/social/reddit/posts
    [GET   ] /api/v1/social/reddit/analyze/<ticker>
    [GET   ] /api/v1/social/sentiment/heatmap

  ### Social Trading
    [POST  ] /api/social-trading/profile/create
    [GET   ] /api/social-trading/traders/top
    [POST  ] /api/social-trading/follow
    [POST  ] /api/social-trading/copy/create
    [POST  ] /api/social-trading/copy/execute

  ### Solana
    [GET   ] /api/v1/solana/balance/<address>
    [GET   ] /api/v1/solana/tokens/<address>
    [GET   ] /api/v1/solana/transactions/<address>
    [GET   ] /api/v1/solana/token-info/<mint>

  ### Spatial
    [GET   ] /api/v1/spatial/portfolio
    [GET   ] /api/v1/spatial/status

  ### Square Bp
    [GET   ] /api/v1/merchant/square/stats
    [GET   ] /api/v1/merchant/square/catalog
    [GET   ] /api/v1/api/v1/square/stats
    [GET   ] /api/v1/api/v1/square/transactions
    [GET   ] /api/v1/api/v1/square/refunds

  ### Stripe Bp
    [GET   ] /api/v1/billing/subscription
    [POST  ] /api/v1/billing/checkout

  ### System Api V1
    [GET   ] /api/v1/system/health
    [GET   ] /api/v1/system/secrets
    [GET   ] /api/v1/system/supply-chain

  ### System Bp
    [GET   ] /api/v1/system/kafka/stats
    [GET   ] /api/v1/system/kafka/status

  ### Tax Api Bp
    [GET   ] /api/v1/tax/harvesting/opportunities

  ### Taxbit
    [POST  ] /api/v1/taxbit/ingest-transactions
    [POST  ] /api/v1/taxbit/generate-document
    [GET   ] /api/v1/taxbit/documents
    [GET   ] /api/v1/taxbit/documents/<int:year>

  ### Twilio Api Bp
    [POST  ] /api/v1/notifications/twilio/send

  ### Venmo Bp
    [POST  ] /api/v1/payment/venmo/pay

  ### Workspace Api
    [GET   ] /api/v1/user/workspace
    [POST  ] /api/v1/user/workspace
    [GET   ] /api/v1/user/workspaces

  ### Zen Api V1
    [GET   ] /api/v1/homeostasis/calculate

## ? Payments & Billing (7 endpoints)
------------------------------------------------------------

  ### Payment Transfer
    [GET   ] /api/v1/payments/linked-vendors
    [POST  ] /api/v1/payments/transfer

  ### Plaid
    [POST  ] /api/v1/link-token
    [POST  ] /api/v1/exchange-token
    [GET   ] /api/v1/accounts
    [GET   ] /api/v1/balance
    [POST  ] /api/v1/check-overdraft

## ? Portfolio & Trading (37 endpoints)
------------------------------------------------------------

  ### Advanced Orders
    [POST  ] /api/orders/trailing-stop
    [POST  ] /api/orders/bracket
    [POST  ] /api/orders/oco
    [POST  ] /api/orders/conditional
    [PUT   ] /api/orders/trailing-stop/<order_id>/update

  ### Alert
    [POST  ] /api/alert/create
    [GET   ] /api/alert/user/<user_id>
    [POST  ] /api/alert/<alert_id>/cancel

  ### Dashboard
    [GET   ] /api/v1/dashboard/allocation
    [GET   ] /api/v1/dashboard/risk
    [GET   ] /api/v1/dashboard/execution

  ### Execution
    [POST  ] /api/execution/twap
    [POST  ] /api/execution/vwap
    [POST  ] /api/execution/implementation-shortfall

  ### Options
    [POST  ] /api/options/strategy/create
    [POST  ] /api/options/strategy/template
    [GET   ] /api/options/strategy/<strategy_id>/greeks
    [GET   ] /api/options/strategy/<strategy_id>/pnl
    [POST  ] /api/options/strategy/<strategy_id>/analyze
    [GET   ] /api/options/chain

  ### Paper Trading
    [POST  ] /api/paper-trading/portfolio/create
    [GET   ] /api/paper-trading/portfolio/<portfolio_id>
    [POST  ] /api/paper-trading/order/execute
    [GET   ] /api/paper-trading/portfolio/<portfolio_id>/performance

  ### Strategy
    [POST  ] /api/strategy/create
    [GET   ] /api/strategy/<strategy_id>
    [POST  ] /api/strategy/<strategy_id>/rule
    [GET   ] /api/strategy/templates
    [POST  ] /api/strategy/<strategy_id>/validate
    [POST  ] /api/strategy/<strategy_id>/start
    [POST  ] /api/strategy/<strategy_id>/stop
    [POST  ] /api/strategy/<strategy_id>/pause
    [GET   ] /api/strategy/<strategy_id>/performance

  ### Watchlist
    [POST  ] /api/watchlist/create
    [GET   ] /api/watchlist/user/<user_id>
    [POST  ] /api/watchlist/<watchlist_id>/add
    [POST  ] /api/watchlist/<watchlist_id>/remove

## ? System & Admin (18 endpoints)
------------------------------------------------------------

  ### Docs
    [GET   ] /api/docs
    [GET   ] /api/docs/openapi.json
    [GET   ] /api/docs/redoc
    [GET   ] /api/docs/swagger.yaml

  ### Enterprise
    [POST  ] /api/enterprise/organization/create
    [POST  ] /api/enterprise/team/create
    [POST  ] /api/enterprise/team/<team_id>/member
    [POST  ] /api/enterprise/resource/share

  ### General
    [GET   ] /api/v1/gap
    [GET   ] /api/v1/market/predict

  ### Health
    [GET   ] /api/health
    [GET   ] /health
    [GET   ] /health/readiness
    [GET   ] /health/liveness
    [GET   ] /health/detailed

  ### Institutional
    [POST  ] /api/institutional/client/create
    [POST  ] /api/institutional/whitelabel/configure
    [POST  ] /api/institutional/report/generate

## ? Web3 & Crypto (18 endpoints)
------------------------------------------------------------

  ### Coinbase Crypto
    [GET   ] /api/v1/coinbase/accounts
    [GET   ] /api/v1/coinbase/trading-pairs
    [POST  ] /api/v1/coinbase/orders
    [GET   ] /api/v1/coinbase/orders
    [GET   ] /api/v1/coinbase/vaults
    [POST  ] /api/v1/coinbase/vaults/withdraw

  ### Ethereum
    [GET   ] /api/v1/ethereum/balance/<address>
    [GET   ] /api/v1/ethereum/tokens/<address>
    [GET   ] /api/v1/ethereum/gas-price
    [POST  ] /api/v1/ethereum/validate-address

  ### Web3
    [GET   ] /api/v1/web3/portfolio/<user_id>
    [GET   ] /api/v1/web3/balance/<address>/<chain>
    [GET   ] /api/v1/web3/chains
    [GET   ] /api/v1/web3/gas/<chain>
    [GET   ] /api/v1/web3/gas/optimal-window
    [POST  ] /api/v1/web3/gas/queue
    [GET   ] /api/v1/web3/lp/<user_id>
    [POST  ] /api/v1/web3/lp/il