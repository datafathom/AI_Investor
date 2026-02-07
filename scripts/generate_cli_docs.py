import json
import subprocess
import os
from pathlib import Path

def run_command(cmd_list):
    try:
        result = subprocess.run(
            cmd_list,
            capture_output=True,
            text=True,
            shell=True
        )
        return result.stdout
    except Exception as e:
        return f"Error running {' '.join(cmd_list)}: {e}"

def generate_docs():
    config_path = Path("config/cli_configuration.json")
    output_dir = Path("docs/cli/cli_commands")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(config_path, "r", encoding="utf-8") as f:
        config = json.load(f)
    
    commands = config.get("commands", {})
    
    for cmd_name, cmd_def in commands.items():
        print(f"Documenting: {cmd_name}")
        md_content = f"# CLI Command: {cmd_name}\n\n"
        md_content += f"## Description\n{cmd_def.get('description', 'No description available.')}\n\n"
        
        # Get Main Help
        main_help = run_command(["python", "cli.py", cmd_name, "--help"])
        md_content += f"## Main Help Output\n```text\n{main_help}\n```\n\n"
        
        # Handle Subcommands recursively
        def process_subcommands(sub_cmds, path_prefix):
            nonlocal md_content
            for sub_name, sub_def in sub_cmds.items():
                full_path = path_prefix + [sub_name]
                print(f"  Subcommand: {' '.join(full_path)}")
                md_content += f"### Subcommand: `{' '.join(full_path)}`\n"
                md_content += f"{sub_def.get('description', '')}\n\n"
                
                sub_help = run_command(["python", "cli.py"] + full_path + ["--help"])
                md_content += f"#### Help Output\n```text\n{sub_help}\n```\n\n"
                
                if "subcommands" in sub_def:
                    process_subcommands(sub_def["subcommands"], full_path)

        if "subcommands" in cmd_def:
            md_content += "## Subcommands\n\n"
            process_subcommands(cmd_def["subcommands"], [cmd_name])
            
        file_path = output_dir / f"cli_{cmd_name}.md"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(md_content)

if __name__ == "__main__":
    generate_docs()
