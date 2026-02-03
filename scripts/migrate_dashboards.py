import os
import re

DASHBOARD_DIR = r"c:\Users\astir\Desktop\AI_Company\AI_Investor\frontend2\src\pages"

def migrate_dashboard(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 1. Add StorageService import if not present
    if "StorageService" not in content:
        # Try to insert after imports
        if "from 'react';" in content:
            content = content.replace("from 'react';", "from 'react';\nimport { StorageService } from '../utils/storageService';")
        elif "from 'react-grid-layout';" in content:
             content = content.replace("from 'react-grid-layout';", "from 'react-grid-layout';\nimport { StorageService } from '../utils/storageService';")
        else:
             # Fallback: Top of file
             content = "import { StorageService } from '../utils/storageService';\n" + content

    # 2. Refactor useState to be sync/default and add useEffect for loading
    # Pattern: 
    # const [layouts, setLayouts] = useState(() => { ... localStorage.getItem(STORAGE_KEY) ... });
    
    # Replacement Pattern:
    # const [layouts, setLayouts] = useState(DEFAULT_LAYOUT);
    # useEffect(() => { ... StorageService.get(STORAGE_KEY) ... }, []);

    regex_state = r"const\s+\[layouts,\s*setLayouts\]\s*=\s*useState\(\(\)\s*=>\s*\{[^}]*localStorage\.getItem\(([^)]+)\)[^}]*\}\);"
    
    match = re.search(regex_state, content)
    if match:
        storage_key_var = match.group(1)
        
        # We need to find the DEFAULT variable. Usually it's DEFAULT_LAYOUT or DEFAULT_LAYOUTS inside the block or defined above.
        # Simple heuristic: Look for return ... ? ... : (DEFAULT_...);
        
        default_var = "DEFAULT_LAYOUT" # Fallback
        
        state_block = match.group(0)
        default_match = re.search(r":\s*([A-Z_]+);", state_block)
        if default_match:
            default_var = default_match.group(1)
        
        new_state_logic = f"""const [layouts, setLayouts] = useState({default_var});

    useEffect(() => {{
        const loadLayout = async () => {{
            const saved = await StorageService.get({storage_key_var});
            if (saved) setLayouts(saved);
        }};
        loadLayout();
    }}, []);"""
        
        content = content.replace(state_block, new_state_logic)
        print(f"Migrated State Logic: {filepath}")

    # 3. Refactor onLayoutChange
    # Pattern: localStorage.setItem(STORAGE_KEY, JSON.stringify(allLayouts));
    
    regex_set = r"localStorage\.setItem\(([^,]+),\s*JSON\.stringify\(allLayouts\)\);"
    
    def replacer(m):
        return f"StorageService.set({m.group(1)}, allLayouts);"

    content = re.sub(regex_set, replacer, content)
    
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated: {filepath}")
    else:
        print(f"No changes needed: {filepath}")

def main():
    print("Starting dashboard migration...")
    files = [f for f in os.listdir(DASHBOARD_DIR) if f.endswith('.jsx')]
    
    count = 0
    for file in files:
        if "Dashboard" in file or "Alpha" in file or "Scanner" in file or "Maintenance" in file or "Control" in file or "Attribution" in file or "Account" in file or "Debate" in file:
             path = os.path.join(DASHBOARD_DIR, file)
             try:
                migrate_dashboard(path)
                count += 1
             except Exception as e:
                 print(f"Error processing {file}: {e}")
    
    print(f"Processed {count} files.")

if __name__ == "__main__":
    main()
