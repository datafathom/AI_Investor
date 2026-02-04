import json
import re
import os

# Original file list from Step 200 (Preserves Order)
ORIGINAL_FILES = [
    "000_init_users.sql", # Move this first manually as users are usually dependency for linked accounts
    "000_init_linked_accounts.sql",
    "017_equity_curves.sql",
    "019_sl_audit.sql",
    "020_kill_switch_events.sql",
    "021_circuit_breaker.sql",
    "022_trading_locks.sql",
    "023_risk_config.sql",
    "045_strategies.sql",
    "066_api_quotas.sql",
    "66_fund_data.sql", # Was 66_fund_data
    "101_advisors.sql",
    "102_index_fund_master.sql",
    "103_emergency_fund.sql",
    "104_employer_match.sql",
    "105_ira_optimization.sql",
    "106_concentration_alerts.sql",
    "107_professional_roles.sql",
    "108_529_plans.sql",
    "108_spending_analyzer.sql",
    "109_private_banking.sql",
    "109_tax_deferral.sql",
    "110_platform_ledger.sql",
    "111_insurance_providers.sql",
    "112_price_discovery.sql",
    "113_reconstitution_log.sql",
    "114_fee_billing.sql",
    "116_international_holdings.sql",
    "118_pension_schedules.sql",
    "122_risk_free_rates.sql",
    "123_drawdown_events.sql",
    "124_reit_holdings.sql",
    "129_index_concentration.sql",
    "130_depreciation.sql",
    "132_operational_workload.sql",
    "134_specialized_reit.sql",
    "135_goal_milestones.sql",
    "136_margin_history.sql",
    "137_education_ledger.sql",
    "138_risk_metrics.sql",
    "139_risk_free_rates.sql",
    "141_trust_stipulations.sql",
    "142_trust_funding_status.sql",
    "143_tax_lots.sql",
    "144_spendthrift_rules.sql",
    "145_gst_ledger.sql",
    "146_ppli_ledger.sql",
    "147_crt_distributions.sql",
    "150_exchange_timers.sql",
    "152_probate_meta.sql",
    "153_testamentary_instructions.sql",
    "155_mediation_log.sql",
    "156_crummey_notices.sql",
    "157_state_investments.sql",
    "158_justification_log.sql",
    "159_fee_accrual.sql",
    "161_sfo_mfo_budget.sql",
    "163_staff_pe_performance.sql",
    "166_syndication_lending.sql",
    "168_ppli_dark_assets_heirs.sql",
    "171_credit_premium.sql",
    "173_waitlist_concierge.sql",
    "178_constitution.sql",
    "178_constitution_crm.sql",
    "179_network_crm.sql",
    "180_global_risk_bridge.sql",
    "181_mtm_gaps.sql",
    "183_fatca_exit_tax_rule144.sql",
    "186_trading_plans_toxicity.sql",
    "187_visa_geopolitics.sql",
    "191_relocation_esg.sql",
    "194_yield_arb_drs.sql",
    "196_market_integrity.sql",
    "197_lifestyle_economics.sql",
    "phase1_001_user_workspaces.sql",
    "phase1_001_user_workspaces_rollback.sql",
    "phase2_002_fear_greed.sql",
    "phase2_002_fear_greed_rollback.sql",
    "phase2_003_hypemeter.sql",
    "phase2_003_hypemeter_rollback.sql",
    "phase6_004_legal_documents.sql",
    "phase6_004_legal_documents_rollback.sql",
    "phase6_005_user_onboarding.sql",
    "phase6_005_user_onboarding_rollback.sql",
    "phase10_006_trade_journal.sql",
    "phase13_007_debate_logs.sql",
    "phase_18_optimization.sql",
    "phase_29_audit_logs.sql",
    "phase_30_legal_consents.sql"
]

def get_new_name(filename):
    new_name = filename
    
    # Logic matches rename_schemas.py
    match_phase = re.match(r"^phase\d*_\d{3}_(.*)", filename)
    if match_phase:
        new_name = match_phase.group(1)
    else:
        match_phase_simple = re.match(r"^phase_\d+_(.*)", filename)
        if match_phase_simple:
            new_name = match_phase_simple.group(1)
        else:
            match_digits = re.match(r"^\d+_(.*)", filename)
            if match_digits:
                new_name = match_digits.group(1)
    return new_name

def main():
    manifest = []
    
    for original in ORIGINAL_FILES:
        # We generally include rollbacks in the manifest for completeness, 
        # though migrate.py mostly cares about forward migrations.
        # But migrate.py FILTERS OUT rollbacks.
        # Let's include everything in the manifest, the runner can filter.
        
        new_name = get_new_name(original)
        manifest.append(new_name)
        
    output_path = r"c:\Users\astir\Desktop\AI_Company\AI_Investor\schemas\postgres\schema_manifest.json"
    
    with open(output_path, "w") as f:
        json.dump(manifest, f, indent=2)
        
    print(f"Manifest generated at {output_path} with {len(manifest)} entries.")

if __name__ == "__main__":
    main()
