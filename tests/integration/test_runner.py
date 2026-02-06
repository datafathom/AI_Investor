"""
Test Runner Handlers for CLI
All test runner functionality integrated directly into CLI system
"""

import subprocess
import sys
import os
from pathlib import Path
from typing import Optional, List

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

_project_root = Path(__file__).parent.parent.parent


# Test category definitions
TEST_CATEGORIES = {
    'backend': {
        'name': 'Backend Services',
        'paths': [
            'tests/analytics',
            'tests/optimization',
            'tests/risk',
            'tests/tax',
            'tests/options',
            'tests/trading',
            'tests/strategy',
            'tests/planning',
            'tests/budgeting',
            'tests/billing',
            'tests/credit',
            'tests/retirement',
            'tests/estate',
            'tests/news',
            'tests/watchlist',
            'tests/research',
            'tests/social_trading',
            'tests/community',
            'tests/education',
            'tests/charting',
            'tests/analysis',
            'tests/ai_predictions',
            'tests/ai_assistant',
            'tests/ml',
            'tests/integration',
            'tests/marketplace',
            'tests/compliance',
            'tests/institutional',
            'tests/public_api',
            'tests/enterprise',
        ],
        'description': 'All backend service tests (Phases 1-4)'
    },
    'backend-phase1': {
        'name': 'Backend Phase 1 - Critical Services',
        'paths': [
            'tests/analytics',
            'tests/optimization',
            'tests/risk',
            'tests/tax',
        ],
        'description': 'Critical analytics, optimization, risk, and tax services'
    },
    'backend-phase2': {
        'name': 'Backend Phase 2 - Core Features',
        'paths': [
            'tests/options',
            'tests/trading',
            'tests/strategy',
            'tests/planning',
            'tests/retirement',
            'tests/estate',
            'tests/budgeting',
            'tests/credit',
        ],
        'description': 'Core feature services (options, trading, planning, etc.)'
    },
    'backend-phase3': {
        'name': 'Backend Phase 3 - Supporting Features',
        'paths': [
            'tests/news',
            'tests/watchlist',
            'tests/research',
            'tests/social_trading',
            'tests/community',
            'tests/education',
            'tests/charting',
            'tests/analysis',
        ],
        'description': 'Supporting feature services (news, watchlist, research, etc.)'
    },
    'backend-phase4': {
        'name': 'Backend Phase 4 - Platform Features',
        'paths': [
            'tests/ai_predictions',
            'tests/ai_assistant',
            'tests/ml',
            'tests/integration',
            'tests/marketplace',
            'tests/compliance',
            'tests/institutional',
            'tests/public_api',
            'tests/enterprise',
        ],
        'description': 'Platform feature services (AI, ML, integrations, etc.)'
    },
    'frontend': {
        'name': 'Frontend Components',
        'paths': ['frontend2/tests/pages'],
        'description': 'All frontend React component tests'
    },
    'api': {
        'name': 'API Endpoints',
        'paths': ['tests/api'],
        'description': 'All API endpoint tests'
    },
    'api-analytics': {
        'name': 'Analytics APIs',
        'paths': [
            'tests/api/test_analytics_api.py',
            'tests/api/test_attribution_api.py',
        ],
        'description': 'Analytics and attribution API tests'
    },
    'api-trading': {
        'name': 'Trading APIs',
        'paths': [
            'tests/api/test_options_api.py',
            'tests/api/test_paper_trading_api.py',
            'tests/api/test_advanced_orders_api.py',
            'tests/api/test_strategy_api.py',
            'tests/api/test_brokerage_api.py',
            'tests/api/test_robinhood_api.py',
            'tests/api/test_ibkr_api.py',
        ],
        'description': 'Trading and brokerage API tests'
    },
    'api-payments': {
        'name': 'Payment APIs',
        'paths': [
            'tests/api/test_stripe_api.py',
            'tests/api/test_paypal_api.py',
            'tests/api/test_venmo_api.py',
            'tests/api/test_square_api.py',
            'tests/api/test_coinbase_api.py',
            'tests/api/test_coinbase_crypto_api.py',
        ],
        'description': 'Payment processing API tests'
    },
    'api-crypto': {
        'name': 'Crypto APIs',
        'paths': [
            'tests/api/test_crypto_api.py',
            'tests/api/test_ethereum_api.py',
            'tests/api/test_solana_api.py',
            'tests/api/test_binance_api.py',
            'tests/api/test_web3_api.py',
        ],
        'description': 'Cryptocurrency and blockchain API tests'
    },
    'api-social': {
        'name': 'Social Media APIs',
        'paths': [
            'tests/api/test_discord_api.py',
            'tests/api/test_stocktwits_api.py',
            'tests/api/test_youtube_api.py',
            'tests/api/test_social_api.py',
            'tests/api/test_facebook_auth_api.py',
            'tests/api/test_facebook_hype_api.py',
        ],
        'description': 'Social media and sentiment API tests'
    },
    'api-integrations': {
        'name': 'Integration APIs',
        'paths': [
            'tests/api/test_integration_api.py',
            'tests/api/test_integrations_api.py',
            'tests/api/test_plaid_api.py',
            'tests/api/test_banking_api.py',
            'tests/api/test_gmail_api.py',
            'tests/api/test_calendar_api.py',
            'tests/api/test_documents_api.py',
        ],
        'description': 'Third-party integration API tests'
    },
    'api-notifications': {
        'name': 'Notification APIs',
        'paths': [
            'tests/api/test_twilio_api.py',
            'tests/api/test_slack_api.py',
            'tests/api/test_email_api.py',
            'tests/api/test_incident_api.py',
        ],
        'description': 'Notification and communication API tests'
    },
    'api-auth': {
        'name': 'Authentication APIs',
        'paths': [
            'tests/api/test_auth_api.py',
            'tests/api/test_google_auth_api.py',
            'tests/api/test_facebook_auth_api.py',
        ],
        'description': 'Authentication and OAuth API tests'
    },
    'api-financial': {
        'name': 'Financial Planning APIs',
        'paths': [
            'tests/api/test_financial_planning_api.py',
            'tests/api/test_retirement_api.py',
            'tests/api/test_estate_api.py',
            'tests/api/test_budgeting_api.py',
            'tests/api/test_billing_api.py',
            'tests/api/test_credit_api.py',
        ],
        'description': 'Financial planning and management API tests'
    },
    'api-ai': {
        'name': 'AI & ML APIs',
        'paths': [
            'tests/api/test_ai_predictions_api.py',
            'tests/api/test_ai_assistant_api.py',
            'tests/api/test_ml_training_api.py',
            'tests/api/test_autocoder_api.py',
            'tests/api/test_ai_autocoder_api.py',
        ],
        'description': 'AI, ML, and automation API tests'
    },
    'api-platform': {
        'name': 'Platform APIs',
        'paths': [
            'tests/api/test_enterprise_api.py',
            'tests/api/test_compliance_api.py',
            'tests/api/test_institutional_api.py',
            'tests/api/test_education_api.py',
            'tests/api/test_marketplace_api.py',
            'tests/api/test_public_api_endpoints.py',
        ],
        'description': 'Platform and enterprise API tests'
    },
    'api-market': {
        'name': 'Market Data APIs',
        'paths': [
            'tests/api/test_market_data_api.py',
            'tests/api/test_macro_api.py',
            'tests/api/test_macro_data_api.py',
            'tests/api/test_charting_api.py',
            'tests/api/test_news_api.py',
            'tests/api/test_watchlist_api.py',
        ],
        'description': 'Market data and analysis API tests'
    },
    'api-risk': {
        'name': 'Risk Management APIs',
        'paths': [
            'tests/api/test_risk_api.py',
            'tests/api/test_advanced_risk_api.py',
            'tests/api/test_margin_api.py',
            'tests/api/test_backtest_api.py',
            'tests/api/test_scenario_api.py',
        ],
        'description': 'Risk management and analysis API tests'
    },
    'api-tax': {
        'name': 'Tax APIs',
        'paths': [
            'tests/api/test_tax_api.py',
            'tests/api/test_tax_optimization_api.py',
            'tests/api/test_taxbit_api.py',
        ],
        'description': 'Tax optimization and reporting API tests'
    },
    'api-other': {
        'name': 'Other APIs',
        'paths': [
            'tests/api/test_workspace_api.py',
            'tests/api/test_dashboard_api.py',
            'tests/api/test_identity_api.py',
            'tests/api/test_privacy_api.py',
            'tests/api/test_legal_api.py',
            'tests/api/test_settlement_api.py',
            'tests/api/test_cash_api.py',
            'tests/api/test_cash_api_flask.py',
            'tests/api/test_assets_api.py',
            'tests/api/test_fixed_income_api.py',
            'tests/api/test_corporate_api.py',
            'tests/api/test_philanthropy_api.py',
            'tests/api/test_politics_api.py',
            'tests/api/test_communication_api.py',
            'tests/api/test_briefing_api.py',
            'tests/api/test_debate_api.py',
            'tests/api/test_evolution_api.py',
            'tests/api/test_homeostasis_api.py',
            'tests/api/test_spatial_api.py',
            'tests/api/test_system_api.py',
            'tests/api/test_mobile_api.py',
            'tests/api/test_kyc_api.py',
            'tests/api/test_kyc_api_flask.py',
            'tests/api/test_wave_apis.py',
        ],
        'description': 'Miscellaneous API tests'
    },
    'models': {
        'name': 'Pydantic Models',
        'paths': ['tests/models'],
        'description': 'All Pydantic model validation tests'
    },
    'models-core': {
        'name': 'Core Models',
        'paths': [
            'tests/models/test_analytics_models.py',
            'tests/models/test_optimization_models.py',
            'tests/models/test_risk_models.py',
            'tests/models/test_options_models.py',
            'tests/models/test_strategy_models.py',
        ],
        'description': 'Core business logic models'
    },
    'models-financial': {
        'name': 'Financial Models',
        'paths': [
            'tests/models/test_financial_planning_models.py',
            'tests/models/test_retirement_models.py',
            'tests/models/test_estate_models.py',
            'tests/models/test_budgeting_models.py',
            'tests/models/test_billing_models.py',
            'tests/models/test_credit_models.py',
        ],
        'description': 'Financial planning and management models'
    },
    'models-platform': {
        'name': 'Platform Models',
        'paths': [
            'tests/models/test_enterprise_models.py',
            'tests/models/test_compliance_models.py',
            'tests/models/test_institutional_models.py',
            'tests/models/test_public_api_models.py',
            'tests/models/test_marketplace_models.py',
            'tests/models/test_integration_models.py',
        ],
        'description': 'Platform and infrastructure models'
    },
    'models-ai': {
        'name': 'AI & ML Models',
        'paths': [
            'tests/models/test_ai_predictions_models.py',
            'tests/models/test_ai_assistant_models.py',
            'tests/models/test_ml_training_models.py',
        ],
        'description': 'AI and machine learning models'
    },
    'models-social': {
        'name': 'Social & Community Models',
        'paths': [
            'tests/models/test_social_trading_models.py',
            'tests/models/test_community_models.py',
            'tests/models/test_news_models.py',
            'tests/models/test_watchlist_models.py',
            'tests/models/test_research_models.py',
        ],
        'description': 'Social trading and community models'
    },
    'models-other': {
        'name': 'Other Models',
        'paths': [
            'tests/models/test_paper_trading_models.py',
            'tests/models/test_orders_models.py',
            'tests/models/test_education_models.py',
        ],
        'description': 'Other model tests'
    },
    'all': {
        'name': 'All Tests',
        'paths': ['tests', 'frontend2/tests'],
        'description': 'Run all tests across the entire application'
    },
    'unit': {
        'name': 'Unit Tests',
        'paths': [
            'tests/analytics',
            'tests/optimization',
            'tests/risk',
            'tests/tax',
            'tests/options',
            'tests/trading',
            'tests/strategy',
            'tests/planning',
            'tests/budgeting',
            'tests/billing',
            'tests/credit',
            'tests/retirement',
            'tests/estate',
            'tests/news',
            'tests/watchlist',
            'tests/research',
            'tests/social_trading',
            'tests/community',
            'tests/education',
            'tests/charting',
            'tests/analysis',
            'tests/ai_predictions',
            'tests/ai_assistant',
            'tests/ml',
            'tests/integration',
            'tests/marketplace',
            'tests/compliance',
            'tests/institutional',
            'tests/public_api',
            'tests/enterprise',
            'tests/models',
        ],
        'description': 'All unit tests (services and models)'
    },
    'integration': {
        'name': 'Integration Tests',
        'paths': ['tests/api', 'frontend2/tests'],
        'description': 'Integration tests (APIs and frontend)'
    },
    'quick': {
        'name': 'Quick Test Suite',
        'paths': [
            'tests/analytics',
            'tests/optimization',
            'tests/api/test_analytics_api.py',
            'tests/api/test_optimization_api.py',
        ],
        'description': 'Quick smoke tests for critical paths'
    },
}


def list_test_categories():
    """List all available test categories."""
    print("\nAvailable Test Categories:\n")
    for category, config in sorted(TEST_CATEGORIES.items()):
        print(f"  {category:20} - {config['name']}")
        print(f"  {'':20}   {config['description']}\n")
    return 0


def run_test_category(
    category: str = None,
    verbose: bool = False,
    coverage: bool = False,
    parallel: bool = False,
    fail_fast: bool = False,
    html: bool = False,
    marker: Optional[List[str]] = None
):
    """Run tests for a specific category."""
    if category not in TEST_CATEGORIES:
        print(f"Error: Unknown category '{category}'")
        print("\nUse 'python cli.py test list' to see available categories")
        return 1
    
    config = TEST_CATEGORIES[category]
    paths = config['paths']
    
    print(f"\nRunning {config['name']}...")
    print(f"   {config['description']}\n")
    
    # Build pytest command
    cmd = ['pytest']
    
    # Add test paths
    for path in paths:
        full_path = _project_root / path
        if full_path.exists():
            cmd.append(str(path))
        else:
            print(f"Warning: Path not found: {path}")
    
    # Add options
    if verbose:
        cmd.append('-v')
    else:
        cmd.append('-q')
    
    if coverage:
        cmd.extend([
            '--cov=services',
            '--cov=web',
            '--cov=agents',
            '--cov=models',
            '--cov=utils',
            '--cov-report=term-missing',
            '--cov-report=html:htmlcov',
        ])
    
    if marker:
        for m in marker:
            cmd.extend(['-m', m])
    
    if parallel:
        cmd.extend(['-n', 'auto'])  # Requires pytest-xdist
    
    if fail_fast:
        cmd.append('-x')
    
    if html:
        cmd.append('--html=report.html')
        cmd.append('--self-contained-html')
    
    print(f"Command: {' '.join(cmd)}\n")
    
    # Run tests
    try:
        result = subprocess.run(cmd, cwd=_project_root)
        return result.returncode
    except KeyboardInterrupt:
        print("\n\nTests interrupted by user")
        return 130
    except Exception as e:
        print(f"\nError running tests: {e}")
        return 1

