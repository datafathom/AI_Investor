
import os
import re

base_path = r"c:\Users\astir\Desktop\AI_Company\AI_Investor\plans\UI_phase_X2"

def update_phase_status(phase_num):
    filename = f"Phase_{phase_num}_ImplementationPlan.md"
    filepath = os.path.join(base_path, filename)
    
    if not os.path.exists(filepath):
        print(f"File not found: {filename}")
        return

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern to find "Status: `[ ]` Not Started" or similar variants
    # Use a broader regex to capture the Status part
    # Look for "Status:" then any characters until end of line, replace with "Status: `[x]` Completed"
    
    new_content = re.sub(r"(Status:\s*).*$", r"\1`[x]` Completed", content, flags=re.MULTILINE)
    
    if content != new_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filename}")
    else:
        print(f"No changes needed for {filename}")

# Update Phases 57 to 68
for i in range(57, 69):
    update_phase_status(i)
