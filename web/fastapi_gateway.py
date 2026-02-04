"""
FastAPI Gateway - Unified API Entry Point
Phase 54-68: Orchestrates all modern FastAPI-based services.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

# Import routers
from web.api.kyc_api import router as kyc_router
from web.api.cash_api import router as cash_router
from web.api.backtest_api import router as backtest_router
from web.api.estate_api import router as estate_router
from web.api.compliance_api import router as compliance_router
from web.api.scenario_api import router as scenario_router
from web.api.philanthropy_api import router as philanthropy_router
from web.api.system_api import router as system_router
from web.api.corporate_api import router as corporate_router
from web.api.margin_api import router as margin_router
from web.api.mobile_api import router as mobile_router
from web.api.integrations_api import router as integrations_router
from web.api.auth_api import router as auth_router
from web.api.ai_autocoder_api import router as ai_autocoder_router
from web.api.autocoder_api import router as autocoder_router
from web.api.documents_api import router as documents_router
from web.api.discord_api import router as discord_router
from web.api.docs_api import router as docs_router
from web.api.calendar_api import router as calendar_router
from web.api.youtube_api import router as youtube_router
from web.api.wave_apis import all_routers as wave_routers
from web.api.brokerage_api import router as brokerage_router
from web.api.homeostasis_api import router as homeostasis_router
from web.api.market_data_api import router as market_data_router
from web.api.politics_api import router as politics_router
from web.api.debate_api import router as debate_router
from web.api.scanner_api import router as scanner_router
from web.api.settlement_api import router as settlement_router
from web.api.onboarding_api import router as onboarding_router
from web.api.analytics_api import router as analytics_router
from web.api.attribution_api import router as attribution_router
from web.api.briefing_api import router as briefing_router
from web.api.advanced_orders_api import router as advanced_orders_router
from web.api.ai_assistant_api import router as ai_assistant_router
from web.api.ai_predictions_api import router as ai_predictions_router
from web.api.strategy_api import router as strategy_router
from web.api.optimization_api import router as optimization_router, router_hyphen as optimization_hyphen_router
from web.api.advanced_risk_api import router as advanced_risk_router, router_advanced as adv_risk_alias_router
from web.api.assets_api import router as assets_router
from web.api.watchlist_api import watchlist_router, alert_router
from web.api.tax_optimization_api import router as tax_optimization_router, router_hyphen as tax_opt_hyphen_router
from web.api.banking_api import router as banking_router
from web.api.billing_api import router as billing_router
from web.api.budgeting_api import router as budgeting_router
from web.api.legal_api import router as legal_router
from web.api.identity_api import router as identity_router
from web.api.financial_planning_api import router as financial_planning_router
from web.api.retirement_api import router as retirement_router
from web.api.tax_api import router as tax_router
from web.api.charting_api import router as charting_router
from web.api.institutional_api import router as institutional_router
from web.api.news_api import router as news_router
from web.api.community_api import router as community_router
from web.api.education_api import router as education_router
from web.api.enterprise_api import router as enterprise_router
from web.api.ml_training_api import router as ml_training_router
from web.api.research_api import router as research_router
from web.api.social_trading_api import router as social_trading_router
from web.api.social_trading_api import router_hyphen as social_trading_hyphen_router
from web.api.public_api import router as public_api_router
from web.api.public_api import router_hyphen as public_api_hyphen_router
from web.api.macro_data_api import router_hyphen as macro_data_hyphen_router
from web.api.evolution_api import router as evolution_router
# New FastAPI routers (converted from Flask)
from web.api.web3_api import router as web3_router
from web.api.fixed_income_api import router as fixed_income_router
from web.api.risk_api import router as risk_router
from web.api.options_api import router as options_router
from web.api.paper_trading_api import router as paper_trading_router
from web.api.marketplace_api import router as marketplace_router
from web.api.dev_api import router as dev_router
from web.socket_gateway import socket_app

app = FastAPI(title="AI Investor API Gateway", version="2.0.0")

# CORS
# Note: We use allow_origins=[\"*\"] for global API access.
# If Socket.IO headers conflict, we may need to refine this.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check
@app.get("/health")
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "gateway": "fastapi"}

# Register routers
app.include_router(kyc_router)
app.include_router(cash_router)
app.include_router(backtest_router)
app.include_router(estate_router)
app.include_router(compliance_router)
app.include_router(scenario_router)
app.include_router(philanthropy_router)
app.include_router(system_router)
app.include_router(corporate_router)
app.include_router(margin_router)
app.include_router(mobile_router)
app.include_router(integrations_router)
app.include_router(auth_router)
app.include_router(brokerage_router)
app.include_router(homeostasis_router)
app.include_router(market_data_router)
app.include_router(politics_router)
app.include_router(debate_router)
app.include_router(scanner_router)
app.include_router(settlement_router)
app.include_router(onboarding_router)
app.include_router(analytics_router)
app.include_router(attribution_router)
app.include_router(briefing_router)
app.include_router(advanced_orders_router)
app.include_router(ai_assistant_router)
app.include_router(ai_predictions_router)
app.include_router(strategy_router)
app.include_router(optimization_router)
app.include_router(optimization_hyphen_router)
app.include_router(advanced_risk_router)
app.include_router(adv_risk_alias_router)
app.include_router(assets_router)
app.include_router(watchlist_router)
app.include_router(alert_router)
app.include_router(tax_optimization_router)
app.include_router(tax_opt_hyphen_router)
app.include_router(banking_router)
app.include_router(billing_router)
app.include_router(budgeting_router)
app.include_router(legal_router)
app.include_router(identity_router)
app.include_router(financial_planning_router)
app.include_router(retirement_router)
app.include_router(tax_router)
app.include_router(charting_router)
app.include_router(institutional_router)
app.include_router(news_router)
app.include_router(community_router)
app.include_router(education_router)
app.include_router(enterprise_router)
app.include_router(ml_training_router)
app.include_router(research_router)
app.include_router(social_trading_router)
app.include_router(social_trading_hyphen_router)
app.include_router(public_api_router)
app.include_router(public_api_hyphen_router)
app.include_router(macro_data_hyphen_router)
app.include_router(evolution_router)
# New FastAPI routers (converted from Flask)
app.include_router(web3_router)
app.include_router(fixed_income_router)
app.include_router(risk_router)
app.include_router(options_router)
app.include_router(paper_trading_router)
app.include_router(marketplace_router)
app.include_router(dev_router)
app.include_router(ai_autocoder_router)
app.include_router(autocoder_router)
app.include_router(documents_router)
app.include_router(discord_router)
app.include_router(docs_router)
app.include_router(calendar_router)
app.include_router(youtube_router)

# Ported Hedging Engine
from web.api.hedging_api import router as hedging_router
app.include_router(hedging_router)

# Wave APIs (Phases 57-68)
for r in wave_routers:
    app.include_router(r)

# Mount Socket.IO ASGI app
app.mount("/socket.io", socket_app)

# Legacy / Gap support
@app.get("/api/v1/gap")
async def get_gap():
    return {
        "stock": 100000.00,
        "set_point": 100000.00,
        "gap": 0.00,
        "gap_percent": 0.0
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5050))
    print(f"🚀 Starting FastAPI Gateway on port {port}...")
    uvicorn.run(app, host="127.0.0.1", port=port)
