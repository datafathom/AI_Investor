"""
==============================================================================
AI Investor - Web API Gateway
==============================================================================
PURPOSE:
    Main entry point for the Flask/FastAPI backend. Exposes REST endpoints
    for the Mission Control Dashboard and orchestrates agent communication.

ARCHITECTURE:
    - Connects to Kafka for real-time event streaming
    - Interfaces with Postgres (TimescaleDB) for time-series data
    - Interfaces with Neo4j for graph-based dependency mapping
==============================================================================
"""
import os
import sys
print("DEBUG: app.py TOP LEVEL START")
from pathlib import Path

# Add project root to Python path
_project_root = Path(__file__).parent.parent
sys.path.insert(0, str(_project_root))

from flask import Flask, jsonify, request
from flask_cors import CORS


print("Importing dashboard_api...")

# --- ABSOLUTE CONSOLIDATED IMPORTS ---
from web.api.advanced_orders_api import advanced_orders_bp
from web.api.advanced_orders_api import execution_bp
from web.api.advanced_risk_api import advanced_risk_bp
from web.api.ai_assistant_api import ai_assistant_bp
from web.api.ai_autocoder_api import ai_autocoder_bp
from web.api.autocoder_api import autocoder_bp
from web.api.ai_predictions_api import ai_predictions_bp
from web.api.analytics_api import analytics_bp
from web.api.assets_api import assets_bp
from web.api.attribution_api import attribution_bp
from web.api.auth_api import auth_bp
from web.api.banking_api import banking_bp
from web.api.billing_api import billing_bp
from web.api.binance_api import binance_bp
from web.api.briefing_api import briefing_bp
from web.api.brokerage_api import brokerage_bp
from web.api.budgeting_api import budgeting_bp
from web.api.calendar_api import calendar_bp
from web.api.cash_api_flask import cash_bp
from web.api.charting_api import charting_bp
from web.api.coinbase_api import coinbase_bp
from web.api.coinbase_crypto_api import coinbase_crypto_bp
from web.api.communication_api import communication_bp
from web.api.community_api import forum_bp
from web.api.community_api import qa_bp
from web.api.compliance_api import compliance_bp
from web.api.credit_api import credit_bp
from web.api.crypto_api import crypto_api_bp
from web.api.dashboard_api import dashboard_bp
from web.api.debate_api import debate_bp
from web.api.discord_api import discord_bp
from web.api.docs_api import docs_bp
from web.api.documents_api import documents_bp
from web.api.education_api import education_bp
from web.api.email_api import email_api_bp
from web.api.enterprise_api import enterprise_bp
from web.api.estate_api import estate_bp
from web.api.ethereum_api import ethereum_bp
from web.api.evolution_api import evolution_bp
from web.api.facebook_auth_api import facebook_auth_bp
from web.api.facebook_hype_api import facebook_hype_bp
from web.api.financial_planning_api import financial_planning_bp
from web.api.fixed_income_api import fixed_income_bp
from web.api.gmail_api import gmail_bp
from web.api.google_auth_api import google_auth_bp
from web.api.health_api import health_bp
from web.api.homeostasis_api import homeostasis_api
from web.api.ibkr_api import ibkr_bp
from web.api.identity_api import identity_api
from web.api.incident_api import incident_api_bp
from web.api.institutional_api import institutional_bp
from web.api.integration_api import integration_bp
from web.api.kyc_api_flask import kyc_bp
from web.api.legal_api import legal_bp
from web.api.macro_api import macro_bp
from web.api.macro_data_api import macro_data_bp
from web.api.market_data_api import market_data_bp
from web.api.marketplace_api import marketplace_bp
from web.api.ml_training_api import ml_training_bp
from web.api.news_api import news_bp
from web.api.optimization_api import optimization_bp
from web.api.onboarding_api import onboarding_bp
from web.api.options_api import options_bp
from web.api.paper_trading_api import paper_trading_bp
from web.api.paper_trading_api import simulation_bp
from web.api.paypal_api import paypal_bp
from web.api.plaid_api import plaid_bp
from web.api.politics_api import politics_bp
from web.api.privacy_api import privacy_bp
from web.api.public_api_endpoints import public_api_bp
from web.api.research_api import research_bp
from web.api.risk_api import risk_bp
from web.api.retirement_api import retirement_bp
from web.api.robinhood_api import robinhood_bp
from web.api.settlement_api import settlement_bp
from web.api.social_api import social_bp
from web.api.social_trading_api import social_trading_bp
from web.api.solana_api import solana_bp
from web.api.spatial_api import spatial_bp
from web.api.square_api import square_bp
from web.api.stocktwits_api import stocktwits_bp
from web.api.strategy_api import strategy_bp
from web.api.stripe_api import stripe_bp
from web.api.tax_api import tax_api_bp
from web.api.tax_optimization_api import tax_optimization_bp
from web.api.taxbit_api import taxbit_bp
from web.api.twilio_api import twilio_api_bp
from web.api.venmo_api import venmo_bp
from web.api.watchlist_api import alert_bp
from web.api.watchlist_api import watchlist_bp
from web.api.wave_apis import backtest_bp, corporate_bp, integrations_bp, margin_bp, mobile_bp, philanthropy_bp, scenario_bp, system_bp, zen_bp
from web.api.web3_api import web3_bp
from web.api.workspace_api import workspace_bp
from web.api.youtube_api import youtube_bp
from web.api.payment_transfer_api import payment_transfer_bp
from web.routes.market_routes import market_bp
from web.routes.system_routes import system_bp as system_routes_bp
# --- FINISHED CONSOLIDATION ---

# from web.api.dashboard_api import dashboard_bp
# from web.api.communication_api import communication_bp
# from web.api.politics_api import politics_bp
# from web.api.evolution_api import evolution_bp
# from web.api.debate_api import debate_bp
# from web.api.autocoder_api import autocoder_bp
# from web.api.ai_autocoder_api import ai_autocoder_bp
# from web.api.spatial_api import spatial_bp
# print("Importing risk_api...")
# # from web.api.risk_api import risk_bp
# print("Importing assets_api...")
# # from web.api.assets_api import assets_bp
# print("Importing attribution_api...")
# # from web.api.attribution_api import attribution_bp
# print("Importing analytics_api...")
# # from web.api.analytics_api import analytics_bp
# print("Importing optimization_api...")
# # from web.api.optimization_api import optimization_bp
# print("Importing advanced_risk_api...")
# # from web.api.advanced_risk_api import advanced_risk_bp
# print("Importing tax_optimization_api...")
# # from web.api.tax_optimization_api import tax_optimization_bp
# print("Importing charting_api...")
# # from web.api.charting_api import charting_bp
# from web.api.options_api import options_bp
# from web.api.financial_planning_api import financial_planning_bp
# from web.api.retirement_api import retirement_bp
# from web.api.estate_api import estate_bp
# from web.api.budgeting_api import budgeting_bp
# print("Importing billing_api...")
# # from web.api.billing_api import billing_bp  # Imported inside create_app()
# from web.api.credit_api import credit_bp
# from web.api.advanced_orders_api import advanced_orders_bp, execution_bp
# from web.api.paper_trading_api import paper_trading_bp, simulation_bp
# from web.api.strategy_api import strategy_bp
# from web.api.news_api import news_bp
# from web.api.watchlist_api import watchlist_bp, alert_bp
# print("Importing research_api...")
# # from web.api.research_api import research_bp  # Imported inside create_app()
# from web.api.social_trading_api import social_trading_bp
# from web.api.community_api import forum_bp, qa_bp
# from web.api.education_api import education_bp
# from web.api.ai_predictions_api import ai_predictions_bp
# from web.api.ai_assistant_api import ai_assistant_bp
# from web.api.enterprise_api import enterprise_bp
# from web.api.compliance_api import compliance_bp
# from web.api.institutional_api import institutional_bp
# from web.api.public_api_endpoints import public_api_bp
# from web.api.ml_training_api import ml_training_bp
# from web.api.integration_api import integration_bp
# from web.api.marketplace_api import marketplace_bp
# from web.api.fixed_income_api import fixed_income_bp
# from web.api.web3_api import web3_bp
# from web.api.macro_api import macro_bp
print("Importing Phase 54-68 APIs...")
# from web.api.kyc_api_flask import kyc_bp
# from web.api.cash_api_flask import cash_bp
# from web.api.wave_apis import (
#     backtest_bp, estate_bp, compliance_bp, scenario_bp, 
#     philanthropy_bp, system_bp, corporate_bp, margin_bp, 
#     mobile_bp, integrations_bp, zen_bp
# )
# from web.api.news_api import news_bp
print("Importing tenant_middleware...")
from web.middleware.tenant_middleware import init_tenant_middleware
print("DONE importing everything")


def create_app() -> Flask:
    """
    Application factory pattern for Flask app.
    
    Returns:
        Flask: Configured Flask application instance.
    """
    print("DEBUG: create_app() started")
    app = Flask(__name__)
    print("DEBUG: Flask instance created")
    
    # Initialize error tracking
    from services.monitoring.error_tracker import get_error_tracker
    error_tracker = get_error_tracker()
    if error_tracker.is_enabled():
        print("[OK] Error tracking initialized (Sentry)")
    
    # Initialize performance middleware
    from web.middleware.performance_middleware import performance_monitor, compress_response, enable_cors_optimization
    from web.middleware.rate_limiter import RateLimiter
    performance_monitor(app)
    compress_response(app)
    enable_cors_optimization(app)
    print("[OK] Performance middleware initialized")
    
    # Initialize security middleware
    from web.middleware.security_middleware import security_headers, require_https
    
    # Initialize rate limiter
    rate_limiter = RateLimiter()
    app.config['RATE_LIMITER'] = rate_limiter
    security_headers(app)
    if os.getenv('APP_ENV') == 'production':
        require_https(app)
    print("[OK] Security middleware initialized")
    
    # Load configuration from environment
    app.config['DEBUG'] = os.getenv('FLASK_ENV', 'development') == 'development'
    
    # Health check endpoints (basic - for load balancer)
    @app.route('/health', methods=['GET'])
    @app.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint for container orchestration."""
        return jsonify({
            'status': 'healthy',
            'service': 'ai-investor-backend'
        })
    
    # Enhanced health check endpoints
    # from web.api.health_api import health_bp # ABSOLUTE STRIP
    app.register_blueprint(health_bp)
    
    @app.route('/api/v1/gap', methods=['GET'])
    def get_gap():
        """
        Returns 'The Gap' - the discrepancy between current Stock and Set Point.
        This is the primary metric for the balancing feedback loop.
        """
        # TODO: Implement actual Stock/SetPoint calculation
        return jsonify({
            'stock': 100000.00,
            'set_point': 100000.00,
            'gap': 0.00,
            'gap_percent': 0.0
        })
    
    @app.route('/api/v1/market/predict', methods=['GET'])
    def get_market_prediction():
        """
        Get directional prediction for a symbol.
        Params:
            symbol: string (default SPY)
        """
        symbol = request.args.get('symbol', 'SPY').upper()
        # In a real scenario, we would fetch data for 'symbol' here.
        # For now, we utilize the mock/synthetic data generation within the endpoint or service wrapper
        # to demonstrate feasibility, as fetching live OHLCV might require the ingestion pipeline (Phase 6).
        
        from services.analysis.prediction_service import get_prediction_service
        import pandas as pd
        import numpy as np
        
        # Mock Data Generation for Prediction
        # TODO: Replace with fetch from MarketDataService when linked
        dates = pd.date_range(end=pd.Timestamp.now(), periods=100, freq='1D')
        df = pd.DataFrame(index=dates)
        df['open'] = 100 + np.random.randn(100).cumsum()
        df['high'] = df['open'] + 1
        df['low'] = df['open'] - 1
        df['close'] = df['open'] + np.random.randn(100) * 0.5
        df['volume'] = 1000
        
        service = get_prediction_service()
        
        # Ensure model is trained (for demo purposes, train on fly if needed)
        try:
            if service.model is None:
                 service.train_model(df)
                 
            result = service.predict_direction(df)
            result['symbol'] = symbol
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    
    # Register Blueprints
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(communication_bp)
    app.register_blueprint(politics_bp)
    app.register_blueprint(evolution_bp)
    # app.register_blueprint(debate_bp)  # Registered later with URL prefix at Phase 9
    app.register_blueprint(autocoder_bp)
    
    # Phase 7: AI Autocoder API (OpenAI-powered code generation)
    # # from web.api.ai_autocoder_api import ai_autocoder_bp # ABSOLUTE STRIP
    app.register_blueprint(ai_autocoder_bp)
    
    # Phase 33: Documents API (AWS S3 storage)
    # from web.api.documents_api import documents_bp # ABSOLUTE STRIP
    app.register_blueprint(documents_bp)
    
    # Phase 17: Google OAuth API
    # from web.api.google_auth_api import google_auth_bp # ABSOLUTE STRIP
    app.register_blueprint(google_auth_bp)
    
    # Phase 18: Gmail API
    # from web.api.gmail_api import gmail_bp # ABSOLUTE STRIP
    app.register_blueprint(gmail_bp)
    
    # Phase 19: Google Calendar API
    # from web.api.calendar_api import calendar_bp # ABSOLUTE STRIP
    app.register_blueprint(calendar_bp)
    
    # Phase 14: Square API
    # from web.api.square_api import square_bp # ABSOLUTE STRIP
    # app.register_blueprint(square_bp) # REMOVED DUPLICATE REGISTRATION
    
    # Phase 15: Plaid API
    # from web.api.plaid_api import plaid_bp # ABSOLUTE STRIP
    # app.register_blueprint(plaid_bp) # REMOVED DUPLICATE REGISTRATION
    
    # Phase 16: Facebook OAuth & Hype API
    # from web.api.facebook_auth_api import facebook_auth_bp # ABSOLUTE STRIP
    app.register_blueprint(facebook_auth_bp)
    # from web.api.facebook_hype_api import facebook_hype_bp # ABSOLUTE STRIP
    app.register_blueprint(facebook_hype_bp)
    
    # Phase 22: Interactive Brokers API
    # from web.api.ibkr_api import ibkr_bp # ABSOLUTE STRIP
    app.register_blueprint(ibkr_bp)
    
    # Phase 23: Robinhood API
    # from web.api.robinhood_api import robinhood_bp # ABSOLUTE STRIP
    app.register_blueprint(robinhood_bp)
    
    # Phase 24: Ethereum API
    # from web.api.ethereum_api import ethereum_bp # ABSOLUTE STRIP
    app.register_blueprint(ethereum_bp)
    
    # Phase 25: Solana API
    # from web.api.solana_api import solana_bp # ABSOLUTE STRIP
    app.register_blueprint(solana_bp)
    
    # Phase 26: Coinbase Crypto API
    # from web.api.coinbase_crypto_api import coinbase_crypto_bp # ABSOLUTE STRIP
    app.register_blueprint(coinbase_crypto_bp)
    
    # Phase 27: StockTwits API
    # from web.api.stocktwits_api import stocktwits_bp # ABSOLUTE STRIP
    app.register_blueprint(stocktwits_bp)
    
    # Phase 28: Discord API
    # from web.api.discord_api import discord_bp # ABSOLUTE STRIP
    app.register_blueprint(discord_bp)
    
    # Phase 29: YouTube API
    # from web.api.youtube_api import youtube_bp # ABSOLUTE STRIP
    app.register_blueprint(youtube_bp)
    
    # Phase 32: TaxBit API
    # # from web.api.taxbit_api import taxbit_bp # ABSOLUTE STRIP
    app.register_blueprint(taxbit_bp)
    app.register_blueprint(spatial_bp)
    # app.register_blueprint(assets_bp, url_prefix='/api/v1/assets')
    # app.register_blueprint(attribution_bp, url_prefix='/api/v1/attribution')
    # app.register_blueprint(analytics_bp)  # Phase 1: Advanced Portfolio Analytics
    # app.register_blueprint(optimization_bp)  # Phase 2: Portfolio Optimization & Rebalancing
    # app.register_blueprint(advanced_risk_bp)  # Phase 3: Advanced Risk Management & Stress Testing
    # app.register_blueprint(tax_optimization_bp)  # Phase 4: Tax-Loss Harvesting & Optimization
    # app.register_blueprint(charting_bp)  # Phase 5: Advanced Charting & Technical Analysis
    app.register_blueprint(options_bp)  # Phase 6: Options Strategy Builder & Analyzer
    app.register_blueprint(financial_planning_bp)  # Phase 7: Financial Planning & Goal Tracking
    app.register_blueprint(retirement_bp)  # Phase 8: Retirement Planning & Projection
    # app.register_blueprint(estate_bp)  # Phase 9: Estate Planning & Inheritance Tools # REMOVED DUPLICATE REGISTRATION
    app.register_blueprint(budgeting_bp)  # Phase 10: Budgeting & Expense Tracking
    # app.register_blueprint(billing_bp)  # Phase 11: Registered later at Phase 14
    app.register_blueprint(credit_bp)  # Phase 12: Credit Score Monitoring & Improvement
    app.register_blueprint(advanced_orders_bp)  # Phase 13: Advanced Order Types & Execution
    app.register_blueprint(execution_bp)  # Phase 13: Smart Execution Engine
    app.register_blueprint(paper_trading_bp)  # Phase 14: Paper Trading & Simulation
    app.register_blueprint(simulation_bp)  # Phase 14: Simulation Service
    app.register_blueprint(strategy_bp)  # Phase 15: Algorithmic Trading & Strategy Automation
    # app.register_blueprint(news_bp)  # Phase 16: News & Sentiment Analysis # REMOVED DUPLICATE REGISTRATION
    app.register_blueprint(watchlist_bp)  # Phase 17: Watchlists & Price Alerts
    app.register_blueprint(alert_bp)  # Phase 17: Alert System
    # app.register_blueprint(research_bp)  # Phase 18: Registered later at Phase 11
    app.register_blueprint(social_trading_bp)  # Phase 19: Social Trading & Copy Trading
    app.register_blueprint(forum_bp)  # Phase 20: Community Forums & Discussion
    app.register_blueprint(qa_bp)  # Phase 20: Expert Q&A System
    # app.register_blueprint(education_bp)  # Phase 21: Investment Education & Learning Platform # REMOVED DUPLICATE REGISTRATION
    app.register_blueprint(ai_predictions_bp)  # Phase 25: Advanced AI Predictions & Forecasting
    app.register_blueprint(ai_assistant_bp)  # Phase 26: Personalized AI Assistant
    app.register_blueprint(enterprise_bp)  # Phase 31: Enterprise Features & Multi-User Support
    # app.register_blueprint(compliance_bp)  # Phase 32: Advanced Compliance & Reporting # REMOVED DUPLICATE REGISTRATION
    app.register_blueprint(institutional_bp)  # Phase 33: Institutional & Professional Tools
    app.register_blueprint(public_api_bp)  # Phase 29: Public API & Developer Platform
    app.register_blueprint(ml_training_bp)  # Phase 27: Machine Learning Model Training Pipeline
    app.register_blueprint(integration_bp)  # Phase 28: Third-Party App Integrations
    app.register_blueprint(marketplace_bp)  # Phase 30: Marketplace & Extensions
    app.register_blueprint(fixed_income_bp, url_prefix='/api/v1/fixed-income')
    app.register_blueprint(web3_bp, url_prefix='/api/v1/web3')
    # app.register_blueprint(tax_bp, url_prefix='/api/v1/tax') # REMOVED: Duplicate/Broken registration

    app.register_blueprint(macro_bp, url_prefix='/api/v1/macro')
    
    # Initialize middleware
    init_tenant_middleware(app)
    
    # from web.api.homeostasis_api import homeostasis_api # ABSOLUTE STRIP
    app.register_blueprint(homeostasis_api, url_prefix='/api/v1/homeostasis')
    app.register_blueprint(risk_bp, url_prefix='/api/v1/risk')
    

    # # from web.api.auth_api import auth_bp # ABSOLUTE STRIP
    # # from web.api.privacy_api import privacy_bp # ABSOLUTE STRIP
    # # from web.api.legal_api import legal_bp # ABSOLUTE STRIP
    # # from web.api.workspace_api import workspace_bp # ABSOLUTE STRIP
    app.register_blueprint(auth_bp)
    app.register_blueprint(privacy_bp)
    # app.register_blueprint(legal_bp) # REMOVED DUPLICATE REGISTRATION
    app.register_blueprint(workspace_bp)

    # --- Phase 23 & 24: Observability ---
    from services.system.tracing_service import get_tracing_service
    from services.system.logging_service import get_logging_service
    get_tracing_service().initialize(app)
    get_logging_service().initialize()

    # --- Phase 07: Security Gateway ---
    from services.system.security_gateway import limiter, get_security_gateway
    limiter.init_app(app)
    # Optionally store the service in app config if needed
    app.config['SECURITY_GATEWAY'] = get_security_gateway()

    # UI Phase 54-68 registration
    app.register_blueprint(kyc_bp, url_prefix='/api/v1/kyc')
    app.register_blueprint(cash_bp, url_prefix='/api/v1/cash')
    app.register_blueprint(backtest_bp, url_prefix='/api/v1/backtest')
    app.register_blueprint(estate_bp, url_prefix='/api/v1/estate')
    app.register_blueprint(compliance_bp, url_prefix='/api/v1/compliance')
    app.register_blueprint(scenario_bp, url_prefix='/api/v1/scenario')
    app.register_blueprint(philanthropy_bp, url_prefix='/api/v1/philanthropy')
    app.register_blueprint(system_bp, url_prefix='/api/v1/system')
    app.register_blueprint(corporate_bp, url_prefix='/api/v1/corporate')
    app.register_blueprint(margin_bp, url_prefix='/api/v1/margin')
    app.register_blueprint(mobile_bp, url_prefix='/api/v1/mobile')
    app.register_blueprint(integrations_bp, url_prefix='/api/v1/integrations')
    app.register_blueprint(zen_bp, url_prefix='/api/v1/homeostasis') # Matching the store's expectation
    
    # Phase 4 API Integration: Quandl
    # (Already registered in market_data_api)

    # Phase 5 API Integration: Finnhub
    # (Already registered in corporate_bp via wave_apis or similar)

    # Phase 6 API Integration: NewsAPI
    app.register_blueprint(news_bp, url_prefix='/api/v1/news')
    
    # Phase 1 API Integration: Market Data
    # from web.api.market_data_api import market_data_bp # ABSOLUTE STRIP
    app.register_blueprint(market_data_bp, url_prefix='/api/v1/market')
    
    # Phase 2 API Integration: FRED Macro Data
    # from web.api.macro_data_api import macro_data_bp # ABSOLUTE STRIP
    app.register_blueprint(macro_data_bp, url_prefix='/api/v1/macro-data')
    
    # Phase 01: Education API
    # # from web.api.education_api import education_bp # ABSOLUTE STRIP
    app.register_blueprint(education_bp, url_prefix='/api/v1/education')

    # Phase 2: Market & System Routes
    # from web.routes.market_routes import market_bp # ABSOLUTE STRIP
    app.register_blueprint(market_bp)
    
    # from web.routes.system_routes import system_bp as system_routes_bp # ABSOLUTE STRIP
    app.register_blueprint(system_routes_bp)

    # Phase 10: Banking API
    # # from web.api.banking_api import banking_bp # ABSOLUTE STRIP
    app.register_blueprint(banking_bp)

    # Phase 12: Brokerage API
    # # from web.api.brokerage_api import brokerage_bp # ABSOLUTE STRIP
    app.register_blueprint(brokerage_bp)

    # Phase 14: Billing API
    # # from web.api.billing_api import billing_bp # ABSOLUTE STRIP
    app.register_blueprint(billing_bp)

    # Phase 15: Crypto API
    # from web.api.crypto_api import crypto_api_bp # ABSOLUTE STRIP
    app.register_blueprint(crypto_api_bp)

    # Phase 16: Settlement API
    # from web.api.settlement_api import settlement_bp # ABSOLUTE STRIP
    app.register_blueprint(settlement_bp)

    # Phase 14: Identity API
    # from web.api.identity_api import identity_api # ABSOLUTE STRIP
    app.register_blueprint(identity_api, url_prefix='/api/v1/identity')

    # Phase 8: Social API (Reddit/Sentiment)
    # # from web.api.social_api import social_bp # ABSOLUTE STRIP
    app.register_blueprint(social_bp, url_prefix='/api/v1/social')

    # Phase 9: AI Debate API (Anthropic)
    # # from web.api.debate_api import debate_bp # ABSOLUTE STRIP
    app.register_blueprint(debate_bp, url_prefix='/api/v1/ai')

    # Phase 10: AI Briefing API (Gemini)
    # from web.api.briefing_api import briefing_bp # ABSOLUTE STRIP
    app.register_blueprint(briefing_bp, url_prefix='/api/v1/ai')

    # Phase 11: AI Research API (Perplexity)
    # # from web.api.research_api import research_bp # ABSOLUTE STRIP
    app.register_blueprint(research_bp, url_prefix='/api/v1/ai')

    # Phase 12: Billing API (Stripe)
    # from web.api.stripe_api import stripe_bp # ABSOLUTE STRIP
    app.register_blueprint(stripe_bp, url_prefix='/api/v1')

    # Phase 13: PayPal API
    # # from web.api.paypal_api import paypal_bp # ABSOLUTE STRIP
    app.register_blueprint(paypal_bp, url_prefix='/api/v1')

    # Phase 14: Venmo API
    # # from web.api.venmo_api import venmo_bp # ABSOLUTE STRIP
    app.register_blueprint(venmo_bp, url_prefix='/api/v1')

    # Phase 15: Square API
    # # from web.api.square_api import square_bp # ABSOLUTE STRIP
    app.register_blueprint(square_bp, url_prefix='/api/v1')

    # Phase 16: Plaid API
    # # from web.api.plaid_api import plaid_bp # ABSOLUTE STRIP
    app.register_blueprint(plaid_bp, url_prefix='/api/v1')

    # Phase 17: Coinbase API
    # # from web.api.coinbase_api import coinbase_bp # ABSOLUTE STRIP
    app.register_blueprint(coinbase_bp, url_prefix='/api/v1')

    # Phase 18: Binance API
    # # from web.api.binance_api import binance_bp # ABSOLUTE STRIP
    app.register_blueprint(binance_bp, url_prefix='/api/v1')

    # Phase 19: Tax API
    # # from web.api.tax_api import tax_api_bp # ABSOLUTE STRIP
    app.register_blueprint(tax_api_bp, url_prefix='/api/v1')

    # Phase 20: Twilio API
    # # from web.api.twilio_api import twilio_api_bp # ABSOLUTE STRIP
    app.register_blueprint(twilio_api_bp, url_prefix='/api/v1')

    # Phase 21: SendGrid API
    # # from web.api.email_api import email_api_bp # ABSOLUTE STRIP
    app.register_blueprint(email_api_bp, url_prefix='/api/v1')

    # Phase 22: PagerDuty API
    # # from web.api.incident_api import incident_api_bp # ABSOLUTE STRIP
    app.register_blueprint(incident_api_bp, url_prefix='/api/v1')
    
    # Legal Documents API
    # from web.api.legal_api import legal_bp # ABSOLUTE STRIP
    app.register_blueprint(legal_bp)
    
    # API Documentation
    # from web.api.docs_api import docs_bp # ABSOLUTE STRIP
    app.register_blueprint(docs_bp)
    
    # Onboarding API
    # from web.api.onboarding_api import onboarding_bp # ABSOLUTE STRIP
    app.register_blueprint(onboarding_bp, url_prefix='/api/v1')
    
    # Phase 23: Payment Transfer API
    app.register_blueprint(payment_transfer_bp)
    
    # Initialize Swagger/OpenAPI documentation
    try:
        from flasgger import Swagger
        swagger_config = {
            "headers": [],
            "specs": [
                {
                    "endpoint": 'apispec',
                    "route": '/api/docs/apispec.json',
                    "rule_filter": lambda rule: True,
                    "model_filter": lambda tag: True,
                }
            ],
            "static_url_path": "/api/docs/flasgger_static",
            "swagger_ui": True,
            "specs_route": "/api/docs/swagger-ui"
        }
        swagger_template = {
            "swagger": "2.0",
            "info": {
                "title": "AI Investor API",
                "description": "Comprehensive API for AI Investor platform",
                "version": "1.0.0",
                "contact": {
                    "name": "API Support",
                    "email": "api@aiinvestor.com"
                }
            },
            "host": os.getenv('API_HOST', 'localhost:5050'),
            "basePath": "/api/v1",
            "schemes": ["http", "https"],
            "securityDefinitions": {
                "Bearer": {
                    "type": "apiKey",
                    "name": "Authorization",
                    "in": "header",
                    "description": "JWT Authorization header using the Bearer scheme. Example: 'Authorization: Bearer {token}'"
                }
            }
        }
        swagger = Swagger(app, config=swagger_config, template=swagger_template)
        print("[OK] Swagger/OpenAPI documentation initialized")
    except ImportError:
        print("[WARN] Flasgger not installed. Install with: pip install flasgger")
    except Exception as e:
        print(f"[ERROR] Failed to initialize Swagger: {e}")

    # Initialize SocketIO with Redis scaling if configured
    from flask_socketio import SocketIO
    from services.system.secret_manager import get_secret_manager
    
    sm = get_secret_manager()
    redis_url = sm.get_secret('REDIS_URL') or f"redis://{sm.get_secret('REDIS_HOST', 'localhost')}:{sm.get_secret('REDIS_PORT', 6379)}/0"
    
    # Check if we should use Redis for horizontal scaling
    message_queue = None
    if os.getenv('WS_SCALE_ENABLED', 'false').lower() == 'true':
        message_queue = redis_url
        print(f"[WS] WebSocket Scaling ENABLED via Redis: {redis_url}")

    # Force threading for Windows Dev stability
    socketio = SocketIO(app, cors_allowed_origins="*", message_queue=message_queue, async_mode='threading')

    # Initialize SocketManager
    from services.system.socket_manager import get_socket_manager
    get_socket_manager().init_app(app, socketio)

    # Initialize CORS
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        from services.monitoring.error_tracker import get_error_tracker
        error_tracker = get_error_tracker()
        error_tracker.capture_message(f"404 Not Found: {request.path}", level='warning')
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from services.monitoring.error_tracker import get_error_tracker
        error_tracker = get_error_tracker()
        error_tracker.capture_exception(error)
        return jsonify({'error': 'Internal server error'}), 500
    
    @app.errorhandler(Exception)
    def handle_exception(e):
        from services.monitoring.error_tracker import get_error_tracker
        error_tracker = get_error_tracker()
        error_tracker.capture_exception(e)
        return jsonify({'error': str(e)}), 500

    return app, socketio



if __name__ == '__main__':
    app, socketio = create_app()
    print("Backend with SocketIO on port 5050...")
    socketio.run(app, host='127.0.0.1', port=5050, debug=True, allow_unsafe_werkzeug=True)
