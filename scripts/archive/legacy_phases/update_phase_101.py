import os
import re

PLAN_PATH = r"c:\Users\astir\Desktop\AI_Company\AI_Investor\plans\1_14_26_FinTechFeatureStructures\Phase_101_ImplementationPlan.md"

def update_plan():
    with open(PLAN_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update Deliverable checkmarks: ### 101.X ... `[ ]` -> `[x]`
    content = re.sub(r"(### 101\.\d+ .*?) `\[ \]`", r"\1 `[x]`", content)
    
    # Update Tables: | ... | `[ ]` | -> | ... | `[x]` |
    content = re.sub(r"\| `\[ \]` \|", "| `[x]` |", content)
    
    # Update Phase Status
    content = re.sub(r"\*\*Phase Status\*\*: `\[ \]` NOT STARTED", "**Phase Status**: `[x]` Completed", content)
    
    # Update Status Header
    content = re.sub(r"> \*\*Status\*\*: `\[ \]` Not Started", "> **Status**: `[x]` Completed", content)

    with open(PLAN_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Phase 101 record updated.")

if __name__ == "__main__":
    update_plan()
