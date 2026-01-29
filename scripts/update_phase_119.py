import os
import re

PLAN_PATH = r"c:\Users\astir\Desktop\AI_Company\AI_Investor\plans\1_14_26_FinTechFeatureStructures\Phase_119_ImplementationPlan.md"

def update_plan():
    if not os.path.exists(PLAN_PATH): return
    with open(PLAN_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    content = re.sub(r"(### 119\.\d+ .*?) `\[ \]`", r"\1 `[x]`", content)
    content = re.sub(r"\| `\[ \]` \|", "| `[x]` |", content)
    content = re.sub(r"> \*\*Status\*\*: `\[ \]` Not Started", "> **Status**: `[x]` Completed", content)
    
    with open(PLAN_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_plan()
