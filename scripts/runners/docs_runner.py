import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def combine_docs(doc_type: str, **kwargs):
    """
    Combines all .md files in docs/[doc_type] into docs_combined/[doc_type]_combined.md.
    Supports aliases like 'routes' -> 'frontend/routes' and 'api' -> 'api/api_commands'.
    """
    project_root = Path(__file__).parent.parent.parent
    
    # Alias mapping
    aliases = {
        "routes": "frontend/routes",
        "api": "api/api_commands"
    }
    
    actual_type = aliases.get(doc_type, doc_type)
    src_dir = project_root / "docs" / actual_type
    dest_dir = project_root / "docs_combined"
    
    # Use the alias name for the output file if it was used
    output_name = doc_type if doc_type in aliases else actual_type.replace("/", "_").replace("\\", "_")
    dest_file = dest_dir / f"{output_name}_combined.md"

    if not src_dir.exists() or not src_dir.is_dir():
        print(f"Error: Source directory {src_dir} does not exist.")
        return

    # Create destination directory if it doesn't exist
    dest_dir.mkdir(parents=True, exist_ok=True)

    print(f"Combining docs from {src_dir} into {dest_file}...")

    md_files = sorted(list(src_dir.rglob("*.md")))
    if not md_files:
        print(f"No .md files found in {src_dir}.")
        return

    combined_content = [f"# {doc_type.capitalize()} - Combined Documentation\n"]
    combined_content.append(f"Auto-generated on: {os.popen('date /t').read().strip()} {os.popen('time /t').read().strip()}\n\n")
    combined_content.append("---\n\n")

    for md_file in md_files:
        relative_path = md_file.relative_to(src_dir)
        print(f"  Adding: {relative_path}")
        
        with open(md_file, "r", encoding="utf-8") as f:
            content = f.read()
            
        combined_content.append(f"## Source: {relative_path}\n\n")
        combined_content.append(content)
        combined_content.append("\n\n---\n\n")

    with open(dest_file, "w", encoding="utf-8") as f:
        f.write("".join(combined_content))

    print(f"\nSuccess! Combined {len(md_files)} files into {dest_file}")

if __name__ == "__main__":
    # Test call
    combine_docs("services")
