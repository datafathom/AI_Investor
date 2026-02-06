import os
import re

def find_fastapi_app(root_dir):
    pattern = re.compile(r'FastAPI\(', re.IGNORECASE)
    for root, dirs, files in os.walk(root_dir):
        if 'venv' in dirs: dirs.remove('venv')
        if 'node_modules' in dirs: dirs.remove('node_modules')
        if '.git' in dirs: dirs.remove('.git')
        
        for file in files:
            if file.endswith('.py'):
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        if pattern.search(f.read()):
                            print(f"FOUND in: {path}")
                except Exception:
                    pass

if __name__ == "__main__":
    find_fastapi_app(".")
