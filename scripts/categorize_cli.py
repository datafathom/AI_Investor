import json
import os

CONFIG_PATH = "config/cli_configuration.json"

def categorize_commands():
    with open(CONFIG_PATH, 'r') as f:
        config = json.load(f)

    commands = config.get("commands", {})
    
    mapping = {
        "System Control": [
            "start-all", "stop-all", "check-backend", "check-port", "check-runtimes", 
            "reset-dev", "demo-start", "verify-pipeline", "speedtest", "docker-ps"
        ],
        "Development & Infrastructure": [
            "dev", "dev-full", "dev-no-db", "build-frontend", "clean-build", 
            "docker", "infra", "git-leaks"
        ],
        "API & Documentation": ["api"],
        "Unified Family Office (UFO)": [
            "sfo", "mfo", "hr", "network", "deal", "syndication", "lend", "ppli", "governance"
        ],
        "Private Markets": ["pe", "vc"],
        "Advanced AI Engines": ["research", "sentinel", "hedge", "defense", "orch"],
        "Alternative Assets": ["alts", "credit", "priv"],
        "Risk & Compliance": [
            "georisk", "bridge", "expat", "fatca", "rule144", "reflex", "risk", "plan"
        ],
        "Data & Analytics": [
            "backfill-history", "persist-trends", "pip-benchmark", "pip-test"
        ],
        "Demo & Simulation": ["demo-reset", "demo-trade"]
    }

    # Reverse mapping for easy lookup
    cat_lookup = {}
    for cat, cmds in mapping.items():
        for cmd in cmds:
            cat_lookup[cmd] = cat

    for cmd_name, cmd_def in commands.items():
        if cmd_name.startswith("test-") or cmd_name == "test":
            cmd_def["category"] = "Verification & Testing"
        elif cmd_name in cat_lookup:
            cmd_def["category"] = cat_lookup[cmd_name]
        else:
            # Default or heuristic
            if "test" in cmd_name:
                cmd_def["category"] = "Verification & Testing"
            else:
                cmd_def["category"] = "General"

    with open(CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=4)

    print(f"✅ Categorized {len(commands)} commands in {CONFIG_PATH}")

if __name__ == "__main__":
    categorize_commands()
