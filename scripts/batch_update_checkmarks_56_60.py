import os
import re

BASE_DIR = r"c:\Users\astir\Desktop\AI_Company\AI_Investor\plans\1_14_26_FinTechFeatureStructures\Completed"

def update_plans(start, end):
    for i in range(start, end + 1):
        filename = f"Phase_{i}_ImplementationPlan.md"
        filepath = os.path.join(BASE_DIR, filename)
        
        if not os.path.exists(filepath):
            print(f"Skipping {filename} (Not found)")
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 1. Update Sub-deliverable Headers: ### 1.1 ... `[ ]` -> `[x]`
        content = re.sub(r"(### \d+\.\d+ .*?) `\[ \]`", r"\1 `[x]`", content)
        
        # 2. Update Tables: | ... | `[ ]` | -> | ... | `[x]` |
        content = re.sub(r"\| `\[ \]` \|", "| `[x]` |", content)
        
        # 3. Update Status lines in body: | Status | `[ ]` |
        content = re.sub(r"\| Status \| `\[ \]` \|", "| Status | `[x]` |", content)

        # 4. Update Header Status
        content = re.sub(r"> \*\*Status\*\*: `\[ \]` NOT STARTED", "> **Status**: `[x]` Completed", content)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Updated {filename}")

if __name__ == "__main__":
    update_plans(56, 60)
