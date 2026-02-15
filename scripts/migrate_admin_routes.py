"""
===============================================================================
FILE: scripts/migrate_admin_routes.py
ROLE: Batch Admin-to-Dept Route Migration Generator
PURPOSE: Creates workstation placeholder JSX files and generates updated
         route test files and departmentRegistry.js subModule entries for
         all departments with /admin/ routes.
===============================================================================
"""

import os
import json
from pathlib import Path
from typing import Dict, List, Tuple

PROJECT_ROOT = Path(__file__).parent.parent

# ─────────────────────────────────── CONFIG ───────────────────────────────────
# Maps: admin-slug -> (target-dept-slug, new-sub-slug, label, description)
# The target-dept-slug must match the workstation folder name
# The new-sub-slug is the new URL segment under the dept

ADMIN_TO_DEPT_MAP: Dict[str, Tuple[str, str, str, str]] = {
    # ═══════════════ AUDITOR ═══════════════
    "attribution-analysis": ("auditor", "attribution-analysis", "Attribution Analysis", "Deep attribution analysis for portfolio decomposition."),
    "discrepancy-resolution": ("auditor", "discrepancy-resolution", "Discrepancy Resolution", "Automated resolution of ledger discrepancies."),
    "fee-auditor": ("auditor", "fee-auditor", "Fee Auditor", "Commission and fee analysis for hidden cost discovery."),
    "model-validator": ("auditor", "model-validator", "Model Validator", "Validating financial model accuracy and drift."),
    "performance-attribution": ("auditor", "performance-attribution", "Performance Attribution", "Decomposing returns by sector, decision, and timing."),
    "performance-report": ("auditor", "performance-report", "Performance Report", "Comprehensive performance reporting and analytics."),
    "pricing-verifier": ("auditor", "pricing-verifier", "Pricing Verifier", "Cross-referencing asset prices from multiple providers."),
    "quality-incidents": ("auditor", "quality-incidents", "Quality Incidents", "Tracking and resolving data quality incidents."),
    "reconciliation-dashboard": ("auditor", "reconciliation-dashboard", "Reconciliation Dashboard", "Unified view of cash and position breaks."),
    "source-reputation": ("auditor", "source-reputation", "Source Reputation", "Rating reliability of data sources and feeds."),
    "tax-lot-analyzer": ("auditor", "tax-lot-analyzer", "Tax Lot Analyzer", "FIFO/LIFO lot analysis for tax optimization."),
    "wealth-benchmark": ("auditor", "wealth-benchmark", "Wealth Benchmark", "Benchmarking wealth growth against indices."),

    # ═══════════════ BANKER ═══════════════
    "account-aggregator": ("banker", "account-aggregator", "Account Aggregator", "Unified view of all external account balances."),
    "bank-manager": ("banker", "bank-manager", "Bank Manager", "Managing institutional bank relationships and accounts."),
    "crypto-wallet": ("banker", "crypto-wallet", "Crypto Wallet", "Managing cryptocurrency wallets and DeFi positions."),
    "defi-yield-dashboard": ("banker", "defi-yield-dashboard", "DeFi Yield Dashboard", "Tracking yield farming and DeFi protocol returns."),
    "expense-manager": ("banker", "expense-manager", "Expense Manager", "Categorizing and tracking all outgoing expenditures."),
    "tax-liability-dashboard": ("banker", "tax-liability-dashboard", "Tax Liability Dashboard", "Real-time estimated tax obligation tracker."),
    "transaction-ledger": ("banker", "transaction-ledger", "Transaction Ledger", "Master record of all financial movements."),
    "transaction-sync": ("banker", "transaction-sync", "Transaction Sync", "Synchronizing transactions across institutions."),
    "transfer-center": ("banker", "transfer-center", "Transfer Center", "Initiating and tracking inter-account transfers."),
    "treasury-dashboard": ("banker", "treasury-dashboard", "Treasury Dashboard", "Master view of all bank balances and liquidity."),
    "yield-optimizer": ("banker", "yield-optimizer", "Yield Optimizer", "Optimizing savings and yield across accounts."),

    # ═══════════════ DATA SCIENTIST ═══════════════
    "backtest-engine": ("data-scientist", "backtest-engine", "Backtest Engine", "High-fidelity backtesting with transaction costs."),
    "correlation-risk": ("data-scientist", "correlation-risk", "Correlation Risk", "Identifying hidden correlation clusters across assets."),
    "crypto-analytics": ("data-scientist", "crypto-analytics", "Crypto Analytics", "On-chain and market analytics for digital assets."),
    "data-pipeline-manager": ("data-scientist", "data-pipeline-manager", "Data Pipeline Manager", "Orchestrating data ingestion and transformation flows."),
    "data-quality-dashboard": ("data-scientist", "data-quality-dashboard", "Data Quality Dashboard", "Monitoring data freshness, completeness, and accuracy."),
    "data-validation": ("data-scientist", "data-validation", "Data Validation", "Automated validation rules for incoming data streams."),

    # ═══════════════ ENVOY ═══════════════
    "donation-manager": ("envoy", "donation-manager", "Donation Manager", "Tracking and managing charitable contributions."),
    "giving-opportunity-finder": ("envoy", "giving-opportunity-finder", "Giving Opportunity Finder", "Discovering tax-advantaged giving opportunities."),
    "impact-scorecard": ("envoy", "impact-scorecard", "Impact Scorecard", "Measuring social and environmental investment impact."),
    "investor-portal": ("envoy", "investor-portal", "Investor Portal", "Shared view for co-investors and partners."),
    "philanthropy-center": ("envoy", "philanthropy-center", "Philanthropy Center", "Centralized management for philanthropic initiatives."),

    # ═══════════════ FRONT OFFICE ═══════════════
    "executive-summary": ("front-office", "executive-summary", "Executive Summary", "High-level overview of institutional health and alpha."),

    # ═══════════════ HUNTER ═══════════════
    "on-chain-terminal": ("hunter", "on-chain-terminal", "On-Chain Terminal", "Real-time blockchain transaction monitoring."),
    "opportunity-tracker": ("hunter", "opportunity-tracker", "Opportunity Tracker", "Tracking alpha opportunities across markets."),
    "private-equity-terminal": ("hunter", "private-equity-terminal", "Private Equity Terminal", "Deal flow and PE fund analytics."),
    "watchlist-manager": ("hunter", "watchlist-manager", "Watchlist Manager", "Managing and monitoring asset watchlists."),

    # ═══════════════ LAWYER ═══════════════
    "compliance-tracker": ("lawyer", "compliance-tracker", "Compliance Tracker", "Monitoring regulatory compliance status."),
    "doc-generator": ("lawyer", "doc-generator", "Doc Generator", "Automated legal document generation."),
    "filing-manager": ("lawyer", "filing-manager", "Filing Manager", "Managing tax filings and regulatory submissions."),
    "tax-harvester": ("lawyer", "tax-harvester", "Tax Harvester", "Automated tax-loss harvesting engine."),
    "trade-surveillance": ("lawyer", "trade-surveillance", "Trade Surveillance", "Monitoring for insider trading and unusual patterns."),
    "trust-admin": ("lawyer", "trust-admin", "Trust Admin", "Managing trusts and fiduciary structures."),

    # ═══════════════ ORCHESTRATOR ═══════════════
    "autonomy-controller": ("orchestrator", "autonomy-controller", "Autonomy Controller", "Configuring agent autonomy levels and boundaries."),
    "consensus-visualizer": ("orchestrator", "consensus-visualizer", "Consensus Visualizer", "Visualizing agent consensus and conflict resolution."),
    "fleet": ("orchestrator", "fleet", "Agent Fleet", "Status and lifecycle management for all active agents."),
    "os-health-dashboard": ("orchestrator", "os-health-dashboard", "OS Health Dashboard", "Operating system health and resource monitoring."),
    "singularity": ("orchestrator", "singularity", "Singularity", "Advanced system convergence metrics."),
    "system-health": ("orchestrator", "system-health", "System Health", "CPU, Memory, and Disk usage metrics."),
    "tactical-command-center": ("orchestrator", "tactical-command-center", "Tactical Command Center", "Mission-critical command and control interface."),
    "task-queue": ("orchestrator", "task-queue", "Task Queue", "Managing agent task queues and priorities."),
    "unified-alert-center": ("orchestrator", "unified-alert-center", "Unified Alert Center", "Centralized notification and alert management."),

    # ═══════════════ PHYSICIST ═══════════════
    "greeks-surface": ("physicist", "greeks-surface", "Greeks Surface", "3D volatility surface for options Greeks."),
    "options-flow": ("physicist", "options-flow", "Options Flow", "Real-time institutional options order flow."),
    "pnl-modeler": ("physicist", "pnl-modeler", "P&L Modeler", "Scenario-based P&L projection for derivatives."),
    "position-greeks": ("physicist", "position-greeks", "Position Greeks", "Aggregate Greeks for the entire portfolio."),

    # ═══════════════ REFINER ═══════════════
    "agent-dna": ("refiner", "agent-dna", "Agent DNA Viewer", "Inspecting agent configuration and prompt DNA."),
    "autocoder": ("refiner", "autocoder", "Auto-Coder Dashboard", "Self-improving logic and code generation."),
    "evolution": ("refiner", "evolution", "Evolution Engine", "Tracking agent capability evolution over time."),
    "meta-optimizer": ("refiner", "meta-optimizer", "Meta Optimizer", "Optimizing optimizer parameters and hypertuning."),
    "prompt-tester": ("refiner", "prompt-tester", "Prompt Tester", "A/B testing prompts for agent performance."),

    # ═══════════════ SENTRY ═══════════════
    "api-key-manager": ("sentry", "api-key-manager", "API Key Manager", "Managing and rotating API keys and tokens."),
    "fraud-center": ("sentry", "fraud-center", "Fraud Center", "Centralized fraud detection and response."),
    "security-center": ("sentry", "security-center", "Security Center", "Consolidated security posture and vulnerabilities."),
    "security-logs": ("sentry", "security-logs", "Security Logs", "Detailed security event and access logs."),
    "warden-panel": ("sentry", "warden-panel", "Warden Panel", "Admin control panel for security protocols."),

    # ═══════════════ STEWARD ═══════════════
    "asset-inventory": ("steward", "asset-inventory", "Asset Inventory", "Tracking physical and digital asset holdings."),
    "collectible-viewer": ("steward", "collectible-viewer", "Collectible Viewer", "Viewing and managing collectible asset portfolio."),
    "exit-planner": ("steward", "exit-planner", "Exit Planner", "Planning liquidation and exit strategies."),

    # ═══════════════ STRATEGIST ═══════════════
    "rebalancer": ("strategist", "rebalancer", "Rebalancer", "Automated portfolio rebalancing engine."),
    "risk-dashboard": ("strategist", "risk-dashboard", "Risk Dashboard", "Comprehensive risk metrics and analytics."),
    "screener-builder": ("strategist", "screener-builder", "Screener Builder", "Building custom asset screening criteria."),
    "strategy-lab": ("strategist", "strategy-lab", "Strategy Lab", "Experimental strategy development environment."),
    "strategy-library": ("strategist", "strategy-library", "Strategy Library", "Repository of tested trading strategies."),
    "walk-forward": ("strategist", "walk-forward", "Walk Forward Analysis", "Out-of-sample strategy validation testing."),

    # ═══════════════ STRESS TESTER ═══════════════
    "black-swan-generator": ("stress-tester", "black-swan-generator", "Black Swan Generator", "Generating extreme tail-risk scenarios."),
    "crash-simulator": ("stress-tester", "crash-simulator", "Crash Simulator", "Simulating market crashes and recovery paths."),
    "liquidity-stress": ("stress-tester", "liquidity-stress", "Liquidity Stress", "Testing portfolio liquidity under stress conditions."),
    "robustness-lab": ("stress-tester", "robustness-lab", "Robustness Lab", "Testing strategy robustness under adversarial conditions."),
    "wargame-arena": ("stress-tester", "wargame-arena", "Wargame Arena", "Multi-agent adversarial simulation environment."),
    "web3-simulator": ("stress-tester", "web3-simulator", "Web3 Simulator", "Simulating DeFi protocol interactions and risks."),

    # ═══════════════ TRADER ═══════════════
    "algo-order-entry": ("trader", "algo-order-entry", "Algo Order Entry", "Algorithmic order entry and scheduling."),
    "bracket-manager": ("trader", "bracket-manager", "Bracket Manager", "Managing bracket and OCO order setups."),
    "dark-pool-access": ("trader", "dark-pool-access", "Dark Pool Access", "Routing orders to dark liquidity pools."),
    "execution-analytics": ("trader", "execution-analytics", "Execution Analytics", "Post-trade analysis of execution quality."),
    "iceberg-slicer": ("trader", "iceberg-slicer", "Iceberg Slicer", "Breaking large orders into hidden iceberg slices."),
    "multi-leg-builder": ("trader", "multi-leg-builder", "Multi-Leg Builder", "Building complex multi-leg options strategies."),
    "order-management": ("trader", "order-management", "Order Management", "Live status of all active and pending orders."),
    "position-sizer": ("trader", "position-sizer", "Position Sizer", "Calculating optimal position sizes by risk budget."),
    "risk-limits": ("trader", "risk-limits", "Risk Limits", "Configuring hard loss limits and circuit breakers."),
    "smart-router": ("trader", "smart-router", "Smart Router", "Intelligent order routing for best execution."),
}

# Template for NOT_IMPLEMENTED workstation placeholder
WORKSTATION_TEMPLATE = """import React from 'react';
import '../Workstation.css';

const {component_name} = () => {{
    return (
        <div className="workstation-container">
            <header className="workstation-header">
                <div className="status-dot pulse"></div>
                <h1>{label} <span className="text-slate-500">//</span> WORKSTATION</h1>
                <div className="flex-1"></div>
                <div className="security-badge">SECURE_CHANNEL_v1.2</div>
            </header>

            <div className="workstation-grid">
                <div className="workstation-main bg-slate-900/50 border border-slate-800 rounded-lg p-6">
                    <h2 className="text-cyan-400 font-mono text-xs uppercase tracking-widest mb-4">Functional Module: {label}</h2>
                    <p className="text-slate-400 font-mono text-sm leading-relaxed mb-6">
                        {description}
                    </p>
                    
                    <div className="boilerplate-container terminal-box bg-black/80 rounded border border-slate-700 p-4 font-mono text-[10px] text-cyan-500/80">
                        <div className="mb-1">&gt; INITIALIZING {component_name}...</div>
                        <div className="mb-1">&gt; SYNCING NEURAL MESH...</div>
                        <div className="mb-1">&gt; ESTABLISHING HANDSHAKE WITH AGENTIC LAYER...</div>
                        <div className="text-green-500">&gt; READY.</div>
                    </div>
                </div>

                <div className="workstation-sidebar flex flex-col gap-4">
                    <div className="bg-slate-900/50 border border-slate-800 rounded-lg p-4">
                        <h3 className="text-slate-500 font-mono text-[10px] uppercase mb-2">Metrics</h3>
                        <div className="metric-row border-b border-slate-800/50 py-2">
                            <span className="text-slate-400 text-xs">Latency:</span>
                            <span className="text-cyan-400 text-xs float-right">12ms</span>
                        </div>
                        <div className="metric-row py-2">
                            <span className="text-slate-400 text-xs">Uptime:</span>
                            <span className="text-cyan-400 text-xs float-right">99.9%</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}};

export default {component_name};
"""


def to_pascal_case(slug: str) -> str:
    """Convert kebab-case to PascalCase: 'attribution-analysis' -> 'AttributionAnalysis'"""
    return "".join(word.capitalize() for word in slug.split("-"))


def to_dept_pascal(dept_slug: str) -> str:
    """Convert dept slug to prefix: 'data-scientist' -> 'Datascientist'"""
    parts = dept_slug.split("-")
    return "".join(word.capitalize() for word in parts)


def generate_component_name(dept_slug: str, sub_slug: str) -> str:
    """Generate component name matching existing convention: DeptSub"""
    dept_prefix = to_dept_pascal(dept_slug)
    sub_pascal = to_pascal_case(sub_slug)
    # Remove hyphens for component naming consistency
    return f"{dept_prefix}{sub_pascal}"


def create_workstation_file(dept_slug: str, sub_slug: str, label: str, description: str) -> str:
    """Create a workstation JSX placeholder file. Returns the relative path."""
    component_name = generate_component_name(dept_slug, sub_slug)
    
    workstation_dir = PROJECT_ROOT / "Frontend" / "src" / "pages" / "workstations" / dept_slug
    workstation_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = workstation_dir / f"{component_name}.jsx"
    
    # Skip if file already exists (preserve existing work)
    if file_path.exists():
        return f"SKIPPED (exists): {file_path.relative_to(PROJECT_ROOT)}"
    
    content = WORKSTATION_TEMPLATE.format(
        component_name=component_name,
        label=label,
        description=description,
    )
    
    file_path.write_text(content, encoding="utf-8")
    return f"CREATED: {file_path.relative_to(PROJECT_ROOT)}"


def generate_submodule_entries() -> Dict[str, List[dict]]:
    """Generate subModule entries grouped by department for departmentRegistry.js"""
    by_dept: Dict[str, List[dict]] = {}
    
    for admin_slug, (dept_slug, sub_slug, label, description) in ADMIN_TO_DEPT_MAP.items():
        if dept_slug not in by_dept:
            by_dept[dept_slug] = []
        
        path = f"/{dept_slug}/{sub_slug}"
        by_dept[dept_slug].append({
            "path": path,
            "label": label,
            "description": description,
        })
    
    return by_dept


def generate_route_file(dept_name: str, dept_slug: str, routes: List[str]) -> str:
    """Generate updated route test file content."""
    var_name = f"{dept_name.upper()}_ROUTES"
    header = f'"""\nDEPARTMENT: {dept_name.upper()}\nGenerated from Registry + Route Migration (admin -> dept-specific)\n"""\n\n'
    
    routes_str = ",\n".join(f'    "{r}"' for r in sorted(routes))
    return f'{header}{var_name} = [\n{routes_str},\n]\n'


def get_updated_routes_for_dept(dept_name: str, dept_slug: str, 
                                 original_routes: List[str]) -> List[str]:
    """Replace /admin/ URLs with dept-specific equivalents."""
    new_routes = []
    
    for route in original_routes:
        url_path = route.replace("http://localhost:5173", "")
        
        if url_path.startswith("/admin/"):
            admin_slug = url_path.replace("/admin/", "").rstrip("/")
            
            if admin_slug in ADMIN_TO_DEPT_MAP:
                target_dept, new_sub, _, _ = ADMIN_TO_DEPT_MAP[admin_slug]
                new_url = f"http://localhost:5173/{target_dept}/{new_sub}"
                new_routes.append(new_url)
            else:
                # Admin route not in our map — keep as-is (belongs to admin dept)
                print(f"  WARNING: {admin_slug} not in map for {dept_name}, keeping /admin/ URL")
                new_routes.append(route)
        else:
            new_routes.append(route)
    
    return new_routes


def main() -> None:
    print("=" * 70)
    print("ADMIN-TO-DEPT ROUTE MIGRATION")
    print("=" * 70)
    
    # Step 1: Create workstation placeholder files
    print("\n--- STEP 1: Creating Workstation Placeholders ---")
    created_count = 0
    skipped_count = 0
    
    for admin_slug, (dept_slug, sub_slug, label, desc) in sorted(ADMIN_TO_DEPT_MAP.items()):
        result = create_workstation_file(dept_slug, sub_slug, label, desc)
        if "CREATED" in result:
            created_count += 1
        else:
            skipped_count += 1
        print(f"  {result}")
    
    print(f"\n  Summary: {created_count} created, {skipped_count} skipped (already exist)")
    
    # Step 2: Generate subModule entries for the registry
    print("\n--- STEP 2: SubModule Entries (for departmentRegistry.js) ---")
    by_dept = generate_submodule_entries()
    
    # Write to a temporary JSON for reference 
    output_path = PROJECT_ROOT / "DEBUGGING" / "FrontEndAudit" / "admin_migration_submodules.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(by_dept, indent=2), encoding="utf-8")
    print(f"  Written to: {output_path.relative_to(PROJECT_ROOT)}")
    
    # Step 3: Update route test files
    print("\n--- STEP 3: Updating Route Test Files ---")
    
    # Define dept info: (file_name, dept_name, dept_slug, var_name)
    dept_configs = [
        ("auditor_routes.py", "AUDITOR", "auditor"),
        ("banker_routes.py", "BANKER", "banker"),
        ("datascientist_routes.py", "DATASCIENTIST", "data-scientist"),
        ("envoy_routes.py", "ENVOY", "envoy"),
        ("frontoffice_routes.py", "FRONTOFFICE", "front-office"),
        ("guardian_routes.py", "GUARDIAN", "guardian"),
        ("historian_routes.py", "HISTORIAN", "historian"),
        ("hunter_routes.py", "HUNTER", "hunter"),
        ("lawyer_routes.py", "LAWYER", "lawyer"),
        ("orchestrator_routes.py", "ORCHESTRATOR", "orchestrator"),
        ("physicist_routes.py", "PHYSICIST", "physicist"),
        ("refiner_routes.py", "REFINER", "refiner"),
        ("sentry_routes.py", "SENTRY", "sentry"),
        ("special_routes.py", "SPECIAL", "special"),
        ("steward_routes.py", "STEWARD", "steward"),
        ("strategist_routes.py", "STRATEGIST", "strategist"),
        ("stresstester_routes.py", "STRESSTESTER", "stress-tester"),
        ("trader_routes.py", "TRADER", "trader"),
    ]
    
    routes_dir = PROJECT_ROOT / "DEBUGGING" / "FrontEndAudit" / "Routes2Test" / "depts"
    
    for file_name, dept_name, dept_slug in dept_configs:
        file_path = routes_dir / file_name
        if not file_path.exists():
            print(f"  SKIP: {file_name} not found")
            continue
        
        # Read existing routes
        content = file_path.read_text(encoding="utf-8")
        
        # Extract URLs from the file
        import re
        urls = re.findall(r'"(http://localhost:5173/[^"]+)"', content)
        
        if not urls:
            print(f"  SKIP: {file_name} — no URLs found")
            continue
        
        # Count admin routes
        admin_count = sum(1 for u in urls if "/admin/" in u)
        
        # Get updated routes
        new_routes = get_updated_routes_for_dept(dept_name, dept_slug, urls)
        
        # Generate the updated file
        var_name = f"{dept_name}_ROUTES"
        header = f'"""\nDEPARTMENT: {dept_name}\nGenerated from Registry + Route Migration (admin -> dept-specific)\n"""\n\n'
        routes_str = ",\n".join(f'    "{r}"' for r in new_routes)
        new_content = f'{header}{var_name} = [\n{routes_str},\n]\n'
        
        file_path.write_text(new_content, encoding="utf-8")
        print(f"  UPDATED: {file_name} ({admin_count} admin routes migrated)")
    
    print("\n" + "=" * 70)
    print("MIGRATION COMPLETE")
    print("=" * 70)
    print("\nNext steps:")
    print("  1. Update departmentRegistry.js with new subModules (see admin_migration_submodules.json)")
    print("  2. Verify `vite build` compiles without errors")
    print("  3. Run verification for each department")


if __name__ == "__main__":
    main()
