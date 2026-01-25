
import re

with open('web/app.py', 'r') as f:
    lines = f.readlines()

new_lines = []
in_create_app = False

# Match local imports like:
# from web.api.xxx_api import xxx_bp
# from web.api.xxx_api import xxx_bp as yyy
# and also Phase-based comments followed by them
blueprint_pattern = re.compile(r'^\s+(from web\.api|import .*_bp)')

for line in lines:
    if 'def create_app()' in line:
        in_create_app = True
        new_lines.append(line)
        continue
    
    if in_create_app:
        # Stop at main block
        if "if __name__ == '__main__':" in line:
            in_create_app = False
            new_lines.append(line)
            continue
            
        if blueprint_pattern.match(line):
            new_lines.append(f"    # {line.strip()} # STRIPPED LOCAL IMPORT\n")
        else:
            new_lines.append(line)
    else:
        new_lines.append(line)

with open('web/app.py.clean', 'w') as f:
    f.writelines(new_lines)

print("Generated web/app.py.clean with all local blueprint imports stripped.")
