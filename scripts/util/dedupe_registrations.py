
import re

with open('web/app.py', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. Identify all register_blueprint calls
# We'll use a map to store the last line index for each blueprint
bp_to_last_index = {}
for i, line in enumerate(lines):
    match = re.search(r'app\.register_blueprint\((\w+)', line)
    if match:
        bp_name = match.group(1)
        if not line.strip().startswith('#'): # Only count uncommented ones
            bp_to_last_index[bp_name] = i

# 2. Comment out any register_blueprint call that isn't the last one
new_lines = []
for i, line in enumerate(lines):
    match = re.search(r'app\.register_blueprint\((\w+)', line)
    if match:
        bp_name = match.group(1)
        if not line.strip().startswith('#') and bp_to_last_index.get(bp_name) != i:
            new_lines.append(f"    # {line.strip()} # REMOVED DUPLICATE REGISTRATION\n")
            continue
    new_lines.append(line)

with open('web/app.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("SUCCESS: Deduplicated app.register_blueprint calls.")
