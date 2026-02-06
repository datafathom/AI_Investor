import json
import os

# Simplified registry data based on departmentRegistry.js
DEPT_AGENTS = {
    1: ["synthesizer", "command_interpreter", "traffic_controller", "layout_morphologist", "red_team_sentry", "context_weaver"],
    2: ["life_cycle_modeler", "tax_location_optimizer", "inheritance_logic_agent", "inflation_architect", "real_estate_amortizer", "goal_priority_arbiter"],
    3: ["scraper_general", "backtest_autopilot", "correlation_detective", "anomaly_scout", "yield_optimizer", "macro_correlation_engine"],
    4: ["logic_architect", "stress_tester", "rebalance_bot", "opportunity_screener", "edge_decay_monitor", "playbook_evolutionist"],
    5: ["sniper", "exit_manager", "arbitrageur", "liquidity_scout", "position_sizer", "flash_crash_circuit_breaker"],
    6: ["theta_collector", "volatility_surface_mapper", "gamma_warning_system", "delta_hedger", "probability_modeler", "black_swan_insurance_agent"],
    7: ["deal_flow_scraper", "cap_table_modeler", "exit_catalyst_monitor", "lotto_risk_manager", "whitepaper_summarizer", "asset_hunter"],
    8: ["breach_sentinel", "api_key_rotator", "travel_mode_guard", "cold_storage_auditor", "permission_auditor", "recovery_path_builder"],
    9: ["property_manager", "vehicle_fleet_ledger", "inventory_agent", "procurement_bot", "wellness_sync", "maintenance_scheduler"],
    10: ["bill_automator", "flow_master", "budget_enforcer", "fraud_watchman", "subscription_assassin", "credit_score_sentinel"],
    11: ["wash_sale_watchdog", "document_notary", "kyc_aml_compliance_agent", "tax_loss_harvester", "regulatory_news_ticker", "audit_trail_reconstructor"],
    12: ["slippage_sleuth", "behavioral_analyst", "benchmarker", "fee_forensic_agent", "reconciliation_bot", "mistake_classifier"],
    13: ["advisor_liaison", "subscription_negotiator", "family_office_coordinator", "philanthropy_scout", "professional_crm", "pitch_deck_generator"],
    14: ["inbox_gatekeeper", "calendar_concierge", "voice_advocate", "logistics_researcher", "document_courier", "executive_buffer"],
    15: ["journal_entry_agent", "regime_classifier", "ghost_decision_overlay", "pattern_recognition_bot", "decision_replay_engine", "timeline_curator"],
    16: ["war_game_simulator", "black_swan_randomizer", "liquidation_optimizer", "cascade_failure_detector", "recovery_path_planner", "robustness_scorer"],
    17: ["hallucination_sentinel", "token_efficiency_reaper", "agent_performance_reviewer", "prompt_optimizer", "model_router", "context_window_manager"],
    18: ["transaction_categorizer", "ach_wire_tracker", "envelope_budget_manager", "recurring_payment_agent", "tax_reserve_calculator", "interest_arbitrage_scout"]
}

def generate_definitions():
    definitions = []
    for dept_id, agents in DEPT_AGENTS.items():
        for agent_slug in agents:
            name = agent_slug.replace("_", " ").title()
            definitions.append({
                "id": agent_slug,
                "dept_id": dept_id,
                "name": name,
                "role": f"Specialized agent for {name} within Department {dept_id}",
                "inputs": ["kafka_stream", "postgres_context"],
                "processing": "LLM-enhanced logic with domain-specific tools",
                "outputs": ["telemetry_event", "state_update"],
                "llm_model": "claude-3-5-sonnet",
                "timeout_seconds": 30
            })
    
    config_dir = "config"
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        
    with open(os.path.join(config_dir, "agent_definitions.json"), "w") as f:
        json.dump(definitions, f, indent=2)
    print(f"Generated {len(definitions)} agent definitions.")

if __name__ == "__main__":
    generate_definitions()
