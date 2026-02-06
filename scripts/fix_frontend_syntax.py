import os

TARGET_DIR = r"c:\Users\astir\Desktop\AI_Company\AI_Investor\frontend\src"

def fix_files():
    count = 0
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith(".jsx"):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if "> INITIALIZING" in content:
                        print(f"Fixing: {file}")
                        new_content = content.replace("> INITIALIZING", "&gt; INITIALIZING")
                        new_content = new_content.replace("> SYNCING", "&gt; SYNCING")
                        new_content = new_content.replace("> ESTABLISHING", "&gt; ESTABLISHING")
                        new_content = new_content.replace("> READY", "&gt; READY")
                        new_content = new_content.replace("> $10k", "&gt; $10k") # For TradeAuth
                        
                        with open(path, 'w', encoding='utf-8') as f:
                            f.write(new_content)
                        count += 1
                except Exception as e:
                    print(f"Error processing {file}: {e}")
    print(f"Fixed {count} files.")

if __name__ == "__main__":
    fix_files()
