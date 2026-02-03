with open('frontend2/src/App.jsx', 'r', encoding='utf-8') as f:
    lines = f.readlines()

target_lines = range(2520, 2550)
for i in target_lines:
    if i < len(lines):
        print(f"{i+1}: {repr(lines[i])}")
