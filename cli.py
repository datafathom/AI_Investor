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
import io
from pathlib import Path

# Add project root to path
_project_root = Path(__file__).parent
sys.path.insert(0, str(_project_root))

# Force UTF-8 and Line-Buffering on Windows to prevent terminal stalling
if sys.platform == 'win32':
    # Wrap buffer in TextIOWrapper with line_buffering=True
    if not isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace', line_buffering=True)
    if not isinstance(sys.stderr, io.TextIOWrapper):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace', line_buffering=True)

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
                    val = raw_args[i + 1]
                    target_type = flag_def.get("type", "string")
                    
                    if target_type == "integer":
                        try:
                            val = int(val)
                        except ValueError:
                            print(f"Error: Flag --{actual_flag_name} expects integer, got '{val}'", file=sys.stderr)
                            sys.exit(1)
                    elif target_type == "float":
                        try:
                            val = float(val)
                        except ValueError:
                            print(f"Error: Flag --{actual_flag_name} expects float, got '{val}'", file=sys.stderr)
                            sys.exit(1)
                            
                    flags[actual_flag_name] = val
                    i += 1
        elif arg.startswith("-") and not arg.startswith("--"):
            short_name = arg[1:]
            if short_name in flag_lookup:
                flag_def = flag_lookup[short_name]
                if flag_def.get("type") == "boolean":
                    flags[flag_def["name"]] = True
                else:
                    if i + 1 < len(raw_args):
                        val = raw_args[i + 1]
                        target_type = flag_def.get("type", "string")
                        
                        if target_type == "integer":
                            try:
                                val = int(val)
                            except ValueError:
                                print(f"Error: Flag -{short_name} expects integer, got '{val}'", file=sys.stderr)
                                sys.exit(1)
                        elif target_type == "float":
                            try:
                                val = float(val)
                            except ValueError:
                                print(f"Error: Flag -{short_name} expects float, got '{val}'", file=sys.stderr)
                                sys.exit(1)
                                
                        flags[flag_def["name"]] = val
                        i += 1
        else:
            if len(args) < len(arg_defs):
                arg_def = arg_defs[len(args)]
                val = arg
                target_type = arg_def.get("type", "string")
                
                if target_type == "integer":
                    try:
                        val = int(val)
                    except ValueError:
                        print(f"Error: Argument <{arg_def['name']}> expects integer, got '{val}'", file=sys.stderr)
                        sys.exit(1)
                elif target_type == "float":
                    try:
                        val = float(val)
                    except ValueError:
                        print(f"Error: Argument <{arg_def['name']}> expects float, got '{val}'", file=sys.stderr)
                        sys.exit(1)
                        
                args[arg_def["name"]] = val
        
        i += 1
    
    # Fill defaults and validate required
    missing_required = []
    for arg_def in arg_defs:
        if arg_def["name"] not in args:
            if "default" in arg_def:
                args[arg_def["name"]] = arg_def["default"]
            elif arg_def.get("required", False):
                missing_required.append(arg_def["name"])
            else:
                args[arg_def["name"]] = None
                
    if missing_required:
        print(f"Error: Missing required argument(s): {', '.join(missing_required)}", file=sys.stderr, flush=True)
        # Usage hint
        usage = f"Usage: python cli.py {' '.join(command_path)}"
        for arg_def in arg_defs:
            if arg_def.get("required"):
                usage += f" <{arg_def['name']}>"
            else:
                usage += f" [{arg_def['name']}]"
        print(usage, file=sys.stderr, flush=True)
        sys.exit(1)

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
    
    # Group commands by category
    categories = {}
    for cmd_name, cmd_def in commands.items():
        cat = cmd_def.get("category", "General")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append((cmd_name, cmd_def.get("description", "")))
    
    # Sort categories to ensure consistent output (General at the top)
    sorted_cats = sorted(categories.keys())
    if "General" in sorted_cats:
        sorted_cats.remove("General")
        sorted_cats.insert(0, "General") # Put General at the top
        
    for cat in sorted_cats:
        print(f"\n[{cat}]")
        for cmd_name, desc in sorted(categories[cat]):
            print(f"  {cmd_name:25} {desc}")

    print("\nDevelopment Modes Summary:")
    print("  dev                      Standard mode: Backend + Frontend + Local Infra Check.")
    print("  dev-full                 Full mode: Starts Docker Infra + Backend + Frontend.")
    print("  dev-no-db                Light mode: Backend + Frontend only (for remote DB/2-node).")
    print("\nUse 'python cli.py <command> --help' for detailed information on a specific command.")


def print_command_help(command_path: list, cmd_def: dict):
    print(f"\nCommand: {' '.join(command_path)}")
    print(f"Description: {cmd_def.get('description', 'No description available.')}")
    
    arg_defs = cmd_def.get("arguments", [])
    if arg_defs:
        print("\nArguments:")
        for arg in arg_defs:
            req = "(Required)" if arg.get("required") else f"(Optional, Default: {arg.get('default')})"
            print(f"  {arg['name']:20} {arg.get('help', '')} {req}")
            
    flag_defs = cmd_def.get("flags", [])
    if flag_defs:
        print("\nFlags:")
        for flag in flag_defs:
            short = f"-{flag['short']}, " if "short" in flag else ""
            print(f"  {short}--{flag['name']:18} {flag.get('help', '')} (Default: {flag.get('default')})")

    if "subcommands" in cmd_def:
        print("\nAvailable subcommands:")
        for subcmd_name, subcmd_def in sorted(cmd_def["subcommands"].items()):
            print(f"  {subcmd_name:20} {subcmd_def.get('description', '')}")
            
    print()


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
    
    # We need to iterate carefully. Once we hit a non-command arg, everything else is args.
    # But we also need to handle nested subcommands.
    
    arg_iter = iter(sys.argv[1:])
    for arg in arg_iter:
        if parsing_args:
            raw_args.append(arg)
            continue
            
        # Try to resolve next step in path
        test_path = command_path + [arg]
        test_cmd = registry.get_command(test_path)
        
        if test_cmd:
            command_path.append(arg)
            # If this command has NO subcommands, we are done parsing path
            if "subcommands" not in test_cmd:
                parsing_args = True
        else:
            # Current arg is not a command/subcommand -> it's an argument
            parsing_args = True
            raw_args.append(arg)
            
    cmd_def = registry.get_command(command_path)
    if not cmd_def:
        print(f"Error: Unknown command: {' '.join(command_path)}", file=sys.stderr, flush=True)
        print_help(registry)
        sys.exit(1)

    # Check for help flag in raw_args
    if "--help" in raw_args or "-h" in raw_args:
        print_command_help(command_path, cmd_def)
        sys.exit(0)
    
    if "subcommands" in cmd_def and not cmd_def.get("handler"):
        print(f"Command: {' '.join(command_path)}")
        print("Available subcommands:")
        for subcmd_name, subcmd_def in sorted(cmd_def["subcommands"].items()):
            print(f"  {subcmd_name:20} {subcmd_def.get('description', '')}")
        sys.exit(0)
    
    handler = registry.get_handler(command_path)
    if not handler:
        print(f"Error: Handler not found for: {' '.join(command_path)}", file=sys.stderr, flush=True)
        sys.exit(1)
    
    try:
        args, flags = parse_args(command_path, cmd_def, raw_args)
        handler(**args, **flags)
        
        # Check for post_handler (sequential execution)
        post_handler_path = cmd_def.get("post_handler")
        if post_handler_path:
            # Re-resolve using the registry's own import logic to avoid duplicate code
            mod_path, func_name = post_handler_path.rsplit(":", 1)
            import importlib
            mod = importlib.import_module(mod_path)
            p_handler = getattr(mod, func_name)
            p_handler(**args, **flags)
            
    except Exception as e:
        logger.exception(f"Error executing command: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
