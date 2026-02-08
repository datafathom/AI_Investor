import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from web.socket_gateway import socket_app, sio
from web.api import (
    health_api,
    auth_api,
    system_api,
    agents_api,
    dev_api,
    debate_api,
    departments_api,
    master_orchestrator_api,
    onboarding_api,
    tasks_api,
    dashboard_api,
    brokerage_api,
    strategy_api,
    risk_api,
    market_data_api,
    news_api,
    watchlist_api,
    scanner_api,
    homeostasis_api,
    evolution_api,
    identity_api,
    compliance_api,
    estate_api,
    tax_api,
    macro_api,
    corporate_api,
    margin_api,
    mobile_api,
    integrations_api,
    admin,
    deployments_api,
    ops_api,
    workspaces_api,
    advanced_risk_api,
    advanced_orders_api,
    ai_assistant_api,
    ai_predictions_api,
    analytics_api,
    assets_api,
    attribution_api,
    banking_api,
    billing_api,
    budgeting_api,
    calendar_api,
    cash_api,
    communication_api,
    community_api,
    credit_api,
    crypto_api,
    docs_api,
    documents_api,
    economics_api,
    education_api,
    email_api,
    enterprise_api,
    financial_planning_api,
    fixed_income_api,
    growth_api,
    hedging_api,
    incident_api,
    institutional_api,
    market_api,
    marketplace_api,
    ml_training_api,
    news_api,
    optimization_api,
    options_api,
    paper_trading_api,
    payment_transfer_api,
    philanthropy_api,
    politics_api,
    privacy_api,
    public_api,
    research_api,
    retirement_api,
    search_api,
    settlement_api,
    social_api,
    social_trading_api,
    spatial_api,
    system_telemetry_api,
    tax_optimization_api
)
from web.api import indicators_api
from web.api import compliance_144a_api
from web.routes import approval_router

# Setup logging
logger = logging.getLogger(__name__)

# Initialize FastAPI App
app = FastAPI(
    title="Sovereign OS: AI Investor API",
    description="Unified API Gateway for the Sovereign AI Investor Organization.",
    version="1.0.0"
)

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
app.include_router(assets_api.router)
app.include_router(attribution_api.router)
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
app.include_router(privacy_api.router)
app.include_router(public_api.router)
app.include_router(research_api.router)
app.include_router(retirement_api.router)
app.include_router(search_api.router)
app.include_router(settlement_api.router)
app.include_router(social_api.router)
app.include_router(social_trading_api.router)
app.include_router(spatial_api.router)
app.include_router(system_telemetry_api.router)
app.include_router(tax_optimization_api.router)
app.include_router(indicators_api.router)
app.include_router(compliance_144a_api.router)

# app.include_router(mission_api.router) # If found later

# Mount Socket.IO
app.mount("/socket.io", socket_app)

from web.websocket.event_bus_ws import eb_socket_app
app.mount("/ws/admin/event-bus", eb_socket_app)

# Global Slack Service reference for lifecycle management
_slack_service = None

@app.on_event("startup")
async def startup_event():
    global _slack_service
    logger.info("Sovereign OS Gateway starting up...")
    try:
        from services.notifications.slack_service import get_slack_service
        _slack_service = get_slack_service()
        
        # 1. Announce Online
        await _slack_service.send_notification(
            text="🚀 *AI Investor Backend Online:* Unified Gateway is active.", 
            level="success"
        )
        
        # 2. Start Event Bus Broadcaster
        try:
            from web.websocket.event_bus_ws import start_event_bus_broadcast
            start_event_bus_broadcast()
            logger.info("🛰️ Event Bus WS Broadcaster started.")
        except Exception as e:
            logger.error(f"Failed to start Event Bus WS Broadcaster: {e}")

        # 3. Start Bot Listener in Background (non-blocking)
        import asyncio
        asyncio.create_task(_slack_service.start_bot())
        logger.info("📡 Slack Bot listener integrated and running.")
        
    except Exception as e:
        logger.warning(f"Failed to initialize integrated Slack Bot: {e}")

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
    uvicorn.run(app, host="127.0.0.1", port=5050)
