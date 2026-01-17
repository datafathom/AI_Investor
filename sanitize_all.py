
import os
from pathlib import Path

pages_dir = Path(r"c:\Users\astir\Desktop\AI_Company\AI_Investor\frontend2\src\pages")

for file in pages_dir.glob("*.jsx"):
    print(f"Sanitizing {file.name}...")
    with open(file, 'rb') as f:
        content = f.read()
    
    # Filter out bytes > 127
    sanitized = bytes([b for b in content if b <= 127])
    
    with open(file, 'wb') as f:
        f.write(sanitized)

print("All page components sanitized.")
