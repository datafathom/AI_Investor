
import re

with open('web/app.py', 'r') as f:
    full_content = f.read()

# Find all registrations like app.register_blueprint(xxx_bp) or app.register_blueprint(xxx_api)
# We also want to capture the module name if it's in a comment like # STRIPPED LOCAL IMPORT
register_pattern = re.compile(r'app\.register_blueprint\((\w+)[,\)]')
internal_import_pattern = re.compile(r'# from (web\.api\.\S+) import (\w+) # STRIPPED LOCAL IMPORT')

registrations = register_pattern.findall(full_content)
stripped_imports = internal_import_pattern.findall(full_content)

# Map variable name to module
var_to_mod = {var: mod for mod, var in stripped_imports}

# List of blueprints we need to ensure are at the top
needed_blueprints = sorted(list(set(registrations)))

print(f"Blueprints found in registrations: {len(needed_blueprints)}")

new_imports = []
for bp in needed_blueprints:
    if bp in var_to_mod:
        new_imports.append(f"from {var_to_mod[bp]} import {bp}")
    else:
        # If we don't have a mapping, try to guess or use previous ones
        # and print warning
        print(f"Warning: No source module found for {bp}")

lines = full_content.splitlines()
insert_pos = 0
for i, line in enumerate(lines):
    if line.startswith('from web.api') or line.startswith('# from web.api'):
        insert_pos = i
        break

if insert_pos == 0: insert_pos = 25

header = ["\n# --- AUTOMATICALLY SYNCED IMPORTS ---"]
header.extend(sorted(list(set(new_imports))))
header.append("# ------------------------------------\n")

final_lines = lines[:insert_pos] + header + lines[insert_pos:]

with open('web/app.py.sync', 'w') as f:
    f.write('\n'.join(final_lines) + '\n')

print("Generated web/app.py.sync")
