
import re

with open('web/app.py', 'r') as f:
    lines = f.readlines()

blueprint_imports = []
new_lines = []
in_create_app = False

blueprint_pattern = re.compile(r'^\s+from (web\.api\.\S+) import (\S+)')

for i, line in enumerate(lines):
    if 'def create_app()' in line:
        in_create_app = True
        new_lines.append(line)
        continue
    
    match = blueprint_pattern.match(line)
    if in_create_app and match:
        module = match.group(1)
        variable = match.group(2)
        blueprint_imports.append(f"from {module} import {variable}")
        new_lines.append(f"    # {line.strip()} # MOVED TO TOP\n")
    else:
        new_lines.append(line)

# Add unique imports to top (after initial imports)
unique_imports = sorted(list(set(blueprint_imports)))
insert_pos = 0
for i, line in enumerate(new_lines):
    if 'from web.api' in line or 'print("Importing' in line:
        insert_pos = i
        break

if insert_pos == 0:
    insert_pos = 25 # Fallback

header = ["\n# --- AUTOMATICALLY CONSOLIDATED IMPORTS ---\n"]
header.extend([imp + "\n" for imp in unique_imports])
header.append("# ------------------------------------------\n\n")

final_lines = new_lines[:insert_pos] + header + new_lines[insert_pos:]

with open('web/app.py.new', 'w') as f:
    f.writelines(final_lines)

print(f"Generated web/app.py.new with {len(unique_imports)} unique consolidated imports.")
