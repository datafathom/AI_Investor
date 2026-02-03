
import os

filepath = r"c:\Users\astir\Desktop\AI_Company\AI_Investor\frontend2\src\App.jsx"

with open(filepath, 'rb') as f:
    content = f.read()

# Filter out bytes > 127
sanitized = bytes([b for b in content if b <= 127])

with open(filepath, 'wb') as f:
    f.write(sanitized)

print("Sanitized App.jsx to ASCII-only.")
