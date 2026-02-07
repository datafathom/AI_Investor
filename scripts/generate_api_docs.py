import json
import os
from pathlib import Path
from collections import defaultdict

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
ROUTES_JSON = PROJECT_ROOT / "docs" / "api" / "api_routes.json"
OUTPUT_DIR = PROJECT_ROOT / "docs" / "api"
COMMANDS_DIR = OUTPUT_DIR / "api_commands"

def slugify_path(path):
    """Converts a path like /api/v1/auth to api_v1_auth."""
    return path.strip('/').replace('/', '_').replace('<', '').replace('>', '')

def generate_markdown(service_name, routes):
    """Generates markdown content for a set of routes."""
    md = f"# API Service: {service_name}\n\n"
    md += f"This document contains all endpoints registered under `{service_name}`.\n\n"
    
    # Sort routes by path then method
    sorted_routes = sorted(routes, key=lambda x: (x['path'], x['method']))
    
    for route in sorted_routes:
        md += f"## {route['method']} {route['path']}\n\n"
        md += f"**Summary**: {route.get('summary', 'No summary provided')}\n\n"
        
        md += "### Details\n"
        md += f"- **Authentication**: {route.get('authentication', 'None')}\n"
        md += f"- **Rate Limiting**: {route.get('rate_limiting', 'N/A')}\n"
        md += f"- **Caching**: {route.get('caching', 'None')}\n\n"
        
        if route.get('parameters'):
            md += "### Parameters\n"
            md += "```json\n"
            md += json.dumps(route['parameters'], indent=2)
            md += "\n```\n\n"
            
        if route.get('request_body'):
            md += "### Request Body\n"
            md += "```json\n"
            md += json.dumps(route['request_body'], indent=2)
            md += "\n```\n\n"
            
        if route.get('response_body'):
            md += "### Response Body\n"
            md += "```json\n"
            md += json.dumps(route['response_body'], indent=2)
            md += "\n```\n\n"
            
        if route.get('error_codes'):
            md += "### Error Codes\n"
            md += "| Code | Description |\n"
            md += "| --- | --- |\n"
            for code, desc in route['error_codes'].items():
                md += f"| {code} | {desc} |\n"
            md += "\n"
            
        md += "---\n\n"
        
    return md

def main():
    if not ROUTES_JSON.exists():
        print(f"Error: {ROUTES_JSON} not found.")
        return

    with open(ROUTES_JSON, 'r', encoding='utf-8') as f:
        routes = json.load(f)

    # Grouping logic
    groups = defaultdict(list)
    
    for route in routes:
        path = route['path']
        
        # Special case for /api/docs
        if path.startswith('/api/docs'):
            groups['api_docs'].append(route)
            continue
            
        # Group by first 3 segments if possible (e.g., /api/v1/auth)
        parts = [p for p in path.split('/') if p]
        if len(parts) >= 3:
            service_key = "_".join(parts[:3])
        elif len(parts) > 0:
            service_key = "_".join(parts)
        else:
            service_key = "root"
            
        groups[service_key].append(route)

    # Ensure output directories exist
    os.makedirs(COMMANDS_DIR, exist_ok=True)

    for service_key, service_routes in groups.items():
        content = generate_markdown(service_key, service_routes)
        
        if service_key == 'api_docs':
            filename = COMMANDS_DIR / "api_docs.md"
        else:
            filename = OUTPUT_DIR / f"{service_key}.md"
            
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"✅ Generated {filename.relative_to(PROJECT_ROOT)}")

if __name__ == "__main__":
    main()
