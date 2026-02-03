import os
import re

api_dir = 'web/api'
files = [f for f in os.listdir(api_dir) if f.endswith('.py')]

# Blueprint map from app.py and user request
BP_MAP = {
    'auth_bp': '/api/v1/auth',
    'privacy_bp': '/api/v1/privacy',
    'legal_bp': '/api/v1/legal',
    'onboarding_bp': '/api/v1/onboarding',
    'banking_bp': '/api/v1/banking',
    'billing_bp': '/api/v1/billing',
    'crypto_api_bp': '/api/v1/crypto',
    'advanced_orders_bp': '/api/v1/orders',
    'execution_bp': '/api/v1/execution',
    'paper_trading_bp': '/api/v1/paper',
    'simulation_bp': '/api/v1/simulation',
    'strategy_bp': '/api/v1/strategy',
    'watchlist_bp': '/api/v1/watchlist',
    'alert_bp': '/api/v1/alert',
    'kyc_bp': '/api/v1/kyc',
    'cash_bp': '/api/v1/cash',
    'backtest_bp': '/api/v1/backtest',
    'estate_bp': '/api/v1/estate',
    'compliance_bp': '/api/v1/compliance',
    'scenario_bp': '/api/v1/scenario',
    'philanthropy_bp': '/api/v1/philanthropy',
    'system_bp': '/api/v1/system',
    'corporate_bp': '/api/v1/corporate',
    'margin_bp': '/api/v1/margin',
    'mobile_bp': '/api/v1/mobile',
    'integrations_bp': '/api/v1/integrations',
    'zen_bp': '/api/v1/homeostasis',
    'market_data_bp': '/api/v1/market',
    'macro_data_bp': '/api/v1/macro_data',
    'macro_bp': '/api/v1/macro',
    'economics_bp': '/api/v1/economics',
    'analytics_bp': '/api/v1/analytics',
    'optimization_bp': '/api/v1/optimization',
    'advanced_risk_bp': '/api/v1/risk',
    'tax_optimization_bp': '/api/v1/tax_optimization',
    'options_bp': '/api/v1/options',
    'financial_planning_bp': '/api/v1/financial_planning',
    'retirement_bp': '/api/v1/retirement',
    'budgeting_bp': '/api/v1/budgeting',
    'credit_bp': '/api/v1/credit',
    'news_bp': '/api/v1/news',
    'forum_bp': '/api/v1/forum',
    'qa_bp': '/api/v1/qa',
    'debate_bp': '/api/v1/debate',
    'briefing_bp': '/api/v1/briefing',
    'research_bp': '/api/v1/research',
    'ai_predictions_bp': '/api/v1/ai_predictions',
    'ai_assistant_bp': '/api/v1/ai_assistant',
    'google_auth_bp': '/api/v1/google_auth',
    'gmail_bp': '/api/v1/gmail',
    'calendar_bp': '/api/v1/calendar',
    'facebook_auth_bp': '/api/v1/facebook_auth',
    'facebook_hype_bp': '/api/v1/facebook_hype',
    'ibkr_bp': '/api/v1/ibkr',
    'robinhood_bp': '/api/v1/robinhood',
    'ethereum_bp': '/api/v1/ethereum',
    'solana_bp': '/api/v1/solana',
    'coinbase_bp': '/api/v1/coinbase',
    'coinbase_crypto_bp': '/api/v1/coinbase_crypto',
    'stocktwits_bp': '/api/v1/stocktwits',
    'discord_bp': '/api/v1/discord',
    'youtube_bp': '/api/v1/youtube',
    'stripe_bp': '/api/v1/stripe',
    'paypal_bp': '/api/v1/paypal',
    'venmo_bp': '/api/v1/venmo',
    'square_bp': '/api/v1/square',
    'plaid_bp': '/api/v1/plaid',
    'binance_bp': '/api/v1/binance',
    'tax_api_bp': '/api/v1/tax_api',
    'taxbit_bp': '/api/v1/taxbit',
    'twilio_api_bp': '/api/v1/twilio',
    'email_api_bp': '/api/v1/email',
    'incident_api_bp': '/api/v1/incident',
    'communication_bp': '/api/v1/communication',
    'evolution_bp': '/api/v1/evolution',
    'documents_bp': '/api/v1/documents',
    'identity_api': '/api/v1/identity',
    'education_bp': '/api/v1/education',
    'spatial_bp': '/api/v1/spatial',
    'fixed_income_bp': '/api/v1/fixed_income',
    'web3_bp': '/api/v1/web3',
    'scanner_bp': '/api/v1/scanner',
    'payment_transfer_bp': '/api/v1/payment_transfer',
    'search_bp': '/api/v1/search',
    'institutional_bp': '/api/v1/institutional',
    'ml_training_bp': '/api/v1/ml',
    'integration_bp': '/api/v1/integration',
    'marketplace_bp': '/api/v1/marketplace',
    'enterprise_bp': '/api/v1/enterprise',
    'social_bp': '/api/v1/social',
    'social_trading_bp': '/api/v1/social_trading'
}

for filename in files:
    path = os.path.join(api_dir, filename)
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    modified = False
    for bp_name, prefix in BP_MAP.items():
        if bp_name in content:
            # Look for Blueprint call
            if 'url_prefix=' in content:
                # Replace existing url_prefix
                # Pattern: Blueprint(..., url_prefix='...')
                # We need to be careful with the blueprint name vs the variable name
                pattern = rf"(Blueprint\([^,]+,\s*__name__,\s*url_prefix=)['\"][^'\"]+['\"]"
                new_content = re.sub(pattern, rf"\1'{prefix}'", content)
                if new_content != content:
                    content = new_content
                    modified = True
            else:
                # Add url_prefix
                pattern = rf"({bp_name}\s*=\s*Blueprint\([^)]+)"
                replacement = rf"\1, url_prefix='{prefix}'"
                new_content = re.sub(pattern, replacement, content)
                if new_content != content:
                    content = new_content
                    modified = True
                    
    if modified:
        print(f'Syncing {filename}')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
