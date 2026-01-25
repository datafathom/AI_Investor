
import re
import os

# 1. Gather all Blueprint variable to module mappings
mappings = {}

def scan_dir(directory, sub_path):
    for filename in os.listdir(directory):
        if filename.endswith('.py'):
            module_name = filename[:-3]
            with open(os.path.join(directory, filename), 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                # Find variable = Blueprint(...)
                matches = re.findall(r'^(\w+)\s*=\s*Blueprint', content, re.MULTILINE)
                for var in matches:
                    if var not in mappings:
                        mappings[var] = f"{sub_path}.{module_name}"

scan_dir('web/api', 'web.api')
scan_dir('web/routes', 'web.routes')

# 2. Read app.py and find all registered blueprints
with open('web/app.py', 'r', encoding='utf-8') as f:
    orig_lines = f.readlines()

registrations = []
for line in orig_lines:
    match = re.search(r'app\.register_blueprint\((\w+)', line)
    if match:
        registrations.append(match.group(1))

# Uniq sorted needed variables
needed_vars = sorted(list(set(registrations)))

# Build new import lines
new_import_lines = []
for var in needed_vars:
    if var in mappings:
        new_import_lines.append(f"from {mappings[var]} import {var}")
    else:
        print(f"Warning: Could not find source for {var}")

# 3. Process app.py: strip all internal/legacy imports and inject new ones
final_lines = []
in_create_app = False
imports_injected = False

for line in orig_lines:
    # Identify create_app boundary
    if 'def create_app()' in line:
        in_create_app = True
        final_lines.append(line)
        continue
    
    # Identify top-level script boundary
    if "if __name__ == '__main__':" in line:
        in_create_app = False
        final_lines.append(line)
        continue

    # Strip existing imports (legacy ones, top-level ones we'll replace, and internal ones)
    if re.match(r'^(\s+)?from (web\.api|web\.routes)', line) or re.match(r'^(\s+)?import .*_bp', line) or "# STRIPPED LOCAL IMPORT" in line or "# MOVED TO TOP" in line:
        # If we are at the top level and haven't injected yet, use this as a placeholder
        if not in_create_app and not imports_injected:
            final_lines.append("\n# --- MASTER CONSOLIDATED IMPORTS ---\n")
            for imp in sorted(list(set(new_import_lines))):
                final_lines.append(f"{imp}\n")
            final_lines.append("# --- FINISHED CONSOLIDATION ---\n\n")
            imports_injected = True
        continue
        
    final_lines.append(line)

# Handle case where no imports were found to trigger injection
if not imports_injected:
    final_lines.insert(25, "\n# --- MASTER CONSOLIDATED IMPORTS ---\n")
    for imp in sorted(list(set(new_import_lines))):
        final_lines.insert(26, f"{imp}\n")
    final_lines.insert(26 + len(new_import_lines), "# --- FINISHED CONSOLIDATION ---\n\n")

with open('web/app.py.master', 'w', encoding='utf-8') as f:
    f.writelines(final_lines)

print("Generated web/app.py.master")
