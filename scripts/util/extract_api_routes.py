
import os
import ast
import json
import re

def extract_routes_from_file(filepath, url_prefix=""):
    routes = []
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        
    # Basic regex to find routes and methods
    # e.g., @auth_bp.route('/login', methods=['POST'])
    route_pattern = re.compile(r'@[\w_]+\.route\((?P<path>[\'"][^\'"]+[\'"])(?:,\s*methods=\[(?P<methods>[^\]]+)\])?\)')
    
    # Also find blueprints to get their base url_prefix if defined in the file
    blueprint_pattern = re.compile(r'Blueprint\([\'"](?P<name>\w+)[\'"],\s*__name__,\s*url_prefix=(?P<prefix>[\'"][^\'"]+[\'"])\)')
    local_prefix = ""
    bp_match = blueprint_pattern.search(content)
    if bp_match:
        local_prefix = bp_match.group('prefix').strip("'").strip('"')

    # Use AST for better docstring extraction
    try:
        tree = ast.parse(content)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                # Check for route decorators
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Call) and getattr(decorator.func, 'attr', '') == 'route':
                        path = ""
                        methods = ["GET"] # Default Flask method
                        
                        if decorator.args:
                            if isinstance(decorator.args[0], ast.Constant):
                                path = decorator.args[0].value
                            elif isinstance(decorator.args[0], ast.Str): # Python < 3.8
                                path = decorator.args[0].s
                                
                        for kw in decorator.keywords:
                            if kw.arg == 'methods' and isinstance(kw.value, ast.List):
                                methods = [m.value if isinstance(m, ast.Constant) else m.s for m in kw.value.elts]

                        # Check if it has @login_required
                        is_secure = any(
                            (isinstance(d, ast.Name) and d.id == 'login_required') or
                            (isinstance(d, ast.Attribute) and d.attr == 'login_required')
                            for d in node.decorator_list
                        )

                        full_path = (url_prefix or local_prefix).rstrip('/') + '/' + path.lstrip('/')
                        
                        docstring = ast.get_docstring(node)
                        summary = ""
                        description = ""
                        if docstring:
                            lines = docstring.strip().split('\n')
                            summary = lines[0]
                            description = "\n".join(lines[1:]).strip() if len(lines) > 1 else ""

                        for method in methods:
                            routes.append({
                                "pageTitle": summary or f"Endpoint {node.name}",
                                "pageDescription": description or summary or "No description provided.",
                                "pageUrl": f"http://localhost:5050{full_path}",
                                "method": method,
                                "authRequired": is_secure,
                                "params": [], # Would need more complex analysis
                                "requestBody": {}, # Would need more complex analysis
                                "responseBody": {}, # Would need more complex analysis
                                "errorCodes": ["400", "401", "500"]
                            })
    except Exception as e:
        print(f"Error parsing {filepath}: {e}")

    return routes

def main():
    api_dir = 'web/api'
    all_routes = []
    
    # Map prefixes from app.py manually for accuracy
    prefixes = {
        "analytics_api.py": "/api/v1/analytics",
        "optimization_api.py": "/api/v1/optimization",
        "advanced_risk_api.py": "/api/v1/advanced-risk",
        "tax_optimization_api.py": "/api/v1/tax-optimization",
        "onboarding_api.py": "/api/v1",
        "market_data_api.py": "/api/v1/market",
        "macro_data_api.py": "/api/v1/macro-data",
        "education_api.py": "/api/v1/education",
        "banking_api.py": "/api/v1",
        "brokerage_api.py": "/api/v1",
        "billing_api.py": "/api/v1",
        "crypto_api.py": "/api/v1",
        "settlement_api.py": "/api/v1",
        "identity_api.py": "/api/v1/identity",
        "social_api.py": "/api/v1/social",
        "debate_api.py": "/api/v1/ai",
        "briefing_api.py": "/api/v1/ai",
        "stripe_api.py": "/api/v1",
        "paypal_api.py": "/api/v1",
        "venmo_api.py": "/api/v1",
        "square_api.py": "/api/v1",
        "plaid_api.py": "/api/v1",
        "coinbase_api.py": "/api/v1",
        "binance_api.py": "/api/v1",
        "tax_api.py": "/api/v1",
        "twilio_api.py": "/api/v1",
        "email_api.py": "/api/v1",
        "incident_api.py": "/api/v1",
        "health_api.py": "",
        "auth_api.py": "/api/auth",
        "kyc_api_flask.py": "/api/v1/kyc",
        "cash_api_flask.py": "/api/v1/cash",
        "backtest_api.py": "/api/v1/backtest",
        "estate_api.py": "/api/v1/estate",
        "compliance_api.py": "/api/v1/compliance",
        "scenario_api.py": "/api/v1/scenario",
        "philanthropy_api.py": "/api/v1/philanthropy",
        "system_api.py": "/api/v1/system",
        "corporate_api.py": "/api/v1/corporate",
        "margin_api.py": "/api/v1/margin",
        "mobile_api.py": "/api/v1/mobile",
        "integrations_api.py": "/api/v1/integrations",
        "homeostasis_api.py": "/api/v1/homeostasis",
    }

    for filename in os.listdir(api_dir):
        if filename.endswith('.py'):
            filepath = os.path.join(api_dir, filename)
            prefix = prefixes.get(filename, "")
            routes = extract_routes_from_file(filepath, prefix)
            all_routes.extend(routes)

    # Add routes direct from app.py
    # ... (health, gap, prediction)
    
    with open('plans/2_02_26/artifacts/api_routes.json', 'w') as f:
        json.dump(all_routes, f, indent=2)

if __name__ == "__main__":
    main()
