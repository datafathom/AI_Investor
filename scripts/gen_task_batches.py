
import os

api_dir = r'c:\Users\astir\Desktop\AI_Company\AI_Investor\web\api'
already_batched = {
    'stripe', 'auth', 'ai_autocoder', 'autocoder',
    'banking', 'cash', 'legal', 'identity', 'kyc', 'billing', 'budgeting', 'financial_planning', 'news', 'community', 'education', 'retirement', 'charting', 'institutional',
    'advanced_orders', 'advanced_risk', 'ai_assistant', 'ai_predictions', 'analytics', 'assets', 'attribution', 'backtest', 'binance', 'briefing', 'brokerage', 'calendar', 'coinbase', 'coinbase_crypto', 'communication', 'compliance', 'corporate', 'dashboard', 'documents', 'risk',
    'credit', 'crypto', 'debate', 'dev', 'discord', 'economics', 'email', 'enterprise', 'estate', 'ethereum', 'evolution', 'facebook_auth', 'facebook_hype', 'fixed_income', 'gmail',
    'google_auth', 'health', 'homeostasis', 'ibkr', 'incident', 'integration', 'integrations', 'macro', 'macro_data', 'margin', 'market_data', 'marketplace', 'ml_training', 'mobile', 'optimization'
}

all_apis = [f.replace('_api.py', '') for f in os.listdir(api_dir) if f.endswith('_api.py')]
# Also check for files that don't end in _api.py but are API files (like wave_apis.py)
all_apis += [f.replace('.py', '') for f in os.listdir(api_dir) if f.endswith('.py') and '_api' not in f]

# clean up names
clean_apis = []
for api in all_apis:
    name = api.replace('_api', '').replace('_apis', '')
    clean_apis.append(name)

unique_apis = sorted(list(set(clean_apis)))

remaining = [api for api in unique_apis if api not in already_batched]

# Remove some non-api files if any
ignored = {'__init__', 'fastapi_gateway', 'base_api', 'api_utils'}
remaining = [api for api in remaining if api not in ignored]

for i in range(0, len(remaining), 15):
    batch_num = 6 + (i // 15)
    print(f"    - [ ] Batch {batch_num}: (15 files)")
    for api in remaining[i:i+15]:
        print(f"        - [ ] test_{api}_api.py")
