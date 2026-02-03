
import os

filepath = r"c:\Users\astir\Desktop\AI_Company\AI_Investor\frontend2\src\App.jsx"

with open(filepath, 'rb') as f:
    content = f.read()

for i, byte in enumerate(content):
    if byte > 127:
        # Find line number
        line_num = content[:i].count(b'\n') + 1
        char = content[i:i+1].decode('latin-1')
        print(f"Non-ASCII at line {line_num}, index {i}: byte {byte}, char '{char}'")
