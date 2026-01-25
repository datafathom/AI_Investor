
import os

with open('web/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_imports = [
    "from web.api.advanced_orders_api import advanced_orders_bp",
    "from web.api.advanced_orders_api import execution_bp",
    "from web.api.advanced_risk_api import advanced_risk_bp",
    "from web.api.advanced_risk_api import risk_bp",
    "from web.api.ai_assistant_api import ai_assistant_bp",
    "from web.api.ai_autocoder_api import ai_autocoder_bp",
    "from web.api.ai_autocoder_api import autocoder_bp",
    "from web.api.ai_predictions_api import ai_predictions_bp",
    "from web.api.analytics_api import analytics_bp",
    "from web.api.assets_api import assets_bp",
    "from web.api.attribution_api import attribution_bp",
    "from web.api.auth_api import auth_bp",
    "from web.api.banking_api import banking_bp",
    "from web.api.billing_api import billing_bp",
    "from web.api.binance_api import binance_bp",
    "from web.api.briefing_api import briefing_bp",
    "from web.api.brokerage_api import brokerage_bp",
    "from web.api.budgeting_api import budgeting_bp",
    "from web.api.calendar_api import calendar_bp",
    "from web.api.cash_api_flask import cash_bp",
    "from web.api.charting_api import charting_bp",
    "from web.api.coinbase_api import coinbase_bp",
    "from web.api.coinbase_crypto_api import coinbase_crypto_bp",
    "from web.api.communication_api import communication_bp",
    "from web.api.community_api import forum_bp",
    "from web.api.community_api import qa_bp",
    "from web.api.compliance_api import compliance_bp",
    "from web.api.credit_api import credit_bp",
    "from web.api.crypto_api import crypto_api_bp",
    "from web.api.dashboard_api import dashboard_bp",
    "from web.api.debate_api import debate_bp",
    "from web.api.discord_api import discord_bp",
    "from web.api.docs_api import docs_bp",
    "from web.api.documents_api import documents_bp",
    "from web.api.education_api import education_bp",
    "from web.api.email_api import email_api_bp",
    "from web.api.enterprise_api import enterprise_bp",
    "from web.api.estate_api import estate_bp",
    "from web.api.ethereum_api import ethereum_bp",
    "from web.api.evolution_api import evolution_bp",
    "from web.api.facebook_auth_api import facebook_auth_bp",
    "from web.api.facebook_hype_api import facebook_hype_bp",
    "from web.api.financial_planning_api import financial_planning_bp",
    "from web.api.fixed_income_api import fixed_income_bp",
    "from web.api.gmail_api import gmail_bp",
    "from web.api.google_auth_api import google_auth_bp",
    "from web.api.health_api import health_bp",
    "from web.api.homeostasis_api import homeostasis_api",
    "from web.api.ibkr_api import ibkr_bp",
    "from web.api.identity_api import identity_api",
    "from web.api.incident_api import incident_api_bp",
    "from web.api.institutional_api import institutional_bp",
    "from web.api.integration_api import integration_bp",
    "from web.api.kyc_api_flask import kyc_bp",
    "from web.api.legal_api import legal_bp",
    "from web.api.macro_api import macro_bp",
    "from web.api.macro_data_api import macro_data_bp",
    "from web.api.market_data_api import market_data_bp",
    "from web.api.marketplace_api import marketplace_bp",
    "from web.api.ml_training_api import ml_training_bp",
    "from web.api.news_api import news_bp",
    "from web.api.optimization_api import optimization_bp",
    "from web.api.options_api import options_bp",
    "from web.api.paper_trading_api import paper_trading_bp",
    "from web.api.paper_trading_api import simulation_bp",
    "from web.api.paypal_api import paypal_bp",
    "from web.api.plaid_api import plaid_bp",
    "from web.api.politics_api import politics_bp",
    "from web.api.privacy_api import privacy_bp",
    "from web.api.public_api_endpoints import public_api_bp",
    "from web.api.research_api import research_bp",
    "from web.api.retirement_api import retirement_bp",
    "from web.api.robinhood_api import robinhood_bp",
    "from web.api.settlement_api import settlement_bp",
    "from web.api.social_api import social_bp",
    "from web.api.social_trading_api import social_trading_bp",
    "from web.api.solana_api import solana_bp",
    "from web.api.spatial_api import spatial_bp",
    "from web.api.square_api import square_bp",
    "from web.api.stocktwits_api import stocktwits_bp",
    "from web.api.strategy_api import strategy_bp",
    "from web.api.stripe_api import stripe_bp",
    "from web.api.tax_api import tax_api_bp",
    "from web.api.tax_optimization_api import tax_optimization_bp",
    "from web.api.taxbit_api import taxbit_bp",
    "from web.api.twilio_api import twilio_api_bp",
    "from web.api.venmo_api import venmo_bp",
    "from web.api.watchlist_api import alert_bp",
    "from web.api.watchlist_api import watchlist_bp",
    "from web.api.wave_apis import backtest_bp, corporate_bp, integrations_bp, margin_bp, mobile_bp, philanthropy_bp, scenario_bp, system_bp, zen_bp",
    "from web.api.web3_api import web3_bp",
    "from web.api.workspace_api import workspace_bp",
    "from web.api.youtube_api import youtube_bp",
    "from web.routes.market_routes import market_bp",
    "from web.routes.system_routes import system_bp as system_routes_bp"
]

in_create_app = False
final_lines = []
imports_injected = False

for line in lines:
    if 'def create_app()' in line:
        in_create_app = True
    
    if in_create_app:
        if "if __name__ == '__main__':" in line:
            in_create_app = False
        
        # Comment out any local import
        if 'from web.api' in line or 'from web.routes' in line or 'import' in line and ('_bp' in line or 'api' in line) and 'from' in line:
            final_lines.append("    # " + line.strip() + " # REMOVED LOCAL\n")
            continue

    # Comment out any top-level web.api/web.routes import we are replacing
    if not in_create_app and ('from web.api' in line or 'from web.routes' in line):
        if not imports_injected:
            final_lines.append("\n# --- FINAL STABILIZED IMPORTS ---\n")
            for imp in new_imports:
                final_lines.append(f"{imp}\n")
            final_lines.append("# --------------------------------\n\n")
            imports_injected = True
        final_lines.append("# " + line)
        continue

    final_lines.append(line)

with open('web/app.py.final', 'w', encoding='utf-8') as f:
    f.writelines(final_lines)
