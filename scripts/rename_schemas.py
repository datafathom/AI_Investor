import os
import re

SCHEMA_DIR = r"c:\Users\astir\Desktop\AI_Company\AI_Investor\schemas\postgres"

def rename_files():
    files = os.listdir(SCHEMA_DIR)
    renamed_count = 0
    
    # Regex patterns to strip
    # 1. Leading digits and underscore: "000_init.sql" -> "init.sql"
    # 2. Phase prefixes: "phase1_001_workspaces.sql" -> "workspaces.sql"
    
    # We'll use a specific set of patterns
    # pattern 1: ^\d{3}_(.*) -> captures everything after "000_"
    # pattern 2: ^phase\d+_\d{3}_(.*) -> captures everything after "phaseX_00Y_"
    # pattern 3: ^phase_\d+_(.*) -> captures everything after "phase_29_" (seen in list)
    # pattern 4: ^\d+_(.*) -> captures "66_fund_data.sql" -> "fund_data.sql"
    
    for filename in files:
        if not filename.endswith(".sql"):
            continue
            
        old_path = os.path.join(SCHEMA_DIR, filename)
        new_name = filename
        
        # Try phase patterns first (more specific)
        match_phase = re.match(r"^phase\d*_\d{3}_(.*)", filename) # Matches phase1_001_... or phase_001_...
        if match_phase:
            new_name = match_phase.group(1)
        else:
            # Try simple phase_XX pattern
            match_phase_simple = re.match(r"^phase_\d+_(.*)", filename)
            if match_phase_simple:
                new_name = match_phase_simple.group(1)
            else:
                 # Try digit prefix
                match_digits = re.match(r"^\d+_(.*)", filename)
                if match_digits:
                    new_name = match_digits.group(1)

        if new_name != filename:
            # Check for collision
            new_path = os.path.join(SCHEMA_DIR, new_name)
            if os.path.exists(new_path):
                print(f"Skipping {filename} -> {new_name} (Collision)")
                continue
                
            print(f"Renaming: {filename} -> {new_name}")
            os.rename(old_path, new_path)
            renamed_count += 1
            
    print(f"Renamed {renamed_count} files.")

if __name__ == "__main__":
    rename_files()
