
import json
import os

config_path = r'c:\Users\astir\Desktop\AI_Company\AI_Investor\config\cli_configuration.json'

with open(config_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

def migrate_handlers(obj):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k == 'handler' and isinstance(v, str):
                if v.startswith('scripts.runners.test_'):
                    obj[k] = v.replace('scripts.runners.test_', 'tests.integration.test_')
            else:
                migrate_handlers(v)
    elif isinstance(obj, list):
        for item in obj:
            migrate_handlers(item)

migrate_handlers(config)

with open(config_path, 'w', encoding='utf-8') as f:
    json.dump(config, f, indent=4)

print("Migration complete.")
