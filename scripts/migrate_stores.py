"""
Script to migrate Zustand stores to use StorageService adapter.
"""
import os
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
STORES_DIR = PROJECT_ROOT / "frontend2" / "src" / "stores"

def migrate_file(file_path):
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # Check if file uses persist and localStorage
        if 'createJSONStorage' in content and 'localStorage' in content:
            # 1. Add import
            if "import { storageAdapter } from '../utils/storageAdapter';" not in content:
                # Insert after zustand middleware import
                content = content.replace(
                    "import { persist, createJSONStorage } from 'zustand/middleware';",
                    "import { persist, createJSONStorage } from 'zustand/middleware';\nimport { storageAdapter } from '../utils/storageAdapter';"
                )
            
            # 2. Replace storage config
            # Regex to find `storage: createJSONStorage(() => localStorage)` widely
            content = re.sub(
                r'storage:\s*createJSONStorage\(\(\)\s*=>\s*localStorage\)',
                'storage: createJSONStorage(() => storageAdapter)',
                content
            )
            
            file_path.write_text(content, encoding='utf-8')
            print(f"Migrated: {file_path.name}")
            return True
        return False
    except Exception as e:
        print(f"Error migrating {file_path.name}: {e}")
        return False

def main():
    count = 0
    for file_path in STORES_DIR.glob("*.js"):
        if migrate_file(file_path):
            count += 1
    print(f"Total stores migrated: {count}")

if __name__ == "__main__":
    main()
