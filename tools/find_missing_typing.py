import os
from pathlib import Path

def find_missing_typing():
    typing_needed = ['List', 'Dict', 'Any', 'Optional', 'Tuple', 'Union']
    root = Path('services')
    
    print("Scanning for missing typing imports...")
    
    for p in root.rglob('*.py'):
        try:
            content = p.read_text(encoding='utf-8', errors='ignore')
            lines = content.splitlines()
            
            # Check if typing is imported at all
            typing_import_line = next((line for line in lines if 'from typing import' in line), None)
            
            missing = []
            for t in typing_needed:
                # Check if the type is used in the file
                # Use simple heuristic: "-> T[" or ": T[" or " T[" to avoid false positives in comments/strings
                is_used = (f'-> {t}[' in content or 
                          f': {t}[' in content or 
                          f' {t}[' in content or
                          f'-> {t}' in content or # e.g. -> List
                          f': {t}' in content)    # e.g. : List
                
                if is_used:
                    if not typing_import_line:
                        missing.append(t)
                    elif f' {t}' not in typing_import_line and f',{t}' not in typing_import_line:
                         # Very basic check, might have false positives if multi-line import
                        missing.append(t)
            
            if missing:
                print(f"{p}: missing {missing}")
                
        except Exception as e:
            print(f"Error reading {p}: {e}")

if __name__ == "__main__":
    find_missing_typing()
