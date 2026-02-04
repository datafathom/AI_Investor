import os
import json
import re
import logging

logger = logging.getLogger(__name__)

def get_frontend_routes_metadata():
    app_jsx_path = os.path.abspath("frontend/src/App.jsx")
    if not os.path.exists(app_jsx_path):
        logger.error(f"App.jsx not found at {app_jsx_path}")
        return []

    with open(app_jsx_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Map paths to descriptions from handleMenuAction cases
    # Example: case 'show-dashboard': navigate('/workspace/terminal'); break;
    menu_actions = {}
    case_pattern = r"case\s+['\"]([^'\"]+)['\"]:\s+navigate\(?['\"]([^'\"]+)['\"]\)?;"
    for match in re.finditer(case_pattern, content):
        action = match.group(1).replace('show-', '').replace('nav-', '').replace('-', ' ').title()
        path = match.group(2)
        menu_actions[path] = action

    # 2. Extract Phase comments for components
    phases = {}
    phase_pattern = r"const\s+(\w+)\s+=\s+lazy.*//\s*(Phase\s+\d+.*)"
    for match in re.finditer(phase_pattern, content):
        phases[match.group(1)] = match.group(2)

    # 3. Extract Routes from <Route path="..." element={...} />
    routes = []
    # Regex to handle multi-line Route tags
    route_pattern = r'<Route\s+path=["\']([^"\']+)["\']\s+element=\{([^}]+)\}'
    
    # Also find top-level RoleOverview aliases
    for match in re.finditer(route_pattern, content):
        path = match.group(1)
        element_raw = match.group(2).strip()
        
        # Skip relative/catch-all redirects for now unless they are interesting
        if path == "/":
            continue
            
        # Try to extract component name from element
        component_match = re.search(r'<(\w+)', element_raw)
        component_name = component_match.group(1) if component_match else "Custom Element"
        
        # Metadata enrichment
        is_secured = True # Default in App.jsx due to top-level AuthGuard
        if path == "*" or "404" in path.lower() or "/legal/" in path:
            is_secured = False
            
        description = menu_actions.get(path, f"Frontend interface for {component_name}")
        if component_name in phases:
            description += f" ({phases[component_name]})"
        
        # Infer query params and dynamic segments
        query_params = []
        if ":" in path:
            segments = re.findall(r':(\w+)', path)
            for s in segments:
                query_params.append(f"{s} (URL Segment)")

        # Common query params for fintech apps
        if "market" in path or "trading" in path or "scanner" in path:
            query_params.append("symbol (query)")
            query_params.append("timeframe (query)")

        routes.append({
            "path": path,
            "component": component_name,
            "description": description,
            "secured": is_secured,
            "query_params": query_params,
            "is_os_style": path in content and "isOSStylePage" in content # Basic check
        })
        
    return routes

def build_routes_txt():
    """Generates notes/All_Frontend_Routes.txt"""
    routes = get_frontend_routes_metadata()
    if not routes:
        print("No routes found.")
        return

    output_path = os.path.abspath("notes/All_Frontend_Routes.txt")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Filter and sort
    paths = sorted(list(set([r['path'] for r in routes])))
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("# AI Investor - Available Frontend Routes\n")
        f.write("=" * 40 + "\n\n")
        f.write("Full URL Base: http://localhost:5173\n\n")
        for p in paths:
            f.write(f"- {p}\n")
            
    print(f"SUCCESS: Generated {output_path}")

def build_routes_json():
    """Generates notes/All_Frontend_Routes.json"""
    routes = get_frontend_routes_metadata()
    if not routes:
        print("No routes found.")
        return

    output_path = os.path.abspath("notes/All_Frontend_Routes.json")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Sort by path
    routes.sort(key=lambda x: x['path'])
    
    data = {
        "project": "AI Investor",
        "type": "Frontend Routes Documentation",
        "base_url": "http://localhost:5173",
        "route_count": len(routes),
        "routes": routes
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)
        
    print(f"SUCCESS: Generated {output_path}")
