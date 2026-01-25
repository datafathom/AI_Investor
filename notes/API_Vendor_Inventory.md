# API Vendor Inventory & Master Data Sources

This document provides a comprehensive, numbered list of all external API vendors and data sources integrated or architected into the AI Investor platform.

> [!IMPORTANT]
> **Agnostic Architecture**: The platform uses a sentinel layer (`APIGovernor`) to manage quotas across all vendors, ensuring the application remains "Free Tier" compliant and cost-controlled.

---

## 1. Market & Financial Data
1. **Alpha Vantage (Primary)**
   - **Purpose**: Real-time equity prices, options flow, and earnings calendars.
   - **Free Tier**: 25 requests/day | 5 requests/minute.
   - **Fees**: Premium starts at ~$49/mo for higher throughput.
   - **Portal**: https://www.alphavantage.co/documentation/
   - **API Documentation**: https://www.alphavantage.co/documentation/
   - **Key**: `ALPHA_VANTAGE_API_KEY`

2. **FRED (Federal Reserve)**
   - **Purpose**: Global macroeconomic indicators (CPI, Unemployment, Yield Curve).
   - **Free Tier**: 120 requests/minute.
   - **Fees**: Free for public data.
   - **Portal**: https://fredaccount.stlouisfed.org/apikeys
   - **API Documentation**: https://fred.stlouisfed.org/docs/api/fred/
   - **Key**: `FRED_API_KEY`

3. **Polygon.io (Secondary)**
   - **Purpose**: Backup high-speed historical tick and bar data.
   - **Free Tier**: 5 requests/minute | 2 years historical data.
   - **Fees**: ~$29/mo for real-time/unlimited.
   - **Portal**: https://polygon.io/dashboard/api-keys
   - **API Documentation**: https://polygon.io/docs/stocks/getting-started
   - **Key**: `POLYGON_API_KEY`

4. **Quandl / Nasdaq Data Link**
   - **Purpose**: Institutional-grade alternative data (short interest, insider trades, economic indicators).
   - **Free Tier**: 300 calls/10sec | 50,000 calls/day (free datasets).
   - **Fees**: Premium datasets from $500+/mo.
   - **Portal**: https://data.nasdaq.com/
   - **API Documentation**: https://docs.data.nasdaq.com/
   - **Key**: `QUANDL_API_KEY`

5. **Finnhub**
   - **Purpose**: Real-time stock/forex/crypto data, IPO/Earnings calendars.
   - **Free Tier**: 30 API calls/second | Limited historical data.
   - **Fees**: Commercial license required for production use.
   - **Portal**: https://finnhub.io/dashboard
   - **API Documentation**: https://finnhub.io/docs/api
   - **Key**: `FINNHUB_API_KEY`

6. **NewsAPI.org**
   - **Purpose**: Aggregated breaking news headlines for sentiment triggers.
   - **Free Tier**: 100 requests/day | 24-hour delay on articles.
   - **Fees**: Paid plans from ~$449/mo for real-time access.
   - **Portal**: https://newsapi.org/account
   - **API Documentation**: https://newsapi.org/docs
   - **Key**: `NEWSAPI_API_KEY`

## 2. Artificial Intelligence & LLMs
7. **OpenAI (GPT-4/o)**
   - **Purpose**: Autonomous code generation (Autocoder) and high-level reasoning.
   - **Free Tier**: Minimal (New accounts get small trial credit).
   - **Fees**: Pay-as-you-go (~$2.50 to $15 per 1M tokens).
   - **Portal**: https://platform.openai.com
   - **API Documentation**: https://platform.openai.com/docs/api-reference
   - **Key**: `OPENAI_API_KEY`

8. **Anthropic (Claude)**
   - **Purpose**: Multi-persona "Debate Chamber".
   - **Free Tier**: Minimal trial credits for initial evaluation.
   - **Fees**: Pay-as-you-go (~$3 to $15 per 1M tokens for Sonnet).
   - **Portal**: https://console.anthropic.com
   - **API Documentation**: https://docs.anthropic.com
   - **Key**: `ANTHROPIC_API_KEY`

9. **Google Gemini (Integrated)**
   - **Purpose**: Market summaries and morning briefings.
   - **Free Tier**: 15 requests/min | 1,500 requests/day (Gemini 1.5 Flash).
   - **Fees**: Paid tier removes "Public Data Usage" for training.
   - **Portal**: https://ai.google.dev/studio
   - **API Documentation**: https://ai.google.dev/gemini-api/docs/api-reference
   - **Key**: `GEMINI_API_KEY`

10. **Perplexity AI (Planned)**
    - **Purpose**: Real-time news retrieval.
    - **Free Tier**: None (API only). Pro users ($20/mo) get $5 credit.
    - **Fees**: Pay-as-you-go (~$0.20 to $5 per 1M tokens).
    - **Portal**: https://www.perplexity.ai/settings/api
    - **API Documentation**: https://docs.perplexity.ai/
    - **Key**: `PERPLEXITY_API_KEY`

## 3. Payments, Billing & Financial Ingestion
11. **Stripe (Direct)**
    - **Purpose**: Subscription management and checkout sessions.
    - **Free Tier**: API access is free.
    - **Fees**: 2.9% + $0.30 per successful card charge.
    - **Portal**: https://dashboard.stripe.com
    - **API Documentation**: https://stripe.com/docs/api
    - **Key**: `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `STRIPE_PRICE_PRO`, `STRIPE_PRICE_INST`

12. **PayPal (Payments)**
    - **Purpose**: Alternative checkout provider and multi-currency support.
    - **Free Tier**: API access is free.
    - **Fees**: Approx 3.49% + $0.49 per transaction.
    - **Portal**: https://developer.paypal.com/dashboard/
    - **API Documentation**: https://developer.paypal.com/docs/api/
    - **Key**: `PAYPAL_CLIENT_ID` / `PAYPAL_CLIENT_SECRET`

13. **Venmo (Supported)**
    - **Purpose**: P2P payment linking and mobile-first checkout.
    - **Free Tier**: Free API access (via Braintree/PayPal).
    - **Fees**: 3% for credit cards; instant transfer fees apply.
    - **Portal**: https://developer.paypal.com/docs/checkout/pay-with-venmo/
    - **API Documentation**: https://developer.paypal.com/docs/checkout/pay-with-venmo/
    - **Key**: Reuses PayPal Credentials.

14. **Square (Supported)**
    - **Purpose**: Merchant processing aggregation and POS integration.
    - **Free Tier**: Free API access in Sandbox.
    - **Fees**: 2.6% + $0.10 (In-person) | 3.3% + $0.30 (Online).
    - **Portal**: https://developer.squareup.com/
    - **API Documentation**: https://developer.squareup.com/docs/api/connect/v2
    - **Key**: `SQUARE_ACCESS_TOKEN`

15. **Plaid**
    - **Purpose**: Link bank accounts for deposits, ACH transfers, and balance checks.
    - **Free Tier**: 200 API calls across all products.
    - **Fees**: ~$0.30 - $1.50 per connection/verification (varies by product).
    - **Portal**: https://dashboard.plaid.com/
    - **API Documentation**: https://plaid.com/docs/
    - **Key**: `PLAID_CLIENT_ID`, `PLAID_SECRET`, `PLAID_ENV` (default: `sandbox`)

## 4. Authentication & Global Identity
16. **Facebook / Meta (OAuth2 + Graph API)**
    - **Purpose**: SSO Login and social hype ingestion from Facebook/Instagram.
    - **Free Tier**: Free for standard OAuth and basic Graph API access.
    - **Fees**: Charges apply for high-volume Ads/Insights API usage.
    - **Portal**: https://developers.facebook.com/
    - **API Documentation**: https://developers.facebook.com/docs/graph-api
    - **Key**: `FACEBOOK_APP_ID` / `FACEBOOK_APP_SECRET`

17. **Google Cloud (OAuth2)**
    - **Purpose**: SSO Login, calendar sync, and drive workspace integration.
    - **Free Tier**: Free for standard OAuth operations.
    - **Fees**: Charges apply only for high-volume Cloud API usage.
    - **Portal**: https://console.cloud.google.com/apis/credentials
    - **API Documentation**: https://developers.google.com/identity/protocols/oauth2
    - **Key**: `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI`

18. **Gmail API**
    - **Purpose**: Email notifications, transactional alerts, and portfolio reports.
    - **Free Tier**: 1 billion quota units/day (reading/sending is low cost).
    - **Fees**: Free for most use cases; paid Workspace for enhanced features.
    - **Portal**: https://console.cloud.google.com/apis/library/gmail.googleapis.com
    - **API Documentation**: https://developers.google.com/gmail/api/guides
    - **Key**: Reuses `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`

19. **Google Calendar API**
    - **Purpose**: Scheduling earnings calls, rebalancing reminders, and dividend dates.
    - **Free Tier**: 1 million requests/day.
    - **Fees**: Free for most use cases.
    - **Portal**: https://console.cloud.google.com/apis/library/calendar-json.googleapis.com
    - **API Documentation**: https://developers.google.com/calendar/api/guides/overview
    - **Key**: Reuses `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET`

20. **Reddit OAuth**
    - **Purpose**: Sentiment-tied user profiling and authenticated social data.
    - **Free Tier**: 100 queries/minute (OAuth).
    - **Fees**: $0.24 per 1,000 calls for commercial/high-volume use.
    - **Portal**: https://www.reddit.com/prefs/apps
    - **API Documentation**: https://www.reddit.com/dev/api/
    - **Key**: `REDDIT_CLIENT_ID` / `REDDIT_CLIENT_SECRET`


## 5. Execution & Institutional Brokerage
19. **Alpaca Markets (Direct)**
    - **Purpose**: Automated equity trade execution and fractional shares.
    - **Free Tier**: Paper Trading (Free) | Commission-free live trading.
    - **Fees**: Market data free with funded account; otherwise subscription.
    - **Portal**: https://app.alpaca.markets/
    - **API Documentation**: https://alpaca.markets/docs/api-references/trading-api/
    - **Key**: `ALPACA_API_KEY` / `ALPACA_SECRET_KEY`

20. **Interactive Brokers (Planned)**
    - **Purpose**: Professional global execution across 150+ markets.
    - **Free Tier**: None (Trial account available).
    - **Fees**: Per-share commissions (approx $0.005/share).
    - **Portal**: https://www.interactivebrokers.com/en/trading/ib-api.php
    - **API Documentation**: https://www.interactivebrokers.com/api/doc.html
    - **Key**: `IBKR_GATEWAY_HOST`, `IBKR_GATEWAY_PORT`, `IBKR_CLIENT_ID`, `IBKR_USERNAME`, `IBKR_PASSWORD`

21. **Robinhood (via `robin_stocks`)**
    - **Purpose**: Retail brokerage sync and 1099-B data ingestion.
    - **Free Tier**: 0 commission.
    - **Fees**: Robinhood Gold subscription ($5/mo) for 24/5 trading.
    - **Portal**: https://robinhood.com/
    - **API Documentation**: https://robin-stocks.readthedocs.io/en/latest/
    - **Key**: `ROBINHOOD_USERNAME`, `ROBINHOOD_PASSWORD`, `ROBINHOOD_TOTP`

## 6. Crypto & Blockchain
22. **Cloudflare (Ethereum RPC)**
    - **Purpose**: Primary node for wallet balance retrieval and chain state.
    - **Free Tier**: Free public gateway (shared usage).
    - **Fees**: Higher tier usage requires Cloudflare Business/Enterprise.
    - **Portal**: https://www.cloudflare.com/web3/
    - **API Documentation**: https://developers.cloudflare.com/web3/ethereum-gateway/
    - **Key**: `ETH_RPC_URL` (default: `https://cloudflare-eth.com`)

23. **Solana Labs (RPC)**
    - **Purpose**: SPL token tracking and wallet health checks on Solana.
    - **Free Tier**: 100 requests / 10 seconds.
    - **Fees**: Free for basic mainnet-beta usage.
    - **Portal**: https://solana.com/rpc
    - **API Documentation**: https://solana.com/docs/rpc/http
    - **Key**: `SOL_RPC_URL` (default: `https://api.mainnet-beta.solana.com`)

24. **Coinbase Cloud (Planned)**
    - **Purpose**: Institutional custody and programmatic crypto trading.
    - **Free Tier**: Free for API access (Sandbox).
    - **Fees**: Trading fees approx 0.4% - 0.6% (Taker).
    - **Portal**: https://www.coinbase.com/cloud
    - **API Documentation**: https://docs.cloud.coinbase.com/
    - **Key**: `COINBASE_API_KEY` / `COINBASE_API_SECRET`

## 7. Social, Sentiment & Ingestion
25. **Reddit Sentiment**
    - **Purpose**: Tracking r/wallstreetbets and r/investing for momentum.
    - **Free Tier**: 100 queries/min.
    - **Fees**: $0.24 per 1k calls for large-scale production.
    - **Portal**: https://www.reddit.com/prefs/apps
    - **API Documentation**: https://www.reddit.com/dev/api/
    - **Key**: `REDDIT_CLIENT_ID`

26. **StockTwits**
    - **Purpose**: Real-time retail sentiment from dedicated trading community.
    - **Free Tier**: 500,000 requests/month | 1,000 requests/hour.
    - **Fees**: Commercial license for AI/sentiment products ~$10k/mo.
    - **Portal**: https://stocktwits.com/developers
    - **API Documentation**: https://api.stocktwits.com/developers/docs
    - **Key**: `STOCKTWITS_ACCESS_TOKEN`

27. **Discord**
    - **Purpose**: Server-based sentiment from crypto/stock trading communities.
    - **Free Tier**: Free for bot development.
    - **Fees**: None (Pay for premium hosting if needed).
    - **Portal**: https://discord.com/developers/applications
    - **API Documentation**: https://discord.com/developers/docs/reference
    - **Key**: `DISCORD_BOT_TOKEN`

28. **YouTube Data API v3**
    - **Purpose**: Transcribe macro strategy videos from institutional channels.
    - **Free Tier**: 10,000 units/day (1 search = 100 units).
    - **Fees**: Quota increases available on request (free).
    - **Portal**: https://console.cloud.google.com/apis/library/youtube.googleapis.com
    - **API Documentation**: https://developers.google.com/youtube/v3/docs
    - **Key**: `YOUTUBE_API_KEY`

29. **Google Trends (Integrated)**
    - **Purpose**: Z-Score retail mania tracking (e.g., "Margin Call" spikes).
    - **Free Tier**: No official fee (~5 calls/min via unofficial API).
    - **Fees**: Use official Vertex AI Search for higher throughput (varies).
    - **Portal**: https://trends.google.com/trends/
    - **API Documentation**: https://github.com/GeneralMills/pytrends
    - **Key**: N/A (IP-based throttling)

30. **Twitter/X (Architected)**
    - **Purpose**: Real-time breaking news and sentiment "Whales" tracking.
    - **Free Tier**: None (v2 Free tier removed).
    - **Fees**: $100/mo for Basic (50k tweets/mo).
    - **Portal**: https://developer.twitter.com/en/portal/dashboard
    - **API Documentation**: https://developer.twitter.com/en/docs/twitter-api
    - **Key**: `TWITTER_BEARER_TOKEN`

## 8. Communication & Notifications
31. **Twilio**
    - **Purpose**: SMS Alerts for margin calls, liquidation warnings, and 2FA.
    - **Free Tier**: Pay-as-you-go (no upfront cost, trial credits available).
    - **Fees**: ~$0.0083/SMS + carrier fees.
    - **Portal**: https://www.twilio.com/console
    - **API Documentation**: https://www.twilio.com/docs/sms/api
    - **Key**: `TWILIO_ACCOUNT_SID` / `TWILIO_AUTH_TOKEN`

32. **SendGrid**
    - **Purpose**: Transactional Emails (receipts, reports, account verification).
    - **Free Tier**: 100 emails/day (forever free).
    - **Fees**: Essentials plan from $19.95/mo.
    - **Portal**: https://app.sendgrid.com/
    - **API Documentation**: https://docs.sendgrid.com/api-reference
    - **Key**: `SENDGRID_API_KEY`

## 9. Tax, Compliance & Storage
33. **TaxBit**
    - **Purpose**: Automated 1099-B and crypto tax reporting for U.S. users.
    - **Free Tier**: Contact for enterprise access.
    - **Fees**: Enterprise pricing.
    - **Portal**: https://taxbit.com/developer/
    - **API Documentation**: https://taxbit.github.io/taxbit-developer-documentation/
    - **Key**: `TAXBIT_API_KEY`, `TAXBIT_CLIENT_ID`, `TAXBIT_CLIENT_SECRET`, `TAXBIT_BASE_URL`

34. **AWS S3**
    - **Purpose**: Document storage for tax docs, filings, and user uploads.
    - **Free Tier**: 5 GB storage | 20,000 GET | 2,000 PUT (12 months).
    - **Fees**: ~$0.023/GB/month (S3 Standard).
    - **Portal**: https://console.aws.amazon.com/s3/
    - **API Documentation**: https://docs.aws.amazon.com/AmazonS3/latest/API/Welcome.html
    - **Key**: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_S3_BUCKET`, `AWS_REGION` (default: `us-east-1`)

## 10. Regulatory & Philanthropy
35. **SEC EDGAR**
    - **Purpose**: Ingestion of Form 13F and 13D/G filings (Whale tracking).
    - **Free Tier**: 10 requests / second.
    - **Fees**: Free for public data.
    - **Portal**: https://www.sec.gov/edgar/filer-information
    - **API Documentation**: https://www.sec.gov/edgar/developer
    - **Key**: `USER_AGENT_EMAIL` (SEC Compliance)

36. **The Giving Block**
    - **Purpose**: Crypto-native donation routing and impact reporting.
    - **Free Tier**: Free API access for non-profits/partners.
    - **Fees**: 3.95% processing fee on crypto/stock donations.
    - **Portal**: https://www.thegivingblock.com/developers
    - **API Documentation**: https://developers.thegivingblock.com/
    - **Key**: `GIVINGBLOCK_API_KEY`, `GIVINGBLOCK_CRYPTO_ADDRESS` (⚠️ **Was hardcoded, now uses env**)

37. **Charity Navigator**
    - **Purpose**: Impact evaluation and efficiency scoring for 501(c)(3) entities.
    - **Free Tier**: Free basic research (1k calls/mo).
    - **Fees**: Paid plans for advanced financial metadata.
    - **Portal**: https://www.charitynavigator.org/research/api
    - **API Documentation**: https://charitynavigator.github.io/
    - **Key**: `CHARITYNAV_APP_ID`, `CHARITYNAV_APP_KEY`

---

## 11. Governance & Cost Sentinel
> [!IMPORTANT]
> All outgoing calls to these **37 vendors** are monitored by the `APIGovernor` found in `services/system/api_governance.py`.

---

## Environment Variables Reference

> [!IMPORTANT]
> **Security Note**: **NEVER commit `.env` files to version control.** All sensitive credentials must be loaded from environment variables via `SecretManager` or `get_env()`.

### Complete Environment Variables List

All API keys, secrets, and configuration values must be stored in `.env` file. Below is the complete list organized by category:

#### Market Data APIs
- `ALPHA_VANTAGE_API_KEY` - Alpha Vantage API key for market data
- `POLYGON_API_KEY` - Polygon.io API key
- `FRED_API_KEY` - Federal Reserve Economic Data API key
- `QUANDL_API_KEY` - Quandl/Nasdaq Data Link API key
- `FINNHUB_API_KEY` - Finnhub API key
- `NEWSAPI_API_KEY` - NewsAPI.org API key

#### Brokerage APIs
- `ALPACA_API_KEY` - Alpaca trading API key
- `ALPACA_SECRET_KEY` - Alpaca trading API secret
- `ALPACA_BASE_URL` - Alpaca base URL (default: `https://paper-api.alpaca.markets`)

#### Interactive Brokers (IBKR)
- `IBKR_GATEWAY_HOST` - IBKR Gateway host (default: `127.0.0.1`)
- `IBKR_GATEWAY_PORT` - IBKR Gateway port (default: `7497`)
- `IBKR_CLIENT_ID` - IBKR client ID (default: `1`)
- `IBKR_USERNAME` - IBKR account username
- `IBKR_PASSWORD` - IBKR account password

#### Robinhood
- `ROBINHOOD_USERNAME` - Robinhood account username
- `ROBINHOOD_PASSWORD` - Robinhood account password
- `ROBINHOOD_TOTP` - Robinhood TOTP secret for MFA

#### Crypto APIs
- `COINBASE_API_KEY` - Coinbase Cloud API key
- `COINBASE_API_SECRET` - Coinbase Cloud API secret
- `COINBASE_BASE_URL` - Coinbase API base URL (default: `https://api.coinbase.com/api/v3/brokerage`)
- `ETH_RPC_URL` - Ethereum RPC endpoint (default: `https://cloudflare-eth.com`)
- `SOL_RPC_URL` - Solana RPC endpoint (default: `https://api.mainnet-beta.solana.com`)

#### Social & Sentiment APIs
- `STOCKTWITS_ACCESS_TOKEN` - StockTwits API access token
- `STOCKTWITS_BASE_URL` - StockTwits API base URL (default: `https://api.stocktwits.com/api/2`)
- `DISCORD_BOT_TOKEN` - Discord bot token for community monitoring
- `DISCORD_MONITORED_CHANNELS` - Comma-separated list of channels (default: `#general,#trading-floor,#alpha-sigs`)
- `YOUTUBE_API_KEY` - YouTube Data API v3 key
- `REDDIT_CLIENT_ID` - Reddit API client ID
- `REDDIT_CLIENT_SECRET` - Reddit API client secret
- `REDDIT_USER_AGENT` - Reddit user agent string (default: `ai_investor_v1`)
- `TWITTER_BEARER_TOKEN` - Twitter/X API bearer token

#### AI/LLM APIs
- `OPENAI_API_KEY` - OpenAI API key for GPT models
- `ANTHROPIC_API_KEY` - Anthropic Claude API key
- `GEMINI_API_KEY` - Google Gemini API key
- `PERPLEXITY_API_KEY` - Perplexity API key

#### Payment & Banking
- `STRIPE_SECRET_KEY` - Stripe secret key
- `STRIPE_WEBHOOK_SECRET` - Stripe webhook signing secret
- `STRIPE_PRICE_PRO` - Stripe Pro plan price ID
- `STRIPE_PRICE_INST` - Stripe Institutional plan price ID
- `PAYPAL_CLIENT_ID` - PayPal client ID
- `PAYPAL_CLIENT_SECRET` - PayPal client secret
- `SQUARE_ACCESS_TOKEN` - Square API access token
- `PLAID_CLIENT_ID` - Plaid client ID
- `PLAID_SECRET` - Plaid secret key
- `PLAID_ENV` - Plaid environment (default: `sandbox`)

#### Google Services
- `GOOGLE_CLIENT_ID` - Google OAuth client ID
- `GOOGLE_CLIENT_SECRET` - Google OAuth client secret
- `GOOGLE_REDIRECT_URI` - Google OAuth redirect URI

#### Facebook/Meta
- `FACEBOOK_APP_ID` - Facebook App ID
- `FACEBOOK_APP_SECRET` - Facebook App Secret

#### Tax & Compliance
- `TAXBIT_API_KEY` - TaxBit API key
- `TAXBIT_CLIENT_ID` - TaxBit OAuth client ID
- `TAXBIT_CLIENT_SECRET` - TaxBit OAuth client secret
- `TAXBIT_BASE_URL` - TaxBit API base URL (default: `https://api.taxbit.com/v1`)

#### Storage
- `AWS_ACCESS_KEY_ID` - AWS access key for S3
- `AWS_SECRET_ACCESS_KEY` - AWS secret key for S3
- `AWS_S3_BUCKET` - S3 bucket name
- `AWS_REGION` - AWS region (default: `us-east-1`)

#### Philanthropy
- `GIVINGBLOCK_API_KEY` - The Giving Block API key
- `GIVINGBLOCK_CRYPTO_ADDRESS` - Crypto donation address (⚠️ **Was hardcoded, now uses env**)
- `CHARITYNAV_APP_ID` - Charity Navigator app ID
- `CHARITYNAV_APP_KEY` - Charity Navigator app key

#### Communication
- `TWILIO_ACCOUNT_SID` - Twilio account SID
- `TWILIO_AUTH_TOKEN` - Twilio auth token
- `SENDGRID_API_KEY` - SendGrid API key
- `SLACK_WEBHOOK_URL` - Slack webhook URL for alerts
- `PAGERDUTY_ROUTING_KEY` - PagerDuty routing key

#### Infrastructure
- `DATABASE_URL` - PostgreSQL connection string
- `POSTGRES_HOST` - PostgreSQL host (default: `localhost`)
- `POSTGRES_PORT` - PostgreSQL port (default: `5432`)
- `POSTGRES_USER` - PostgreSQL user (default: `postgres`)
- `POSTGRES_PASSWORD` - PostgreSQL password (default: `postgres`)
- `POSTGRES_DB` - PostgreSQL database name (default: `ai_investor`)
- `NEO4J_URI` - Neo4j connection URI (default: `bolt://localhost:7687`)
- `NEO4J_USER` - Neo4j username (default: `neo4j`)
- `NEO4J_PASSWORD` - Neo4j password (default: `password`)
- `REDIS_URL` - Redis connection URL (default: `redis://localhost:6379/0`)
- `REDIS_HOST` - Redis host (default: `localhost`)
- `REDIS_PORT` - Redis port (default: `6379`)
- `REDIS_DB` - Redis database number (default: `0`)
- `REDIS_PASSWORD` - Redis password (optional)
- `KAFKA_BOOTSTRAP_SERVERS` - Kafka bootstrap servers (default: `localhost:9092`)

#### Security
- `JWT_SECRET` - JWT signing secret (⚠️ **Change in production**)
- `SECRET_KEY` - Flask secret key (⚠️ **Change in production**)
- `ENCRYPTION_MASTER_KEY` - Master key for API key encryption (⚠️ **Change in production**)

#### Application Configuration
- `APP_NAME` - Application name (default: `AI Investor`)
- `APP_ENV` - Environment (`development`, `staging`, `production`)
- `DEBUG` - Debug mode (default: `true`)
- `LOG_LEVEL` - Logging level (default: `INFO`)
- `LOGS_DIR` - Logs directory path
- `FRONTEND_URL` - Frontend URL for redirects (default: `http://localhost:5173`)
- `PORT` - Server port (default: `5050`)
- `FLASK_ENV` - Flask environment

#### Observability
- `OTLP_ENDPOINT` - OpenTelemetry endpoint (default: `http://localhost:4317`)
- `SERVICE_NAME` - Service name for tracing (default: `ai-investor-backend`)

#### Feature Flags
- `LITE_MODE` - Enable lite mode for resource-constrained environments
- `WS_SCALE_ENABLED` - Enable WebSocket scaling
- `CHAOS_ENABLED` - Enable chaos engineering tests

#### Regulatory
- `USER_AGENT_EMAIL` - SEC EDGAR compliance email (required for SEC API access)

---

## 🔍 Security Audit: Hardcoded Values Fixed

### ✅ Fixed Issues (2026-01-21)

1. **Hardcoded Wallet Address** (`services/philanthropy/charity_client.py`)
   - **Before**: `"crypto_address": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"`
   - **After**: Uses `GIVINGBLOCK_CRYPTO_ADDRESS` from environment
   - **Note**: Fallback address remains for mock mode only

2. **IBKR Client** (`services/brokerage/ibkr_client.py`)
   - **Before**: Hardcoded `host='127.0.0.1'`, `port=7497`
   - **After**: Uses `IBKR_GATEWAY_HOST`, `IBKR_GATEWAY_PORT` from env

3. **Ethereum Client** (`services/crypto/ethereum_client.py`)
   - **Before**: Hardcoded `rpc_url="https://cloudflare-eth.com"`
   - **After**: Uses `ETH_RPC_URL` from env

4. **Solana Client** (`services/crypto/solana_client.py`)
   - **Before**: Hardcoded `rpc_url="https://api.mainnet-beta.solana.com"`
   - **After**: Uses `SOL_RPC_URL` from env

5. **Coinbase Client** (`services/crypto/coinbase_client.py`)
   - **Before**: Optional `api_key`/`api_secret` parameters
   - **After**: Loads from `COINBASE_API_KEY`, `COINBASE_API_SECRET` if not provided

6. **StockTwits Client** (`services/social/stocktwits_client.py`)
   - **Before**: Optional `access_token` parameter
   - **After**: Loads from `STOCKTWITS_ACCESS_TOKEN` if not provided

7. **Discord Bot** (`services/social/discord_bot.py`)
   - **Before**: Optional `bot_token` parameter, hardcoded channels
   - **After**: Loads from `DISCORD_BOT_TOKEN` and `DISCORD_MONITORED_CHANNELS`

8. **YouTube Client** (`services/social/youtube_client.py`)
   - **Before**: Optional `api_key` parameter
   - **After**: Loads from `YOUTUBE_API_KEY` if not provided

9. **TaxBit Client** (`services/taxes/taxbit_service.py`)
   - **Before**: Optional `api_key` parameter
   - **After**: Loads from `TAXBIT_API_KEY`, `TAXBIT_CLIENT_ID`, `TAXBIT_CLIENT_SECRET`

10. **IBKR Gateway Manager** (`services/brokerage/ibkr_gateway_manager.py`)
    - **Before**: Required `username`/`password` parameters
    - **After**: Loads from `IBKR_USERNAME`, `IBKR_PASSWORD` if not provided

### ✅ Public Addresses (No Change Needed)

These are **public contract addresses** and are safe to hardcode:
- **Ethereum Token Contracts**: USDT (`0xdAC17F958D2ee523a2206206994597C13D831ec7`), USDC (`0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`), WBTC (`0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599`), LINK (`0x514910771AF9Ca656af840dff83E8264EcF986CA`)
- **Solana Token Mints**: USDC (`EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`), USDT (`Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB`), BONK (`DezXAZ8z7PnrnMcqzR2S6Pb9k8i6yT2ccWU6Ykcr98J3`), SOL (`So11111111111111111111111111111111111111112`)

### ✅ Test Files (No Change Needed)

Test files may contain hardcoded values for testing purposes:
- `tests/test_*.py` - Mock credentials for testing
- `scripts/runners/test_*.py` - Test runner scripts

---

## 📝 Usage Examples

### Using SecretManager (Recommended)
```python
from services.system.secret_manager import get_secret_manager

sm = get_secret_manager()
api_key = sm.get_secret('ALPHA_VANTAGE_API_KEY')
```

### Using get_env from utils.core.config
```python
from utils.core.config import get_env

api_key = get_env('ALPHA_VANTAGE_API_KEY', required=True)
```

### Using config.environment_manager
```python
from config.environment_manager import get_settings

settings = get_settings()
api_key = settings.ALPHA_VANTAGE_API_KEY
```

---

## ⚠️ Security Checklist

- [x] All API keys load from environment variables
- [x] No hardcoded credentials in production code
- [x] Hardcoded wallet address moved to environment variable
- [x] All services use `SecretManager` or `get_env()`
- [x] Test files excluded from security audit
- [x] Public contract addresses documented as safe

---

**Last Updated**: 2026-01-21
**Security Audit Completed**: 2026-01-21