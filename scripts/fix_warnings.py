import os

def fix_content(content):
    # 1. Fix Pydantic V2 deprecations
    content = content.replace(".model_dump()", ".model_dump()")
    content = content.replace(".model_dump.return_value", ".model_dump.return_value")
    
    # 2. Fix datetime.now(timezone.utc) deprecations
    # Standardize to datetime.now(timezone.utc)
    if "datetime.now(timezone.utc)" in content:
        content = content.replace("datetime.now(timezone.utc)", "datetime.now(timezone.utc)")
        content = content.replace("datetime.now(timezone.utc)", "datetime.now(timezone.utc)")
    
    # 3. Ensure timezone is imported everywhere it is needed
    if "timezone.utc" in content:
        # Check specifically for import statements
        import_present = (
            "from datetime import timezone" in content or 
            "import datetime.timezone" in content or
            ", timezone" in content and "from datetime import" in content
        )
        
        if not import_present:
            if "from datetime import" in content:
                content = content.replace("from datetime import ", "from datetime import timezone, ")
            elif "import datetime" in content:
                content = content.replace("import datetime", "import datetime\nfrom datetime import timezone")
            else:
                content = "from datetime import timezone\n" + content
            
    return content

def process_all_py_files():
    base_dir = r"c:/Users/astir/Desktop/AI_Company/AI_Investor"
    for root, _, files in os.walk(base_dir):
        if any(d in root for d in ["venv", ".git", "__pycache__", ".gemini"]):
            continue
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    new_content = fix_content(content)
                    
                    if new_content != content:
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        print(f"Fixed: {os.path.relpath(path, base_dir)}")
                except Exception as e:
                    print(f"Error processing {path}: {e}")

if __name__ == "__main__":
    process_all_py_files()
