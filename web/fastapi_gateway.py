import sys
import os
print(f">>> [BOOTSTRAP] Loading fastapi_gateway.py (PID: {os.getpid()})...")
import logging
import asyncio
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from web.socket_gateway import get_socket_app, get_sio

from web.api import health_api
from web.api import auth_api
from web.api import system_api
from web.api import agents_api
from web.api import dev_api
from web.api import debate_api
from web.api import departments_api
from web.api import master_orchestrator_api
from web.api import onboarding_api
from web.api import tasks_api
from web.api import dashboard_api
from web.api import brokerage_api
from web.api import strategy_api
from web.api import risk_api
from web.api import market_data_api
from web.api import news_api
from web.api import watchlist_api
from web.api import scanner_api
from web.api import homeostasis_api
from web.api import evolution_api
from web.api import identity_api
from web.api import compliance_api
from web.api import estate_api
from web.api import tax_api
from web.api import macro_api
from web.api import corporate_api
from web.api import margin_api
from web.api import mobile_api
from web.api import integrations_api
from web.api import admin
from web.api.admin import deployments_api
from web.api.admin import ops_api
from web.api.admin import workspaces_api
from web.api import advanced_risk_api

from web.api import advanced_orders_api
from web.api import ai_assistant_api
from web.api import ai_predictions_api
from web.api import analytics_api
from web.api import assets_api
from web.api import attribution_api
from web.api import banking_api
from web.api import billing_api
from web.api import budgeting_api
from web.api import calendar_api
from web.api import cash_api
from web.api import communication_api
from web.api import community_api
from web.api import credit_api
from web.api import crypto_api
from web.api import docs_api
from web.api import documents_api
from web.api import economics_api
from web.api import education_api
from web.api import email_api
from web.api import enterprise_api
from web.api import financial_planning_api
from web.api import fixed_income_api
from web.api import growth_api
from web.api import hedging_api
from web.api import incident_api
from web.api import institutional_api
from web.api import marketplace_api
from web.api import ml_training_api
from web.api import news_api
from web.api import optimization_api
from web.api import options_api
from web.api import paper_trading_api
from web.api import payment_transfer_api
from web.api import philanthropy_api
from web.api import politics_api
from web.api import privacy_api
from web.api import public_api
from web.api import research_api
from web.api import retirement_api
from web.api import search_api
from web.api import settlement_api
from web.api import social_api
from web.api import social_trading_api
from web.api import spatial_api
from web.api import system_telemetry_api
from web.api import tax_optimization_api
from web.api import indicators_api
from web.api import compliance_144a_api
from web.api import ingestion_api
from web.api import external_data_api
from web.api import webhook_ingestion_api
from web.api import quantitative_api
from web.api import analysis_api
from web.api import charting_api
from web.api import pricing_api
from web.api import missions_api
from web.api import modes_api
from web.api import meta_api
from web.api import singularity_api
from web.api import execution_core_api
from web.api import smart_router_api
from web.api import execution_analytics_api
from web.api import broker_health_api
from web.api import brokerage_integration_api
from web.api import backtest_api
print(">>> [BOOTSTRAP] Importing administrative and legal API modules...")
from web.api import simulation_api
from web.api import alerts_api
from web.api import opportunities_api
from web.api import screener_api
from web.api import watchlist_share_api
from web.api import fraud_api
from web.api import risk_limits_api
from web.api import legal_api
from web.api import audit_api
from web.api import security_api
from web.api import warden_api
from web.api import audit_recon_api
from web.api import reporting_api
from web.api import validation_api
from web.api import valuation_api
from web.api import reputation_api
from web.api import treasury_api
from web.api import portfolio_api
from web.api import order_api
from web.api import defi_api
from web.api import tax_reporting_api
from web.api import wealth_planning_api
from web.api import stress_test_api
from web.api import orchestrator_api
print(">>> [BOOTSTRAP] Importing core components and approval routes...")
from web.routes import approval_router
import web.api.market as market_api


# Setup logging
logger = logging.getLogger(__name__)

# Initialize FastAPI App
print(">>> [BOOTSTRAP] Initializing FastAPI App instance...")
app = FastAPI(
    title="Sovereign OS: AI Investor API",
    description="Unified API Gateway for the Sovereign AI Investor Organization.",
    version="1.0.0"
)
print(">>> [BOOTSTRAP] FastAPI App instance created.")

# --- Debug Middleware for Event Loop Stalls ---
@app.middleware("http")
async def log_request_time(request: Request, call_next):
    import time
    start_time = time.time()
    logger.info(f"Incoming Request: {request.method} {request.url.path}")
    response = None
    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(f"Error processing {request.method} {request.url.path}: {e}")
        raise
    finally:
        process_time = time.time() - start_time
        if process_time > 1.0:
            logger.warning(f"🐢 SLOW REQUEST: {request.method} {request.url.path} took {process_time:.4f}s")
        else:
            logger.info(f"⚡ COMPLETED: {request.method} {request.url.path} in {process_time:.4f}s")
    return response

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Include Core Routers ---
app.include_router(health_api.router)
app.include_router(auth_api.router)
app.include_router(system_api.router)
app.include_router(agents_api.router)
app.include_router(dev_api.router)
app.include_router(debate_api.router)
app.include_router(departments_api.router)
app.include_router(master_orchestrator_api.router)
app.include_router(approval_router.router)
app.include_router(onboarding_api.router)
app.include_router(tasks_api.router)
app.include_router(dashboard_api.router)
app.include_router(brokerage_api.router)
app.include_router(strategy_api.router)
app.include_router(risk_api.router)
app.include_router(market_data_api.router)
app.include_router(news_api.router)
app.include_router(watchlist_api.router)
app.include_router(scanner_api.router)
app.include_router(homeostasis_api.router)
app.include_router(evolution_api.router)
app.include_router(identity_api.router)
app.include_router(compliance_api.router)
app.include_router(estate_api.router)
app.include_router(tax_api.router)
app.include_router(macro_api.router)
app.include_router(corporate_api.router)
app.include_router(margin_api.router)
app.include_router(mobile_api.router)
app.include_router(integrations_api.router)
app.include_router(admin.router)
# app.include_router(deployments_api.router)
# app.include_router(ops_api.router)
# app.include_router(workspaces_api.router) # New

# Phase 6+ and Supplemental Routers
app.include_router(advanced_risk_api.router)
app.include_router(advanced_orders_api.router)
app.include_router(ai_assistant_api.router)
app.include_router(ai_predictions_api.router)
app.include_router(analytics_api.router)
app.include_router(analysis_api.router)
# app.include_router(analysis_api.router) (Duplicate)
app.include_router(assets_api.router) # Now fully populated
app.include_router(attribution_api.router)
# app.include_router(attribution_api.router) (Duplicate)
app.include_router(banking_api.router)
app.include_router(billing_api.router)
app.include_router(budgeting_api.router)
app.include_router(calendar_api.router)
app.include_router(cash_api.router)
app.include_router(communication_api.router)
app.include_router(community_api.router)
app.include_router(credit_api.router)
app.include_router(crypto_api.router)
app.include_router(docs_api.router)
app.include_router(documents_api.router)
app.include_router(economics_api.router)
app.include_router(education_api.router)
app.include_router(email_api.router)
app.include_router(enterprise_api.router)
app.include_router(financial_planning_api.router)
app.include_router(fixed_income_api.router)
app.include_router(growth_api.router)
app.include_router(hedging_api.router)
app.include_router(incident_api.router)
app.include_router(institutional_api.router)
app.include_router(marketplace_api.router)
app.include_router(market_api.router)
app.include_router(ml_training_api.router)
app.include_router(news_api.router)
app.include_router(optimization_api.router)
app.include_router(options_api.router)
app.include_router(paper_trading_api.router)
app.include_router(payment_transfer_api.router)
app.include_router(philanthropy_api.router)
app.include_router(politics_api.router)
app.include_router(pricing_api.router)
app.include_router(privacy_api.router)
app.include_router(public_api.router)
app.include_router(research_api.router)
# app.include_router(research_api.router) (Duplicate)
app.include_router(quantitative_api.router)
app.include_router(retirement_api.router)
app.include_router(search_api.router)
app.include_router(settlement_api.router)
app.include_router(social_api.router)
app.include_router(social_trading_api.router)
app.include_router(spatial_api.router)
app.include_router(system_telemetry_api.router)
app.include_router(tax_optimization_api.router)
# app.include_router(identifiers_api.router) # Not imported - identity_api covers it
app.include_router(compliance_144a_api.router)
app.include_router(ingestion_api.router)
app.include_router(external_data_api.router)
app.include_router(webhook_ingestion_api.router)
app.include_router(indicators_api.router)
app.include_router(missions_api.router)
app.include_router(modes_api.router)
app.include_router(meta_api.router)
app.include_router(singularity_api.router)
app.include_router(execution_core_api.router)
app.include_router(smart_router_api.router)
app.include_router(execution_analytics_api.router)
app.include_router(broker_health_api.router)
app.include_router(brokerage_integration_api.router)
app.include_router(backtest_api.router)
app.include_router(simulation_api.router)
app.include_router(watchlist_api.router)
app.include_router(alerts_api.router)
app.include_router(opportunities_api.router)
app.include_router(screener_api.router)
app.include_router(watchlist_share_api.router)
app.include_router(risk_api.router)
app.include_router(fraud_api.router)
app.include_router(risk_limits_api.router)
app.include_router(compliance_api.router)
app.include_router(legal_api.router)
app.include_router(audit_api.router)
app.include_router(security_api.router)
app.include_router(auth_api.router)
app.include_router(warden_api.router)
app.include_router(audit_recon_api.router)
app.include_router(reporting_api.router)
app.include_router(validation_api.router)
app.include_router(valuation_api.router)
app.include_router(reputation_api.router)
app.include_router(treasury_api.router)
app.include_router(portfolio_api.router)
app.include_router(reporting_api.router)
app.include_router(tax_reporting_api.router)
app.include_router(wealth_planning_api.router)
app.include_router(stress_test_api.router)
app.include_router(philanthropy_api.router)
app.include_router(banking_api.router)
app.include_router(crypto_api.router)
app.include_router(defi_api.router)
# app.include_router(admin.router)

# app.include_router(mission_api.router) # If found later

# Mount Socket.IO
app.mount("/socket.io", get_socket_app())

# Mounted via main Socket.IO app using namespace /admin/event-bus


# Global Slack Service reference for lifecycle management
_slack_service = None

@app.on_event("startup")
async def startup_event():
    print(">>> [STARTUP] Running minimal startup...")
    logger.info("Sovereign OS Gateway starting up (Minimal Mode)...")
    print(">>> [STARTUP] Minimal startup completed.")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Sovereign OS Gateway shutting down...")
    try:
        if _slack_service:
            # Cleanup resources (this also updates status and sends disconnection message)
            await _slack_service.close()
            _slack_service = None
            logger.info("✅ Slack Service resources released.")
    except Exception as e:
        logger.warning(f"Failed to gracefully shutdown Slack Service: {e}")

if __name__ == "__main__":
    import uvicorn
    print(">>> [BOOTSTRAP] Configuration complete. Starting Uvicorn...")
    uvicorn.run(
        app, 
        host="127.0.0.1", 
        port=5050, 
        log_level="info",
        reload=False,
        workers=1
    )

