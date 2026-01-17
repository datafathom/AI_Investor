"""
==============================================================================
FILE: cli.py
ROLE: Unified CLI Entry Point
PURPOSE: Orchestrates all AI Investor commands via a JSON-based registry.
USAGE: python cli.py [command] [subcommand] --args
INPUT/OUTPUT:
    - Input: Sys.argv (CLI arguments)
    - Output: Dispatches to specific service/runner handlers.
==============================================================================
"""

import sys
from pathlib import Path


# Add project root to path
_project_root = Path(__file__).parent
sys.path.insert(0, str(_project_root))

# Delay heavy imports
# from utils.registry.command_registry import CommandRegistry
# from utils.logging import setup_logging
import logging

def setup_logger_lazy():
    from utils.logging import setup_logging
    setup_logging()
    return logging.getLogger(__name__)

logger = None # Will init in main



def parse_args(command_path: list, cmd_def: dict, raw_args: list) -> tuple[dict, dict]:
    args = {}
    flags = {}
    
    arg_defs = cmd_def.get("arguments", [])
    flag_defs = cmd_def.get("flags", [])
    
    flag_lookup = {}
    for flag_def in flag_defs:
        flag_lookup[flag_def["name"]] = flag_def
        if "short" in flag_def:
            flag_lookup[flag_def["short"]] = flag_def
    
    i = 0
    while i < len(raw_args):
        arg = raw_args[i]
        
        if arg.startswith("--"):
            flag_name = arg[2:]
            if flag_name not in flag_lookup:
                flag_name_underscore = flag_name.replace("-", "_")
                if flag_name_underscore in flag_lookup:
                    flag_name = flag_name_underscore
                else:
                    i += 1
                    continue
            
            flag_def = flag_lookup[flag_name]
            actual_flag_name = flag_def["name"]
            if flag_def.get("type") == "boolean":
                flags[actual_flag_name] = True
            else:
                if i + 1 < len(raw_args):
                    flags[actual_flag_name] = raw_args[i + 1]
                    i += 1
        elif arg.startswith("-") and not arg.startswith("--"):
            short_name = arg[1:]
            if short_name in flag_lookup:
                flag_def = flag_lookup[short_name]
                if flag_def.get("type") == "boolean":
                    flags[flag_def["name"]] = True
                else:
                    if i + 1 < len(raw_args):
                        flags[flag_def["name"]] = raw_args[i + 1]
                        i += 1
        else:
            if len(args) < len(arg_defs):
                arg_def = arg_defs[len(args)]
                args[arg_def["name"]] = arg
        
        i += 1
    
    # Fill defaults
    for arg_def in arg_defs:
        if arg_def["name"] not in args:
            if "default" in arg_def:
                args[arg_def["name"]] = arg_def["default"]
            elif not arg_def.get("required", False):
                args[arg_def["name"]] = None
                
    for flag_def in flag_defs:
        if flag_def["name"] not in flags:
            if "default" in flag_def:
                flags[flag_def["name"]] = flag_def["default"]

    # Convert flags to underscores
    flags_fixed = {}
    for key, value in flags.items():
        fixed_key = key.replace("-", "_")
        flags_fixed[fixed_key] = value
    flags = flags_fixed
    
    return args, flags


def print_help(registry):
    print("AI Investor CLI")
    print("\nAvailable commands:")
    commands = registry.list_commands()
    for cmd_name, cmd_def in sorted(commands.items()):
        desc = cmd_def.get("description", "")
        print(f"  {cmd_name:20} {desc}")


def main():
    global logger
    logger = setup_logger_lazy()
    
    from utils.registry.command_registry import CommandRegistry
    registry = CommandRegistry()
    if not registry.load_config():
        print("Error: Failed to load CLI configuration", file=sys.stderr)
        sys.exit(1)
    
    if len(sys.argv) < 2:
        print_help(registry)
        sys.exit(1)
    
    # Simple recursive parsing logic
    command_path = []
    raw_args = []
    parsing_args = False
    
    for arg in sys.argv[1:]:
        if not parsing_args:
            test_path = command_path + [arg]
            test_cmd = registry.get_command(test_path)
            
            if test_cmd:
                command_path.append(arg)
            else:
                current_cmd = registry.get_command(command_path)
                if current_cmd and "subcommands" in current_cmd:
                    subcommands = current_cmd.get("subcommands", {})
                    if arg in subcommands:
                        command_path.append(arg)
                    else:
                        parsing_args = True
                        raw_args.append(arg)
                else:
                    parsing_args = True
                    raw_args.append(arg)
        else:
            raw_args.append(arg)
    
    cmd_def = registry.get_command(command_path)
    if not cmd_def:
        print(f"Error: Unknown command: {' '.join(command_path)}", file=sys.stderr)
        print_help(registry)
        sys.exit(1)
    
    if "subcommands" in cmd_def and not cmd_def.get("handler"):
        print(f"Command: {' '.join(command_path)}")
        print("Available subcommands:")
        for subcmd_name, subcmd_def in sorted(cmd_def["subcommands"].items()):
            print(f"  {subcmd_name:20} {subcmd_def.get('description', '')}")
        sys.exit(0)
    
    handler = registry.get_handler(command_path)
    if not handler:
        print(f"Error: Handler not found for: {' '.join(command_path)}", file=sys.stderr)
        sys.exit(1)
    
    try:
        args, flags = parse_args(command_path, cmd_def, raw_args)
        handler(**args, **flags)
    except Exception as e:
        logger.exception(f"Error executing command: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
