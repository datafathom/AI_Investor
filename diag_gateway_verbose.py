import sys
import os
import time

sys.path.append(os.getcwd())

def trace_imports(frame, event, arg):
    if event == 'import' or event == 'call':
        return trace_imports
    return None

# sys.settrace(trace_imports)

print("Starting Trace of web.fastapi_gateway...")

# Manual step-by-step import simulation
try:
    print("1. Importing logging, asyncio, fastapi...")
    import logging
    import asyncio
    from fastapi import FastAPI, Request
    from fastapi.middleware.cors import CORSMiddleware
    
    print("2. Importing web.socket_gateway...")
    import web.socket_gateway
    print("   - SUCCESS: web.socket_gateway")

    print("3. Importing web.api.health_api...")
    from web.api import health_api
    print("4. Importing web.api.auth_api...")
    from web.api import auth_api
    print("5. Importing web.api.system_api...")
    from web.api import system_api
    print("6. Importing web.api.agents_api...")
    from web.api import agents_api
    print("7. Importing web.api.dev_api...")
    from web.api import dev_api
    print("8. Importing web.api.debate_api...")
    from web.api import debate_api
    print("9. Importing web.api.departments_api...")
    from web.api import departments_api
    print("10. Importing web.api.admin...")
    from web.api import admin
    print("   - SUCCESS: web.api.admin")

    print("11. Importing web.websocket.event_bus_ws...")
    from web.websocket.event_bus_ws import eb_socket_app
    print("   - SUCCESS: web.websocket.event_bus_ws")

    print("12. Importing services.notifications.slack_service...")
    from services.notifications.slack_service import get_slack_service
    print("   - SUCCESS: slack_service")

    print("All critical imports completed!")

except Exception as e:
    import traceback
    print("\n!!! IMPORT FAILED !!!")
    traceback.print_exc()
