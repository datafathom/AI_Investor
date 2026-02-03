
import os
import re
import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

EXCLUDES = {
    'dirs': {'venv', '.git', '__pycache__', 'node_modules', 'tests', 'artifacts', 'plans', 'dist', 'build', 'coverage', '.gemini'},
    'files': {'package-lock.json', 'yarn.lock', 'requirements.txt', '.gitignore', 'audit_codebase.py'}
}

MOCK_PATTERNS = [
    r'(?i)mock_response',
    r'(?i)dummy_data',
    r'(?i)placeholder data',
    r'(?i)# todo: remove mock',
    r'(?i)# todo: implement real',
    r'(?i)return .*?{"mock":',
    r'(?i)return .*?\[{"mock":'
]

VENDOR_PATTERNS = [
    r'requests\.(get|post|put|delete|patch)\(',
    r'axios\.(get|post|put|delete|patch)\(',
    r'fetch\(',
    r'(?i)googleapis\.com',
    r'(?i)stripe\.com',
    r'(?i)plaid\.com',
    r'(?i)polygon\.io',
    r'(?i)openai\.com',
    r'(?i)anthropic\.com'
]

def scan_file(filepath):
    mock_matches = []
    vendor_matches = []
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            for i, line in enumerate(lines):
                # Check mocks
                for pattern in MOCK_PATTERNS:
                    if re.search(pattern, line):
                        mock_matches.append({
                            "file": str(filepath.relative_to(PROJECT_ROOT)),
                            "line": i + 1,
                            "content": line.strip(),
                            "pattern": pattern
                        })
                        break # One match per line is enough
                
                # Check vendors
                for pattern in VENDOR_PATTERNS:
                    if re.search(pattern, line):
                        vendor_matches.append({
                            "file": str(filepath.relative_to(PROJECT_ROOT)),
                            "line": i + 1,
                            "content": line.strip(),
                            "pattern": pattern
                        })
                        break
    except Exception as e:
        print(f"Skipping {filepath}: {e}")
        
    return mock_matches, vendor_matches

def main():
    all_mocks = []
    all_vendors = []
    
    print(f"Scanning {PROJECT_ROOT}...")
    
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Filter dirs
        dirs[:] = [d for d in dirs if d not in EXCLUDES['dirs']]
        
        for file in files:
            if file in EXCLUDES['files']:
                continue
            if not (file.endswith('.py') or file.endswith('.js') or file.endswith('.jsx') or file.endswith('.ts') or file.endswith('.tsx')):
                continue
                
            filepath = Path(root) / file
            mocks, vendors = scan_file(filepath)
            all_mocks.extend(mocks)
            all_vendors.extend(vendors)
            
    # Save artifacts
    artifacts_dir = PROJECT_ROOT / "notes"
    
    artifacts_dir.mkdir(parents=True, exist_ok=True)
    
    mock_path = artifacts_dir / "MockResponses_needImplemenetation.json"
    with open(mock_path, 'w') as f:
        json.dump(all_mocks, f, indent=2)
        
    vendor_path = artifacts_dir / "Vendor_API_Needed.json"
    with open(vendor_path, 'w') as f:
        json.dump(all_vendors, f, indent=2)
        
    print(f"Generated {mock_path} ({len(all_mocks)} items)")
    print(f"Generated {vendor_path} ({len(all_vendors)} items)")

if __name__ == "__main__":
    main()
