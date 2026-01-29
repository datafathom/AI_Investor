import re
import os

ROADMAP_PATH = r"c:\Users\astir\Desktop\AI_Company\AI_Investor\plans\1_14_26_FinTechFeatureStructures\ROADMAP_1_14_26.md"

def update_roadmap():
    with open(ROADMAP_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update Phase 120 in table
    content = re.sub(r"\| 120 \| (.*?) \| `\[ \]` \|", r"| 120 | \1 | `[x]` |", content)

    # Update Epoch VI status in Overview table
    content = re.sub(r"\| VI \| 101-120 \| (.*?) \| ⚪ Not Started \|", r"| VI | 101-120 | \1 | 🟢 Completed |", content)

    with open(ROADMAP_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_roadmap()
