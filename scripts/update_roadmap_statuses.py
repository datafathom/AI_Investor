import re
import os

ROADMAP_PATH = r"c:\Users\astir\Desktop\AI_Company\AI_Investor\plans\1_14_26_FinTechFeatureStructures\ROADMAP_1_14_26.md"

def update_roadmap():
    with open(ROADMAP_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Update Epoch Statuses
    content = re.sub(r"\| (I|II|III|IV|V) \| (.*?) \| (.*?) \| (.*?) \|", r"| \1 | \2 | \3 | 🟢 Completed |", content)

    # Update table phase status
    def replace_phase_status(match):
        phase_num = int(match.group(1))
        if phase_num <= 100:
            return f"| {phase_num} | {match.group(2)} | `[x]` | {match.group(3)}"
        return match.group(0)

    content = re.sub(r"\| (\d+) \| (.*?) \| `\[[ /]\]` \| (.*)", replace_phase_status, content)

    # Update header phase status
    content = re.sub(r"## Phase ([0-9][0-9]?|100): (.*?) `\[[ /]\]`", r"## Phase \1: \2 `[x]`", content)

    with open(ROADMAP_PATH, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Roadmap updated for Phases 0-100.")

if __name__ == "__main__":
    update_roadmap()
