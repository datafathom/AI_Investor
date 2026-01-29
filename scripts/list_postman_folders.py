"""
Script to generate a comprehensive API-to-Frontend audit report.
"""
import json
from pathlib import Path
from typing import Dict, List, Any, Set


def sanitize(text: str) -> str:
    """Remove or replace special characters for safe output"""
    return text.encode('ascii', 'replace').decode('ascii')


def extract_endpoints(item: dict, folder_path: str = "") -> List[Dict[str, Any]]:
    """Recursively extract all endpoints"""
    endpoints = []
    name = sanitize(item.get("name", "Unnamed"))
    current_path = f"{folder_path}/{name}" if folder_path else name

    if "item" in item:
        for child in item["item"]:
            endpoints.extend(extract_endpoints(child, current_path))
    else:
        method = item.get("request", {}).get("method", "?")
        url_parts = item.get("request", {}).get("url", {}).get("path", [])
        url = "/" + "/".join(url_parts) if url_parts else "N/A"
        endpoints.append({
            "folder": folder_path,
            "name": name,
            "method": method,
            "url": url
        })
    
    return endpoints


def get_api_prefix(url: str) -> str:
    """Extract the main API prefix from a URL"""
    parts = url.strip("/").split("/")
    if len(parts) >= 3:
        # /api/v1/{prefix}/...
        return parts[2] if parts[0] == "api" and parts[1] == "v1" else parts[0]
    return url


def main() -> None:
    collection_path = Path("docs/api/ai_investor_postman_collection.json")
    
    with open(collection_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Extract all endpoints
    all_endpoints = []
    for item in data.get("item", []):
        all_endpoints.extend(extract_endpoints(item))
    
    # Group by top-level folder  
    top_folders: Dict[str, List[dict]] = {}
    for ep in all_endpoints:
        top_folder = ep["folder"].split("/")[0] if ep["folder"] else "Root"
        if top_folder not in top_folders:
            top_folders[top_folder] = []
        top_folders[top_folder].append(ep)
    
    # Group by API prefix
    api_prefixes: Dict[str, Set[str]] = {}
    for ep in all_endpoints:
        prefix = get_api_prefix(ep["url"])
        if prefix not in api_prefixes:
            api_prefixes[prefix] = set()
        api_prefixes[prefix].add(ep["url"])
    
    # Print summary
    print("=" * 60)
    print("POSTMAN COLLECTION SUMMARY")
    print("=" * 60)
    print(f"Total Endpoints: {len(all_endpoints)}")
    print(f"\nTop-Level Folders ({len(top_folders)}):")
    for name, eps in sorted(top_folders.items(), key=lambda x: -len(x[1])):
        print(f"  - {name}: {len(eps)} endpoints")
    
    print(f"\n\nAPI Prefixes ({len(api_prefixes)}):")  
    for prefix, urls in sorted(api_prefixes.items(), key=lambda x: -len(x[1])):
        print(f"  - /api/v1/{prefix}: {len(urls)} unique URLs")


if __name__ == "__main__":
    main()
