import re
import os
from pathlib import Path

def categorize_routes():
    project_root = Path(__file__).parent.parent.parent
    input_file = project_root / "DEBUGGING" / "FrontEndAudit" / "Routes2Test" / "_NEW_ROUTES.txt"
    round2_file = project_root / "DEBUGGING" / "FrontEndAudit" / "Routes2Test" / "verification_round_2.py"
    output_dir = project_root / "DEBUGGING" / "FrontEndAudit" / "Routes2Test" / "depts"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    all_extracted_urls = set()
    
    # 1. Read from _NEW_ROUTES.txt
    if input_file.exists():
        content = input_file.read_text(encoding='utf-8')
        url_pattern = r'http://localhost:5173[^\s\)\],]+'
        all_extracted_urls.update(re.findall(url_pattern, content))
    else:
        print(f"Warning: Input file not found: {input_file}")

    # 2. Read from verification_round_2.py
    if round2_file.exists():
        content = round2_file.read_text(encoding='utf-8')
        url_pattern = r'http://localhost:5173[^\s\)\],"]+'
        all_extracted_urls.update(re.findall(url_pattern, content))
    else:
        print(f"Warning: Round 2 file not found: {round2_file}")

    # Department Config with Registry Sub-Modules and ULTIMATE Keywords
    dept_config = {
        "orchestrator": {
            "slug": "orchestrator",
            "dashboard": "/dept/orchestrator",
            "subpages": [
                "/special/terminal", "/special/mission-control", "/special/homeostasis", 
                "/special/command", "/special/venn", "/orchestrator/graph", 
                "/special/search", "/orchestrator/permissions", "/orchestrator/layout"
            ],
            "keywords": ["/orchestrator/", "autopilot", "fleet", "task-queue", "autonomy-controller", "consensus-visualizer", "tactical-command", "unified-alert", "os-health", "system-health", "singularity"]
        },
        "architect": {
            "slug": "architect",
            "dashboard": "/dept/architect",
            "subpages": [
                "/architect/goals", "/architect/allocation", "/architect/blueprints", 
                "/architect/vault", "/architect/legacy", "/architect/liability", 
                "/architect/tax", "/architect/inflation", "/architect/retirement", "/architect/capex"
            ],
            "keywords": ["/architect/", "protection", "legacy-storytelling", "construction-lab", "real-estate-suite"]
        },
        "datascientist": {
            "slug": "data-scientist",
            "dashboard": "/dept/data-scientist",
            "subpages": [
                "/data-scientist/research", "/data-scientist/debate", "/data-scientist/debate-history",
                "/data-scientist/forced-sellers", "/data-scientist/whale-flow", "/data-scientist/indicators",
                "/data-scientist/backtest", "/data-scientist/correlation", "/data-scientist/sentiment",
                "/data-scientist/social-sentiment-radar", "/data-scientist/anomaly", "/data-scientist/yield",
                "/data-scientist/arbitrage", "/data-scientist/factor-analysis", "/data-scientist/fundamental-scanner",
                "/data-scientist/quant-backtest", "/data-scientist/integrator"
            ],
            "keywords": ["/data-scientist/", "/analyst/", "/pioneer/", "/special/debate", "forced-seller", "whale-flow", "indicator", "heatmap", "debate/room", "debate-arena", "predict", "training", "data-pipeline", "data-quality", "data-validation", "external-data", "backtest-engine", "correlation-risk", "crypto-analytics"]
        },
        "strategist": {
            "slug": "strategist",
            "dashboard": "/dept/strategist",
            "subpages": [
                "/strategist/builder", "/strategist/risk", "/strategist/screener", 
                "/strategist/stress-test", "/strategist/rebalance", "/strategist/alpha-beta", 
                "/strategist/hub", "/strategist/decay", "/strategist/library"
            ],
            "keywords": ["/strategist/", "/special/strategy", "risk-management", "strategy-lab", "strategy-library", "walk-forward", "risk-dashboard", "rebalancer", "screener-builder"]
        },
        "trader": {
            "slug": "trader",
            "dashboard": "/dept/trader",
            "subpages": [
                "/trader/execution", "/trader/monitor", "/trader/options", "/trader/depth", 
                "/trader/pad", "/trader/tape", "/trader/zen", "/trader/ladder", 
                "/trader/slippage", "/trader/routing"
            ],
            "keywords": ["/trader/", "manual-execution", "options-chain", "market-depth", "execution-pad", "trade-tape", "ladder-interface", "slippage-estimator", "order-entry", "dark-pool", "charts/advanced", "charts/technical", "advanced-orders", "algorithmic-trading", "paper-trading", "options-strategy", "bracket-manager", "iceberg-slicer", "order-management", "smart-router", "execution-analytics", "order-management", "risk-limits", "multi-leg-builder", "position-sizer"]
        },
        "physicist": {
            "slug": "physicist",
            "dashboard": "/dept/physicist",
            "subpages": ["/physicist/margin", "/physicist/morphing", "/physicist/expected-move"],
            "keywords": ["/physicist/", "strategy-morphing", "greeks", "surface", "pnl-modeler", "options-flow", "position-greeks"]
        },
        "hunter": {
            "slug": "hunter",
            "dashboard": "/dept/hunter",
            "subpages": [
                "/hunter/pipeline", "/hunter/cap-tables", "/hunter/pulse", "/hunter/unusual-options",
                "/hunter/news-aggregator", "/hunter/social-trading-feed", "/hunter/rumor-mill",
                "/hunter/moonshots", "/hunter/ipo-monitor", "/hunter/collectibles",
                "/hunter/crowdfunding", "/hunter/exits", "/hunter/rumors", "/hunter/mining"
            ],
            "keywords": ["/hunter/", "/marketing/", "venture-pipeline", "cap-table", "market-pulse", "unusual-options", "news", "social-trading", "rumor-mill", "ipo", "exit-strategy", "speculative-news", "resource-mining", "marketplace", "watchlist-manager", "opportunity-tracker", "on-chain-terminal", "private-equity-terminal"]
        },
        "sentry": {
            "slug": "sentry",
            "dashboard": "/dept/sentry",
            "subpages": [
                "/sentry/vault", "/sentry/encryption", "/sentry/firewall", "/sentry/dark-web",
                "/sentry/devices", "/sentry/geo-logs", "/sentry/kill-switch", "/sentry/backups",
                "/sentry/hardware", "/sentry/audit"
            ],
            "keywords": ["/sentry/", "credential-vault", "encryption-status", "logical-firewall", "dark-web", "device-authorization", "ip-access", "kill-protocol", "backup-integrity", "hardware-wallet", "perimeter-audit", "warden", "security-center", "security-logs", "api-key", "permissions", "fraud-center"]
        },
        "steward": {
            "slug": "steward",
            "dashboard": "/dept/steward",
            "subpages": ["/steward/maintenance", "/steward/kill-list", "/steward/liquidity"],
            "keywords": ["/steward/", "maintenance-reserve", "subscription-kill", "net-worth-vs-liquid", "asset-inventory", "real-estate", "collectible-viewer", "exit-planner"]
        },
        "guardian": {
            "slug": "guardian",
            "dashboard": "/dept/guardian",
            "subpages": [
                "/guardian/bills", "/guardian/loom", "/guardian/budgeting", "/guardian/forecast",
                "/guardian/fraud", "/guardian/emergency", "/guardian/ladder", "/guardian/tax-buffer", "/guardian/sweep"
            ],
            "keywords": ["/guardian/", "bill-payment", "emergency-fund", "liquidity-ladder", "tax-safe", "sweep"]
        },
        "lawyer": {
            "slug": "lawyer",
            "dashboard": "/dept/lawyer",
            "subpages": [
                "/lawyer/logs", "/lawyer/library", "/legal/144a-compliance", "/lawyer/journal",
                "/lawyer/vault", "/lawyer/harvest", "/lawyer/wash-sale", "/lawyer/regulation",
                "/lawyer/beneficiaries", "/lawyer/signatures", "/lawyer/compliance"
            ],
            "keywords": ["/lawyer/", "/legal/", "audit-log", "precedent", "document-vault", "tax-harvest", "wash-sale", "trade-surveillance", "filing-manager", "doc-generator", "compliance-tracker", "trust-admin"]
        },
        "auditor": {
            "slug": "auditor",
            "dashboard": "/dept/auditor",
            "subpages": [
                "/auditor/equity", "/auditor/fees", "/auditor/ledger", "/auditor/equity-curve",
                "/auditor/psychology", "/auditor/attribution", "/auditor/mistakes",
                "/auditor/benchmarks", "/auditor/time-weighted", "/auditor/recovery"
            ],
            "keywords": ["/auditor/", "equity-reconciliation", "fee-leakage", "immutable-ledger", "reconciliation", "tax-lot", "pricing-verifier", "source-reputation", "quality-incidents", "discrepancy", "fee-auditor", "model-validator", "performance-report", "performance-attribution", "attribution-analysis", "wealth-benchmark"]
        },
        "envoy": {
            "slug": "envoy",
            "dashboard": "/dept/envoy",
            "subpages": [
                "/envoy/advisor", "/envoy/pitch", "/envoy/inbox", "/envoy/contacts",
                "/envoy/subscriptions", "/envoy/family", "/envoy/education", "/envoy/daf",
                "/envoy/share", "/envoy/crm"
            ],
            "keywords": ["/envoy/", "advisor-portal", "strategic-inbox", "investor-portal", "philanthropy", "donation", "impact-scorecard", "giving-opportunity", "donation-manager", "philanthropy-center"]
        },
        "frontoffice": {
            "slug": "front-office",
            "dashboard": "/dept/front-office",
            "subpages": ["/orchestrator/terminal", "/orchestrator/mission-control"],
            "keywords": ["/front-office/", "inbox-gatekeeper", "calendar", "voice-advocate", "logistics", "courier", "executive-buffer", "executive-summary"]
        },
        "historian": {
            "slug": "historian",
            "dashboard": "/dept/historian",
            "subpages": ["/historian/replay", "/historian/regime", "/historian/patterns"],
            "keywords": ["/historian/", "replay", "regime", "pattern", "history"]
        },
        "stresstester": {
            "slug": "stress-tester",
            "dashboard": "/dept/stress-tester",
            "subpages": ["/stress-tester/wargame", "/stress-tester/liquidation", "/stress-tester/robustness"],
            "keywords": ["/stress-tester/", "liquidation", "robustness", "black-swan", "crash-simulator", "liquidity-stress", "wargame", "web3-simulator", "black-swan-generator", "robustness-lab", "war-game-arena"]
        },
        "refiner": {
            "slug": "refiner",
            "dashboard": "/dept/refiner",
            "subpages": ["/refiner/efficiency", "/refiner/hallucination", "/refiner/prompts"],
            "keywords": ["/refiner/", "meta-optimizer", "agent-dna", "prompt-tester", "autocoder", "evolution"]
        },
        "banker": {
            "slug": "banker",
            "dashboard": "/dept/banker",
            "subpages": ["/banker/ledger", "/banker/recovery", "/banker/sweep"],
            "keywords": ["/banker/", "transaction-categorizer", "ach-wire", "envelope-budget", "recurring-payment", "tax-reserve", "interest-arbitrage", "transaction-sync", "bank-manager", "treasury", "transaction-ledger", "expense-manager", "yield-optimizer", "tax-harvester", "tax-liability", "account-aggregator", "crypto-wallet", "defi-yield", "transfer-center", "tax-lot-analyzer"]
        },
        "admin": {
            "slug": "admin",
            "dashboard": "/dept/admin",
            "subpages": [
                "/admin/logs", "/admin/event-bus", "/admin/storage", "/admin/health", 
                "/admin/deployments", "/admin/fleet", "/admin/autocoder", "/admin/system-health", 
                "/admin/executive-summary", "/admin/order-management"
            ],
            "keywords": ["/admin/"]
        }
    }
    
    check_order = list(dept_config.keys())
    categorized = {dept: set() for dept in check_order}
    special = set()
    
    # 1. Start with Sub-Modules for each dept (guaranteed from registry)
    for dept, cfg in dept_config.items():
        base_url = "http://localhost:5173"
        for sub in cfg["subpages"]:
            categorized[dept].add(f"{base_url}{sub}")
            
    # 2. Add routes from ALL sources based on keywords
    for url in all_extracted_urls:
        matched = False
        path = url.replace("http://localhost:5173", "").lower()
        if not path: continue
        
        # Check departments in order (Admin is last)
        for dept in check_order:
            keywords = dept_config[dept]["keywords"]
            for kw in keywords:
                if kw.lower() in path:
                    categorized[dept].add(url)
                    matched = True
                    break
            if matched: break
        
        if not matched:
            special.add(url)
            
    # Write files
    for dept in check_order:
        dept_urls = sorted(list(categorized[dept]))
        cfg = dept_config[dept]
        dashboard_url = f"http://localhost:5173{cfg['dashboard']}"
        
        # Remove if already in list to avoid double entry
        if dashboard_url in dept_urls:
            dept_urls.remove(dashboard_url)
            
        # Prepend dashboard to the list
        dept_urls.insert(0, dashboard_url)
        
        filename = f"{dept}_routes.py"
        filepath = output_dir / filename
        
        lines = [
            '"""',
            f'DEPARTMENT: {dept.upper()}',
            'Generated from Registry + Ultimate Keyword Mapping (Union of Sources)',
            '"""',
            '',
            f'{dept.upper().replace("-", "_")}_ROUTES = ['
        ]
        for u in dept_urls:
            lines.append(f"    \"{u}\",")
        lines.append("]")
        
        filepath.write_text("\n".join(lines), encoding='utf-8')
        print(f"Wrote {len(dept_urls)} routes to {filename}")
        
    # Write special (should be empty but keeping for logic)
    special_file = output_dir / "special_routes.py"
    lines = [
        '"""',
        'SPECIAL ROUTES (Uncategorized)',
        '"""',
        '',
        'SPECIAL_ROUTES = ['
    ]
    for u in sorted(list(special)):
        lines.append(f"    \"{u}\",")
    lines.append("]")
    special_file.write_text("\n".join(lines), encoding='utf-8')

if __name__ == "__main__":
    categorize_routes()
