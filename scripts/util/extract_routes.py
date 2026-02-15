import re
from pathlib import Path

def extract_routes():
    project_root = Path(__file__).parent.parent.parent
    input_file = project_root / "DEBUGGING" / "FrontEndAudit" / "Routes2Test" / "_NEW_ROUTES.txt"
    output_file = project_root / "DEBUGGING" / "FrontEndAudit" / "Routes2Test" / "verification_round_2.py"
    
    if not input_file.exists():
        print(f"Input file not found: {input_file}")
        return

    content = input_file.read_text(encoding='utf-8')
    
    # Extract URLs starting with http://localhost:5173
    # Stop at space, newline, closing parenthesis, or closing bracket
    url_pattern = r'http://localhost:5173[^\s\)\],]+'
    urls = re.findall(url_pattern, content)
    
    # Unique and sorted
    unique_urls = sorted(list(set(urls)))
    
    # Format as Python list
    lines = [
        '"""',
        'VERIFICATION ROUND 2 - URL LIST',
        'Extracted from _NEW_ROUTES.txt',
        '"""',
        '',
        'VERIFICATION_ROUTES = ['
    ]
    
    for u in unique_urls:
        lines.append(f"    \"{u}\",")
        
    lines.append("]")
    
    output_file.write_text("\n".join(lines), encoding='utf-8')
    print(f"Extracted {len(unique_urls)} unique URLs to {output_file.relative_to(project_root)}")

if __name__ == "__main__":
    extract_routes()
