path = 'frontend2/src/App.jsx'
with open(path, 'r', encoding='utf-8', errors='ignore') as f:
    content = f.read()

# Clean up any potential garbage patterns seen in debug
if "n'tPage" in content:
    content = content.replace("n'tPage", "currentPage")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
