import os
import re
import shutil

BASE_DIR = r"c:\Users\astir\Desktop\AI_Company\AI_Investor\plans\1_14_26_FinTechFeatureStructures"
COMPLETED_DIR = os.path.join(BASE_DIR, "Completed")

def process_phases(start, end):
    if not os.path.exists(COMPLETED_DIR):
        os.makedirs(COMPLETED_DIR)
        
    for i in range(start, end + 1):
        filename = f"Phase_{i}_ImplementationPlan.md"
        filepath = os.path.join(BASE_DIR, filename)
        
        if not os.path.exists(filepath):
            print(f"Skipping {filename} (Not found)")
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Update status
        # Looser regex to catch variations
        new_content = re.sub(r">\s*\*\*Status\*\*:\s*`\[\s*\]`\s*Not Started", "> **Status**: `[x]` Completed", content)
        
        # If no change happened, maybe it's already started or different format?
        if content == new_content:
             # Try replacing "In Progress" or similar if needed, or just force it
             pass

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        # Move file
        try:
            shutil.move(filepath, os.path.join(COMPLETED_DIR, filename))
            print(f"Processed and moved {filename}")
        except Exception as e:
            print(f"Error moving {filename}: {e}")

if __name__ == "__main__":
    process_phases(28, 100)
