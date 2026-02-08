import os
import re
import glob

PLANS_DIR = r"c:\Users\astir\Desktop\AI_Company\AI_Investor\docs\_PLANS\Services_Mapped_To_Frontend_Pages"
OUTPUT_FILE = r"c:\Users\astir\Desktop\AI_Company\AI_Investor\docs\_PLANS\Services_Mapped_To_Frontend_Pages\_NEW_ROUTES.txt"

def extract_routes():
    # Pattern to find routes in descriptions. e.g. "Full-page interface (`/admin/logs`)" or "Page (`/dashboard`)"
    # We look for (`/something`)
    route_pattern = re.compile(r"\(`(/[^`]+)`\)")
    # Also handle without backticks just in case: (/admin/logs)
    route_pattern_simple = re.compile(r"\((/[^)]+)\)")
    
    # Store results
    new_entries = []

    # Get all phase files
    files = glob.glob(os.path.join(PLANS_DIR, "Phase_*_Implementation_Plan.md"))
    
    # Sort by phase number
    def get_phase_num(f):
        match = re.search(r"Phase_(\d+)_", f)
        return int(match.group(1)) if match else 999
    
    files.sort(key=get_phase_num)

    for file_path in files:
        phase_name = os.path.basename(file_path).replace("_Implementation_Plan.md", "")
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # Split by Deliverable to give context
        deliverables = content.split("## Deliverable")
        
        for section in deliverables[1:]: # Skip preamble
            # Get Deliverable Title
            title_match = re.match(r"\s*\d+: (.+)", section)
            title = title_match.group(1).strip() if title_match else "Unknown"
            
            # Find route
            routes = []
            
            # Try with backticks first
            matches = route_pattern.findall(section)
            routes.extend(matches)
            
            # Try without backticks if none found
            if not matches:
                 matches_simple = route_pattern_simple.findall(section)
                 for r in matches_simple:
                     if r.startswith("/") and len(r) > 1 and " " not in r:
                         routes.append(r)
            
            # Fallback: Parse table for Pages
            # Look for lines like | Component | Path | Type |
            # and then rows like | Name.jsx | frontend/src/pages/... | Page |
            
            # Simple line iteration for the section
            lines = section.split('\n')
            for line in lines:
                if "| Page |" in line or "| Page" in line: # Loose match for Page type
                    parts = [p.strip() for p in line.split('|')]
                    # expected parts: ['', Component, Path, Type, '']
                    if len(parts) >= 4:
                        path = parts[2]
                        if "frontend/src/pages/" in path:
                            # Extract relative path from pages/
                            rel_path = path.split("frontend/src/pages/")[1]
                            # Remove extension
                            rel_path = os.path.splitext(rel_path)[0]
                            
                            # Split into segments
                            segments = rel_path.split('/')
                            kebab_segments = []
                            for seg in segments:
                                # CamelToKebab
                                kebab = re.sub(r'(?<!^)(?=[A-Z])', '-', seg).lower()
                                kebab_segments.append(kebab)
                                
                            inferred_route = "/" + "/".join(kebab_segments)
                            routes.append(inferred_route)

            # Unique routes
            routes = list(set(routes))
            
            for route in routes:
                entry = f"{phase_name} - {title}: http://localhost:5173{route}"
                if entry not in new_entries:
                    new_entries.append(entry)

    if not new_entries:
        print("No new routes found in plans.")
        return

    # Read existing to avoid duplication (though set check above helps)
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            existing = f.read()
    else:
        existing = ""

    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write("\n\n# Auto-Extracted Routes from Phase Plans\n")
        count = 0
        for entry in new_entries:
            # Check if route already in file (simple check)
            route_part = entry.split(": http")[1].strip()
            if route_part not in existing:
                f.write(f"{entry}\n")
                print(f"Added: {entry}")
                count += 1
            else:
                print(f"Skipping duplicate: {route_part}")
        
    print(f"\nTotal new routes added: {count}")

if __name__ == "__main__":
    extract_routes()
