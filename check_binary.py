with open('frontend2/src/App.jsx', 'rb') as f:
    data = f.read()

# Search for the pattern around line 2530
lines = data.split(b'\n')
for i in range(2520, 2550):
    if i < len(lines):
        print(f"{i+1}: {lines[i]}")
