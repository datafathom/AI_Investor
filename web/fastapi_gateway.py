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

app = FastAPI(title="AI Investor API Gateway", version="2.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
