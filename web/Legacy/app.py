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
import eventlet
eventlet.monkey_patch()
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
# from web.api.compliance_api import compliance_bp # REPLACED BY WAVE_APIS
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
# from web.api.estate_api import estate_bp # REPLACED BY WAVE_APIS
from web.api.ethereum_api import ethereum_bp
from web.api.evolution_api import evolution_bp
from web.api.facebook_auth_api import facebook_auth_bp
from web.api.facebook_hype_api import facebook_hype_bp
from web.api.financial_planning_api import financial_planning_bp
from web.api.fixed_income_api import fixed_income_bp
from web.api.gmail_api import gmail_bp
from web.api.google_auth_api import google_auth_bp
from web.api.master_orchestrator_api import master_orchestrator_bp
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
from web.api.wave_apis import backtest_bp, corporate_bp, integrations_bp, margin_bp, mobile_bp, philanthropy_bp, scenario_bp, system_bp, zen_bp, compliance_bp, estate_bp
from web.api.web3_api import web3_bp
from web.api.workspace_api import workspace_bp
from web.api.youtube_api import youtube_bp
from web.api.payment_transfer_api import payment_transfer_bp
from web.api.scanner_api import scanner_bp
from web.api.search_api import search_bp
from web.api.system_telemetry_api import system_telemetry_bp
from web.routes.market_routes import market_bp
from web.routes.system_routes import system_bp as system_routes_bp
from web.api.economics_api import economics_bp
# --- FINISHED CONSOLIDATION ---

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
    
    # Initialize CORS early to handle preflight requests
    from flask_cors import CORS
    CORS(app, resources={r"/*": {
        "origins": ["http://127.0.0.1:5173", "http://localhost:5173"],
        "allow_headers": ["Content-Type", "Authorization", "X-Requested-With", "X-Tenant-ID", "x-tenant-id"],
        "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE", "PATCH"],
        "supports_credentials": True
    }})
    print("[OK] CORS initialized")
    
    # Initialize error tracking
    from services.monitoring.error_tracker import get_error_tracker
    error_tracker = get_error_tracker()
    if error_tracker.is_enabled():
        print("[OK] Error tracking initialized (Sentry)")
    
    # Initialize performance middleware
    from web.middleware.performance_middleware import performance_monitor, compress_response
    from web.middleware.rate_limiter import RateLimiter
    performance_monitor(app)
    # compress_response(app) # Disabled due to AssertionError: write() before start_response on Windows
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
    
    def safe_register(bp, **kwargs):
        try:
            name = kwargs.get('name', bp.name)
            if name in app.blueprints:
                print(f"[INFO] Blueprint '{name}' already registered, skipping.")
                return
            app.register_blueprint(bp, **kwargs)
        except ValueError as e:
            print(f"[ERROR] Failed to register blueprint '{bp.name}': {e}")

    # --- BLUEPRINT REGISTRATIONS ---
    # Register all blueprints exactly once with correct prefixes.
    
    # Dashboard & Orchestration
    safe_register(dashboard_bp)
    safe_register(master_orchestrator_bp)
    safe_register(communication_bp)
    safe_register(politics_bp)
    safe_register(evolution_bp)
    safe_register(autocoder_bp)
    safe_register(ai_autocoder_bp)
    
    # Core User & Workspace
    safe_register(auth_bp)
    safe_register(privacy_bp)
    safe_register(workspace_bp) # Prefix in definition
    safe_register(legal_bp)
    safe_register(onboarding_bp)
    
    # Financial & Trading
    safe_register(banking_bp)
    safe_register(brokerage_bp)
    safe_register(billing_bp)
    safe_register(crypto_api_bp)
    safe_register(settlement_bp)
    safe_register(advanced_orders_bp)
    safe_register(execution_bp)
    safe_register(paper_trading_bp)
    safe_register(simulation_bp)
    safe_register(strategy_bp)
    safe_register(watchlist_bp)
    safe_register(alert_bp)
    
    # UI Phase 54-68 (Wave APIs)
    safe_register(kyc_bp)
    safe_register(cash_bp)
    safe_register(backtest_bp)
    safe_register(estate_bp)
    safe_register(compliance_bp)
    safe_register(scenario_bp)
    safe_register(philanthropy_bp)
    safe_register(system_bp) # system_bp from wave_apis
    safe_register(corporate_bp)
    safe_register(margin_bp)
    safe_register(mobile_bp)
    safe_register(integrations_bp)
    safe_register(zen_bp)
    
    # Data & Analytics
    safe_register(market_data_bp)
    safe_register(macro_data_bp)
    safe_register(macro_bp)
    safe_register(economics_bp)
    safe_register(analytics_bp)
    safe_register(optimization_bp)
    safe_register(advanced_risk_bp)
    safe_register(tax_optimization_bp)
    safe_register(options_bp)
    safe_register(financial_planning_bp)
    safe_register(retirement_bp)
    safe_register(budgeting_bp)
    safe_register(credit_bp)
    safe_register(news_bp)
    
    # Institutional & ML
    safe_register(institutional_bp)
    safe_register(ml_training_bp)
    safe_register(integration_bp)
    safe_register(marketplace_bp)
    safe_register(enterprise_bp)
    
    # Social & AI
    safe_register(social_bp)
    safe_register(social_trading_bp)
    safe_register(forum_bp)
    safe_register(qa_bp)
    safe_register(debate_bp)
    safe_register(briefing_bp)
    safe_register(research_bp)
    safe_register(ai_predictions_bp)
    safe_register(ai_assistant_bp)
    
    # Connectivity & Integrations
    safe_register(google_auth_bp)
    safe_register(gmail_bp)
    safe_register(calendar_bp)
    safe_register(facebook_auth_bp)
    safe_register(facebook_hype_bp)
    safe_register(ibkr_bp)
    safe_register(robinhood_bp)
    safe_register(ethereum_bp)
    safe_register(solana_bp)
    safe_register(coinbase_bp)
    safe_register(coinbase_crypto_bp)
    safe_register(stocktwits_bp)
    safe_register(discord_bp)
    safe_register(youtube_bp)
    safe_register(stripe_bp)
    safe_register(paypal_bp)
    safe_register(venmo_bp)
    safe_register(square_bp)
    safe_register(plaid_bp)
    safe_register(binance_bp)
    safe_register(tax_api_bp)
    safe_register(taxbit_bp)
    safe_register(twilio_api_bp)
    safe_register(email_api_bp)
    safe_register(incident_api_bp)
    
    # Infrastructure & System
    safe_register(system_routes_bp) # Registered without prefix to allow internal name 'system_bp'
    safe_register(system_telemetry_bp)
    safe_register(documents_bp)
    safe_register(identity_api)
    safe_register(market_bp)
    safe_register(docs_bp)
    safe_register(education_bp)
    safe_register(spatial_bp)
    safe_register(fixed_income_bp)
    safe_register(web3_bp)
    safe_register(scanner_bp)
    safe_register(payment_transfer_bp)
    safe_register(search_bp)

    # Enhanced health check endpoints
    safe_register(health_bp)
    
    # Missing Registration
    safe_register(homeostasis_api, url_prefix='/api/v1/homeostasis')

    # Observability Setup
    print("DEBUG: Initializing TracingService...")
    from services.system.tracing_service import get_tracing_service
    from services.system.logging_service import get_logging_service
    get_tracing_service().initialize(app)
    print("DEBUG: TracingService initialized.")
    get_logging_service().initialize()
    print("DEBUG: LoggingService initialized.")
    
    # Security Gateway
    print("DEBUG: Initializing Security Gateway...")
    from services.system.security_gateway import limiter, get_security_gateway
    limiter.init_app(app)
    app.config['SECURITY_GATEWAY'] = get_security_gateway()
    print("DEBUG: Security Gateway initialized.")

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
        if 'flasgger' not in app.blueprints:
            swagger = Swagger(app, config=swagger_config, template=swagger_template)
            print("[OK] Swagger/OpenAPI documentation initialized")
        else:
            print("[INFO] Swagger/OpenAPI already initialized")
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

    # Define origins for SocketIO
    allowed_origins = ["http://127.0.0.1:5173", "http://localhost:5173"]
    socketio = SocketIO(app, cors_allowed_origins=allowed_origins, message_queue=message_queue, async_mode='eventlet', ping_timeout=60)

    # Initialize SocketManager
    from services.system.socket_manager import get_socket_manager
    get_socket_manager().init_app(app, socketio)
    
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
    print("DEBUG: __main__ block started")
    app, socketio = create_app()
    print("DEBUG: create_app() returned. Starting socketio.run on 127.0.0.1:5050...")
    socketio.run(app, host='127.0.0.1', port=5050, debug=False, allow_unsafe_werkzeug=True)
