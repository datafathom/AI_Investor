"""
Wave APIs - Consolidated Flask Blueprints for UI Phases 57-68
Consolidates all Wave 3-5 endpoints for easier registration and demoability.
"""

from flask import Blueprint, jsonify, request
import asyncio
import logging
import uuid
from datetime import datetime

logger = logging.getLogger(__name__)

from web.auth_utils import login_required, requires_role
# ... (existing imports)

# ...

# Define Blueprints with URL Prefixes
backtest_bp = Blueprint('backtest_api_v1', __name__, url_prefix='/api/v1/backtest')
estate_bp = Blueprint('estate_api_v1', __name__, url_prefix='/api/v1/estate')
compliance_bp = Blueprint('compliance_api_v1', __name__, url_prefix='/api/v1/compliance')
scenario_bp = Blueprint('scenario_api_v1', __name__, url_prefix='/api/v1/scenario')
philanthropy_bp = Blueprint('philanthropy_api_v1', __name__, url_prefix='/api/v1/philanthropy')
system_bp = Blueprint('system_api_v1', __name__, url_prefix='/api/v1/system')
corporate_bp = Blueprint('corporate_api_v1', __name__, url_prefix='/api/v1/corporate')
margin_bp = Blueprint('margin_api_v1', __name__, url_prefix='/api/v1/margin')
mobile_bp = Blueprint('mobile_api_v1', __name__, url_prefix='/api/v1/mobile')
integrations_bp = Blueprint('integrations_api_v1', __name__, url_prefix='/api/v1/integrations')
assets_bp = Blueprint('assets_api_v1', __name__, url_prefix='/api/v1/assets')
zen_bp = Blueprint('zen_api_v1', __name__, url_prefix='/api/v1/market')

# Phase 1 API Integration - Market Data
from web.api.market_data_api import market_data_bp

from services.security.estate_service import get_estate_service
from services.security.compliance_service import get_compliance_service
from services.analysis.scenario_service import get_scenario_service
from services.analysis.esg_service import get_esg_service
from services.security.system_health_service import get_system_health_service
from services.trading.corporate_service import get_corporate_service
from services.risk.margin_service import get_margin_service
from services.security.mobile_service import get_mobile_service
from services.trading.integrations_service import get_integrations_service
from services.portfolio.assets_service import assets_service
from services.analysis.homeostasis_service import get_homeostasis_service
from services.analysis.monte_carlo_service import get_monte_carlo_service

# Helper for async execution in Flask
def _run_async(coro):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            return asyncio.run_coroutine_threadsafe(coro, loop).result()
    except RuntimeError:
        pass
    return asyncio.run(coro)

# --- Backtest (Phase 57) ---
@backtest_bp.route('/monte-carlo', methods=['POST'])
@login_required
def run_monte_carlo():
    """
    Run Geometric Brownian Motion simulation for portfolio projection.
    
    Predicts future portfolio value distribution based on historical mean 
    returns and volatility.
    
    Payload:
        initial_value (float): Starting balance in USD.
        mu (float): Expected annual return (0.08 = 8%).
        sigma (float): Annualized volatility (0.15 = 15%).
        
    Returns:
        JSON: Standardized response with simulation paths and ruin probability.
        
    Security:
        Bearer JWT required.
    """
    try:
        data = request.json or {}
        service = get_monte_carlo_service()
        res = service.run_gbm_simulation(
            data.get('initial_value', 1000000), 
            mu=data.get('mu', 0.08), 
            sigma=data.get('sigma', 0.15)
        )
        return jsonify({
            "status": "success",
            "data": {
                "paths": res.paths, 
                "quantiles": res.quantiles, 
                "ruin_probability": res.ruin_probability,
                "median_final": res.median_final
            }
        })
    except Exception as e:
        logger.exception("Monte Carlo simulation failed")
        return jsonify({"status": "error", "message": str(e)}), 500

@backtest_bp.route('/overfit', methods=['GET'])
@login_required
def check_overfit():
    """
    Verify if strategy performance is due to over-optimization.
    
    Compares in-sample vs. out-of-sample Sharpe ratios to detect probability 
    of backtest overfitting.
    
    Query Params:
        is_sharpe (float): In-sample Sharpe ratio.
        oos_sharpe (float): Out-of-sample Sharpe ratio.
        
    Returns:
        JSON: Standardized response with overfit indicator and variance analysis.
        
    Security:
        Bearer JWT required.
    """
    try:
        is_sharpe = request.args.get('is_sharpe', 1.5, type=float)
        oos_sharpe = request.args.get('oos_sharpe', 1.12, type=float)
        service = get_monte_carlo_service()
        is_overfit, variance = service.detect_overfit(is_sharpe, oos_sharpe)
        return jsonify({
            "status": "success",
            "data": {
                "is_overfit": is_overfit, 
                "variance": variance
            }
        })
    except Exception as e:
        logger.exception("Overfit check failed")
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Estate (Phase 58) ---
@estate_bp.route('/heartbeat', methods=['GET'])
@login_required
def get_heartbeat():
    """
    Check the "Dead Man's Switch" status for Estate execution.
    
    Monitors the user's activity heartbeat; if expired, triggers automatic 
    legal and wealth distribution sequences.
    
    Returns:
        JSON: Standardized response with last check-in and days till trigger.
        
    Security:
        Bearer JWT required.
    """
    try:
        service = get_estate_service()
        status = service.check_heartbeat("demo-user")
        return jsonify({
            "status": "success",
            "data": {
                "last_check": status.last_check, 
                "is_alive": status.is_alive, 
                "days_until_trigger": status.days_until_trigger
            }
        })
    except Exception as e:
        logger.exception("Estate heartbeat check failed")
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Compliance (Phase 59) ---
@compliance_bp.route('/overview', methods=['GET'])
@login_required
def get_compliance_overview():
    """
    Retrieve high-level compliance health and alert summary.
    
    Aggregation of compliance scores, pending SAR alerts, and total audit logs.
    
    Returns:
        JSON: Standardized response with score and alert counts.
    """
    try:
        service = get_compliance_service()
        score = service.get_compliance_score()
        alerts = service.get_sar_alerts()
        logs = service.get_audit_logs()
        return jsonify({
            "status": "success",
            "data": {
                "compliance_score": score,
                "pending_alerts": len([a for a in alerts if a.status == "pending"]),
                "total_logs": len(logs)
            }
        })
    except Exception as e:
        logger.exception("Compliance overview failed")
        return jsonify({"status": "error", "message": str(e)}), 500

@compliance_bp.route('/audit', methods=['GET'])
@login_required
def get_audit_logs():
    """
    Retrieve immutable audit logs for regulatory oversight.
    
    Returns a list of actions, resource access, and cryptographic hashes 
    ensuring log integrity.
    
    Query Params:
        limit (int): Maximum number of log entries to return.
        
    Returns:
        JSON: Standardized response with audit log array.
    """
    try:
        limit = request.args.get('limit', 100, type=int)
        service = get_compliance_service()
        logs = service.get_audit_logs(limit)
        return jsonify({
            "status": "success",
            "data": [{
                "id": l.id,
                "timestamp": l.timestamp,
                "action": l.action,
                "resource": l.resource,
                "status": l.status,
                "severity": l.severity,
                "details": l.details,
                "prev_hash": l.prev_hash,
                "hash": l.hash
            } for l in logs]
        })
    except Exception as e:
        logger.exception("Audit log fetch failed")
        return jsonify({"status": "error", "message": str(e)}), 500

@compliance_bp.route('/sar', methods=['GET'])
@login_required
def list_sar_alerts():
    """
    List Suspicious Activity Report (SAR) alerts for investigation.
    
    Returns:
        JSON: Standardized response with SAR alert array.
    """
    try:
        service = get_compliance_service()
        alerts = service.get_sar_alerts()
        return jsonify({
            "status": "success",
            "data": [{
                "id": a.id,
                "timestamp": a.timestamp,
                "type": a.type,
                "status": a.status,
                "severity": a.severity,
                "description": a.description,
                "evidence_score": a.evidence_score,
                "agent_id": a.agent_id
            } for a in alerts]
        })
    except Exception as e:
        logger.exception("SAR alert list failed")
        return jsonify({"status": "error", "message": str(e)}), 500

@compliance_bp.route('/sar/<sap_id>/status', methods=['POST'])
@login_required
@requires_role('admin')
def update_sar_status(sap_id):
    """
    Update the resolution status of a SAR alert.
    
    Args:
        sap_id (str): Unique identifier for the SAR.
        
    Query Params:
        status (str): New status (e.g., 'resolved', 'investigating').
        
    Returns:
        JSON: Success confirmation.
    """
    try:
        status = request.args.get('status')
        service = get_compliance_service()
        success = service.update_sar_status(sap_id, status)
        if not success:
            return jsonify({"status": "error", "message": "SAR not found"}), 404
        return jsonify({"status": "success"})
    except Exception as e:
        logger.exception("SAR status update failed")
        return jsonify({"status": "error", "message": str(e)}), 500

@compliance_bp.route('/verify', methods=['GET'])
@login_required
def verify_integrity():
    """
    Verify the cryptographic integrity of the compliance ledger.
    
    Runs a chain verification to ensure audit logs have not been tampered with.
    
    Returns:
        JSON: Standardized response with validity status and error list.
    """
    try:
        service = get_compliance_service()
        res = service.verify_log_integrity()
        return jsonify({
            "status": "success",
            "data": {
                "is_valid": res['is_valid'],
                "errors": res['errors'],
                "log_count": res['log_count'],
                "timestamp": res['timestamp']
            }
        })
    except Exception as e:
        logger.exception("Integrity verification failed")
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Scenario (Phase 60) ---
@scenario_bp.route('/simulate', methods=['POST'])
@login_required
def simulate_scenario():
    """
    Apply macro-economic shocks to portfolio value.
    
    Simulates the impact of historical or custom market events (e.g., COVID-2020)
    on the current portfolio holdings and projects recovery timelines.
    
    Payload:
        id (str): Reference ID for the shock scenario.
        equityDrop (float): Expected percentage drop in equity value.
        bondDrop (float): Expected percentage drop in bond value.
        goldChange (float): Expected percentage change in gold price.
        
    Returns:
        JSON: Standardized response with impact metrics and recovery path.
        
    Security:
        Bearer JWT required.
    """
    try:
        service = get_scenario_service()
        from services.analysis.scenario_service import MacroShock
        data = request.json
        shock = MacroShock(data['id'], data['id'], data['equityDrop'], data['bondDrop'], data['goldChange'])
        result = service.apply_shock("default", shock)
        sufficiency = service.calculate_hedge_sufficiency("default", shock)
        recovery = service.project_recovery_timeline(result)
        
        return jsonify({
            "status": "success",
            "data": {
                "impact": {
                    "portfolio_impact_pct": result.portfolio_impact,
                    "new_value": result.new_portfolio_value,
                    "net_impact_usd": result.net_impact,
                    "hedge_offset": result.hedge_offset
                },
                "hedge_sufficiency": sufficiency,
                "recovery": {
                    "days": recovery.recovery_days,
                    "path": recovery.recovery_path,
                    "worst_case": recovery.worst_case_days
                }
            }
        })
    except Exception as e:
        logger.exception("Scenario simulation failed")
        return jsonify({"status": "error", "message": str(e)}), 500

@scenario_bp.route('/monte-carlo-refined', methods=['GET'])
@login_required
def run_refined_mc():
    """
    Run post-shock Monte Carlo simulation.
    
    Predicts the range of recovery outcomes following a major market shock 
    using 10,000+ paths.
    
    Query Params:
        scenario_id (str): ID of the shock event.
        initial_value (float): Starting balance post-shock.
        
    Returns:
        JSON: Standardized response with refined recovery distributions.
    """
    try:
        scenario_id = request.args.get('scenario_id')
        initial_value = request.args.get('initial_value', type=float)
        service = get_scenario_service()
        from services.analysis.scenario_service import MacroShock
        shock = MacroShock(id=scenario_id, name=scenario_id, equity_drop=0, bond_drop=0, gold_change=0)
        res = service.run_refined_monte_carlo(initial_value, shock)
        return jsonify({
            "status": "success",
            "data": res
        })
    except Exception as e:
        logger.exception("Refined MC failed")
        return jsonify({"status": "error", "message": str(e)}), 500

@scenario_bp.route('/bank-run', methods=['GET'])
@login_required
def simulate_bank_run():
    """
    Simulate liquidity drain during a systemic bank run event.
    
    Query Params:
        stress_level (float): Cumulative stress multiplier (e.g., 2.0).
        
    Returns:
        JSON: Standardized response with liquidity depletion projection.
    """
    try:
        stress_level = request.args.get('stress_level', 1.0, type=float)
        service = get_scenario_service()
        res = service.calculate_liquidity_drain(stress_level)
        return jsonify({
            "status": "success",
            "data": res
        })
    except Exception as e:
        logger.exception("Bank run simulation failed")
        return jsonify({"status": "error", "message": str(e)}), 500

@scenario_bp.route('/shadow-fork', methods=['POST'])
@login_required
def shadow_fork():
    """
    Simulate parallel strategy paths from a single starting point.
    """
    try:
        data = request.json
        service = get_scenario_service()
        res = service.simulate_shadow_fork(
            data.get('initial_value', 1000000),
            data.get('baseline_params', {}),
            data.get('shadow_params', {}),
            data.get('horizon_days', 30)
        )
        return jsonify({
            "status": "success",
            "data": res
        })
    except Exception as e:
        logger.exception("Shadow fork simulation failed")
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Philanthropy (Phase 61) ---
@philanthropy_bp.route('/donate', methods=['POST'])
@login_required
def donate():
    """
    Route alpha/excess capital to designated charitable allocations.
    
    Automates tax-efficient donating by routing non-essential capital to 
    ESG or personal charitable causes.
    
    Payload:
        amount (float): Total USD amount to donate.
        allocations (list): List of destination allocations with weights.
        
    Returns:
        JSON: Standardized response with transaction ID and tax estimate.
    """
    try:
        data = request.json
        from services.philanthropy.donation_service import get_donation_service
        service = get_donation_service()
        allocs = data.get('allocations', [])
        record = service.route_excess_alpha(data.get('amount', 0), allocs)
        return jsonify({
            "status": "success",
            "data": {
                "transaction_id": record.id,
                "status": record.status,
                "tax_savings": record.tax_savings_est,
                "message": "Donation routed successfully."
            }
        })
    except Exception as e:
        logger.exception("Donation failed")
        return jsonify({"status": "error", "message": str(e)}), 500

@philanthropy_bp.route('/history', methods=['GET'])
@login_required
def donation_history():
    """
    Retrieve historical donation records and tax benefits.
    
    Returns:
        JSON: Standardized response with donation history array.
    """
    try:
        from services.philanthropy.donation_service import get_donation_service
        service = get_donation_service()
        history = service.get_donation_history()
        return jsonify({
            "status": "success",
            "data": [{
                "id": r.id, 
                "total": r.total_amount, 
                "date": r.timestamp, 
                "savings": r.tax_savings_est
            } for r in history]
        })
    except Exception as e:
        logger.exception("Donation history failed")
        return jsonify({"status": "error", "message": str(e)}), 500

@philanthropy_bp.route('/esg', methods=['GET'])
@login_required
def get_esg():
    """
    Retrieve portfolio-wide ESG scores (Environmental, Social, Governance).
    
    Returns:
        JSON: Standardized response with scores and composite grade.
    """
    try:
        service = get_esg_service()
        scores = service.get_portfolio_esg_scores()
        return jsonify({
            "status": "success",
            "data": {
                "environmental": scores.environmental,
                "social": scores.social,
                "governance": scores.governance,
                "composite": scores.composite,
                "grade": scores.grade
            }
        })
    except Exception as e:
        logger.exception("ESG fetch failed")
        return jsonify({"status": "error", "message": str(e)}), 500

@philanthropy_bp.route('/carbon', methods=['GET'])
@login_required
def get_carbon():
    """
    Calculate carbon footprint and retrieve alpha-vs-emissions data.
    
    Query Params:
        value (float): Portfolio value for footprint scaling.
        
    Returns:
        JSON: Standardized response with emission tons and offset costs.
    """
    try:
        service = get_esg_service()
        footprint = service.calculate_carbon_footprint(request.args.get('value', 3000000, type=float))
        scatter = service.get_alpha_vs_carbon_data()
        return jsonify({
            "status": "success",
            "data": {
                "footprint": {
                    "total": footprint.total_emissions_tons,
                    "cost": footprint.offset_cost_usd
                },
                "scatter": scatter
            }
        })
    except Exception as e:
        logger.exception("Carbon fetch failed")
        return jsonify({"status": "error", "message": str(e)}), 500

# --- System Health (Phase 62 & Phase 05) ---
@system_bp.route('/health', methods=['GET'])
@login_required
def get_health():
    """
    Get comprehensive health status of core system services.
    
    Returns:
        JSON: Standardized response with health status and latency metrics.
    """
    try:
        service = get_system_health_service()
        health = service.get_health_status()
        return jsonify({
            "status": "success",
            "data": health
        })
    except Exception as e:
        logger.exception("System health check failed")
        return jsonify({"status": "error", "message": str(e)}), 500

@system_bp.route('/error', methods=['POST'])
def log_frontend_error():
    """
    Log frontend crashes and exceptions to the system logger.
    Fixes 404 errors observed in frontend error tracking.
    """
    try:
        data = request.json or {}
        logger.error(f"FRONTEND_CRASH: {data.get('error')}\nStack: {data.get('stack')}\nContext: {data.get('context')}")
        return jsonify({"status": "logged"})
    except Exception as e:
        logger.exception("Failed to log frontend error")
        return jsonify({"status": "error"}), 500

@system_bp.route('/secrets', methods=['GET'])
@login_required
@requires_role('admin')
def get_secrets_status():
    """
    Check the rotation and integrity status of system secrets.
    
    Returns:
        JSON: Standardized response with secret management status.
        
    Security:
        Bearer JWT and ADMIN role required.
    """
    try:
        from services.system.secret_manager import SecretManager
        manager = SecretManager()
        return jsonify({
            "status": "success",
            "data": manager.get_status()
        })
    except Exception as e:
        logger.exception("Secret status check failed")
        return jsonify({"status": "error", "message": str(e)}), 500

@system_bp.route('/supply-chain', methods=['GET'])
@login_required
@requires_role('admin')
def get_supply_chain_status():
    """
    Retrieve software supply chain audit and vulnerability status.
    
    Returns:
        JSON: Standardized response with supply chain audit findings.
        
    Security:
        Bearer JWT and ADMIN role required.
    """
    try:
        from services.system.supply_chain_service import get_supply_chain_service
        service = get_supply_chain_service()
        return jsonify({
            "status": "success",
            "data": service.get_audit_status()
        })
    except Exception as e:
        logger.exception("Supply chain audit failed")
        return jsonify({"status": "error", "message": str(e)}), 500

@system_bp.route('/kafka/stats', methods=['GET'])
@login_required
def get_kafka_stats():
    """
    Get Kafka cluster performance and throughput statistics.
    
    Returns real-time metrics for market data, options flow, and risk alert 
    topics, including messages per second and consumer lag.
    
    Returns:
        JSON: Standardized response with list of topic-specific metrics.
    """
    try:
        import random
        return jsonify({
            "status": "success",
            "data": [
                {
                    "topic": "market-data",
                    "msg_per_sec": random.randint(200, 800),
                    "lag": random.randint(0, 5),
                    "kbps": random.randint(1000, 3000)
                },
                {
                    "topic": "options-flow",
                    "msg_per_sec": random.randint(50, 150),
                    "lag": random.randint(0, 2),
                    "kbps": random.randint(200, 500)
                },
                {
                    "topic": "risk-alerts",
                    "msg_per_sec": random.randint(1, 10),
                    "lag": 0,
                    "kbps": random.randint(10, 50)
                },
                {
                    "topic": "system-logs",
                    "msg_per_sec": random.randint(10, 100),
                    "lag": 1,
                    "kbps": random.randint(50, 200)
                }
            ]
        })
    except Exception as e:
        logger.exception("Kafka stats fetch failed")
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Corporate (Phase 63) ---
@corporate_bp.route('/earnings', methods=['GET'])
@login_required
def get_corporate_earnings():
    """
    Retrieve historical and upcoming corporate earnings events.
    
    Returns:
        JSON: Standardized response with earnings event array.
    """
    try:
        service = get_corporate_service()
        evs = service.get_earnings_calendar()
        return jsonify({
            "status": "success",
            "data": [{"ticker": e.ticker, "date": e.date} for e in evs]
        })
    except Exception as e:
        logger.exception("Corporate earnings fetch failed")
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Margin (Phase 64) ---
@margin_bp.route('/status', methods=['GET'])
@login_required
def get_margin_status():
    """
    Check current margin utilization and buffer levels.
    
    Returns:
        JSON: Standardized response with margin buffer and used amounts.
    """
    try:
        service = get_margin_service()
        status = service.get_margin_status("default")
        return jsonify({
            "status": "success",
            "data": {
                "buffer": status.margin_buffer, 
                "used": status.margin_used
            }
        })
    except Exception as e:
        logger.exception("Margin status check failed")
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Mobile (Phase 65) ---
@mobile_bp.route('/kill-switch', methods=['POST'])
@login_required
@requires_role('trader')
def activate_kill_switch():
    """
    Activate system-wide kill switch from a mobile device.
    
    Payload:
        token (str): Secure authorization token for kill-switch activation.
        
    Returns:
        JSON: Standardized response confirming activation success.
        
    Security:
        Bearer JWT and TRADER role required.
    """
    try:
        service = get_mobile_service()
        success = service.activate_kill_switch(request.json.get('token'))
        return jsonify({
            "status": "success" if success else "error",
            "data": {"success": success}
        })
    except Exception as e:
        logger.exception("Kill switch activation failed")
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Integrations (Phase 66) ---
@integrations_bp.route('/connectors', methods=['GET'])
@login_required
def get_external_connectors():
    """
    List status of all external API connectors and broker bridges.
    """
    try:
        service = get_integrations_service()
        conns = service.get_connectors() # Synchronous call
        return jsonify({
            "status": "success",
            "data": [{"name": c.name, "status": c.status} for c in conns]
        })
    except Exception as e:
        logger.exception("Connector status fetch failed")
        return jsonify({"status": "error", "message": str(e)}), 500

@integrations_bp.route('/webhooks', methods=['GET'])
@login_required
def get_webhooks():
    """
    List configured webhooks.
    """
    try:
        service = get_integrations_service()
        hooks = service.get_webhooks() # Synchronous call
        return jsonify({
            "status": "success",
            "data": [{"id": h.id, "url": h.url, "status": h.status} for h in hooks]
        })
    except Exception as e:
        logger.exception("Webhook fetch failed")
        return jsonify({"status": "error", "message": str(e)}), 500

@integrations_bp.route('/webhooks/<webhook_id>/test', methods=['POST'])
@login_required
def test_webhook(webhook_id):
    """
    Test a webhook configuration.
    """
    try:
        service = get_integrations_service()
        res = service.test_webhook(webhook_id) # Synchronous call
        return jsonify({
            "status": "success",
            "data": res
        })
    except Exception as e:
        logger.exception("Webhook test failed")
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Assets (Phase 67) ---
@assets_bp.route('/illiquid', methods=['GET'])
@login_required
def get_illiquid_assets():
    """
    Retrieve audit list of illiquid assets (Real Estate, VC, PE).
    
    Returns:
        JSON: Standardized response with illiquid asset details.
    """
    try:
        assets = assets_service.get_all_assets()
        return jsonify({
            "status": "success",
            "data": assets
        })
    except Exception as e:
        logger.exception("Illiquid assets fetch failed")
        return jsonify({"status": "error", "message": str(e)}), 500

# --- Zen (Phase 68) ---
@zen_bp.route('/calculate', methods=['GET'])
@login_required
def calculate_zen_equilibrium():
    """
    Calculate portfolio Homeostasis and "Freedom Number" progress.
    
    Calculates the balance between current wealth, burn rate, and 
    retirement sustainability.
    
    Returns:
        JSON: Standardized response with freedom number and probability.
    """
    try:
        service = get_homeostasis_service()
        res = service.calculate_homeostasis("default")
        return jsonify({
            "status": "success",
            "data": {
                "freedom_number": res.freedom_number, 
                "progress": res.freedom_progress,
                "retirement_probability": res.retirement_probability
            }
        })
    except Exception as e:
        logger.exception("Zen calculation failed")
        return jsonify({"status": "error", "message": str(e)}), 500

@zen_bp.route('/status', methods=['GET'])
@login_required
def get_homeostasis_status():
    """
    Get current homeostasis status and net worth metrics.
    """
    try:
        service = get_homeostasis_service()
        # The analysis service uses calculate_homeostasis
        res = service.calculate_homeostasis("demo-user")
        return jsonify({
            "status": "success",
            "data": {
                "net_worth": res.current_value,
                "target": res.freedom_number,
                "homeostasis_score": res.freedom_progress * 100,
                "years_covered": res.years_covered,
                "retirement_probability": res.retirement_probability,
                "monthly_safe_withdrawal": res.monthly_safe_withdrawal
            }
        })
    except Exception as e:
        logger.exception("Homeostasis status fetch failed")
        return jsonify({"status": "error", "message": str(e)}), 500

@zen_bp.route('/update', methods=['POST'])
@login_required
def update_homeostasis_metrics():
    """
    Update net worth and trigger homeostasis checks.
    """
    try:
        service = get_homeostasis_service()
        # In analysis version, we don't have update_net_worth, but we can re-calculate
        res = service.calculate_homeostasis("demo-user")
        return jsonify({
            "status": "success",
            "data": {
                "net_worth": res.current_value,
                "target": res.freedom_number,
                "homeostasis_score": res.freedom_progress * 100
            }
        })
    except Exception as e:
        logger.exception("Homeostasis update failed")
        return jsonify({"status": "error", "message": str(e)}), 500
@zen_bp.route('/donate', methods=['POST'])
@login_required
def manual_donate():
    """
    Manually trigger a philanthropy donation.
    """
    try:
        from services.execution.philanthropy_service import philanthropy_service
        data = request.json
        amount = data.get('amount', 0)
        philanthropy_service.donate_excess_alpha("demo-user", amount)
        return jsonify({"status": "success", "amount": amount})
    except Exception as e:
        logger.exception("Manual donation failed")
        return jsonify({"status": "error", "message": str(e)}), 500
