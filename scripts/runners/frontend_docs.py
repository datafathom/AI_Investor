import os
import re
import json
from pathlib import Path
from typing import List, Dict, Optional

# Constants
PROJECT_ROOT = Path(__file__).parent.parent.parent
FRONTEND_SRC = PROJECT_ROOT / "frontend" / "src"
APP_JSX = FRONTEND_SRC / "App.jsx"
OUTPUT_PATH = PROJECT_ROOT / "notes" / "FrontendPages.json"

class FrontendRouteExtractor:
    """Extracts frontend routes and their descriptions from App.jsx and components."""

    def __init__(self, frontend_port: int = 5173):
        self.base_url = f"http://localhost:{frontend_port}"

    def extract_routes(self) -> List[Dict]:
        """Main method to extract routes."""
        if not APP_JSX.exists():
            print(f"Error: {APP_JSX} not found.")
            return []

        content = APP_JSX.read_text(encoding='utf-8')
        
        # Regex for <Route path="..." element={<Component ... />} />
        route_pattern = re.compile(r'<Route\s+path=["\']([^"\']+)["\']\s+element=\{<([^/\s>]+)')
        matches = route_pattern.findall(content)
        
        routes = []
        for path, component in matches:
            description = self._get_component_description(component)
            
            # Normalize path
            full_url = self.base_url + (path if path.startswith('/') else f"/{path}")
            
            routes.append({
                "pageTitle": component.replace("Dashboard", "").replace("Page", ""),
                "pageDescription": description or f"Main page for {component}",
                "pageUrl": full_url
                # "componentName": component  # Removed to match precise schema requirements if strict
            })
            
        return routes

    def _get_component_description(self, component_name: str) -> Optional[str]:
        """Attempts to find a description in the component file or docstrings."""
        # Common locations for page components
        search_dirs = [
            FRONTEND_SRC / "pages",
            FRONTEND_SRC / "components",
            FRONTEND_SRC / "widgets"
        ]
        
        for directory in search_dirs:
            # Try .jsx and .tsx
            for ext in [".jsx", ".tsx"]:
                file_path = directory / f"{component_name}{ext}"
                if file_path.exists():
                    return self._parse_file_description(file_path)
                    
                # Check subdirectories
                matching_files = list(directory.rglob(f"{component_name}{ext}"))
                if matching_files:
                    return self._parse_file_description(matching_files[0])
                    
        return None

    def _parse_file_description(self, file_path: Path) -> Optional[str]:
        """Parses a file for JSDoc or comments describing the component."""
        content = file_path.read_text(encoding='utf-8')
        
        # Look for JSDoc @description or first multi-line comment
        jsdoc_match = re.search(r'/\*\*[\s\S]*?@description\s+([\s\S]*?)\*/', content)
        if jsdoc_match:
            return jsdoc_match.group(1).strip().replace('\n', ' ')
            
        # Look for any comment at the top of the file
        top_comment = re.search(r'/\*\*([\s\S]*?)\*/', content)
        if top_comment:
            text = top_comment.group(1).strip()
            # Clean up asterisks
            lines = [line.strip().lstrip('*').strip() for line in text.split('\n')]
            return ' '.join(filter(None, lines))[:200]
            
        return None

def build_frontend_pages():
    """CLI handler for generating the frontend pages JSON."""
    extractor = FrontendRouteExtractor()
    routes = extractor.extract_routes()
    
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(routes, f, indent=4)
        
    print(f"Successfully generated {len(routes)} routes in {OUTPUT_PATH}")

if __name__ == "__main__":
    build_frontend_pages()
