import os
import re

PROJECT_ROOT = r"c:\Users\astir\Desktop\AI_Company\AI_Investor"

def refactor_imports():
    count = 0
    # Walk through all python files
    for root, dirs, files in os.walk(PROJECT_ROOT):
        # Skip venv and .git
        if "venv" in root or ".git" in root:
            continue
            
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # Regex replacement patterns
                    # 1. from schemas.xyz import ... -> from schemas.xyz import ...
                    # 2. from schemas import ... -> from schemas import ...
                    # 3. import schemas.xyz -> import schemas.xyz
                    
                    new_content = re.sub(r'from models(\.|\s)', r'from schemas\1', content)
                    new_content = re.sub(r'import models\.', r'import schemas.', new_content)
                    
                    if content != new_content:
                        count += 1
                        print(f"Updating imports in: {file}")
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                            
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")

    print(f"Refactor complete. Updated {count} files.")

if __name__ == "__main__":
    refactor_imports()
