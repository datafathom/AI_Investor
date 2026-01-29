import re
import os

ROADMAP_PATH = r"c:\Users\astir\Desktop\AI_Company\AI_Investor\plans\1_14_26_FinTechFeatureStructures\ROADMAP_1_14_26.md"

def update_roadmap():
    with open(ROADMAP_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update Phase 109 in table
    content = re.sub(r"\| 109 \| (.*?) \| `\[ \]` \|", r"| 109 | \1 | `[x]` |", content)

    with open(ROADMAP_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_roadmap()
