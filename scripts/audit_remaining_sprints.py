import os
import requests

def check_file(path, description):
    exists = os.path.exists(path)
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {path}")
    return exists

def check_endpoint(url, method="GET"):
    try:
        if method == "GET":
             resp = requests.get(url)
        else:
             resp = requests.post(url)
        
        # 401 or 200 means it's registered
        if resp.status_code in [200, 401, 405]:
            print(f"✅ API {url} [{method}]: Verified (Status {resp.status_code})")
            return True
        else:
            print(f"❌ API {url} [{method}]: Failed (Status {resp.status_code})")
            return False
    except:
        print(f"❌ API {url} [{method}]: Connection Refused")
        return False

print("\n--- SPRINT 3: MASTER ORCHESTRATOR ---")
check_file("services/neo4j/neo4j_service.py", "Neo4j Service")
check_file("web/api/master_orchestrator_api.py", "Master API")
check_file("frontend2/src/widgets/Graph/NodeConnectionHeatmap.jsx", "Widget: Heatmap")
check_file("frontend2/src/widgets/Graph/ReflexivityEcho.jsx", "Widget: Reflexivity")
check_file("frontend2/src/pages/MasterOrchestrator.jsx", "Page: Master Orchestrator")
check_endpoint("http://localhost:5050/api/v1/master/graph")

print("\n--- SPRINT 4: EVOLUTION LAB ---")
check_file("services/evolution/evolution_service.py", "Evolution Service")
check_file("web/api/evolution_api.py", "Evolution API")
check_file("frontend2/src/widgets/Evolution/FitnessSurface3D.jsx", "Widget: Fitness 3D")
check_file("frontend2/src/widgets/Evolution/GeneFrequencyPlot.jsx", "Widget: Gene Plot")
check_file("frontend2/src/pages/EvolutionDashboard.jsx", "Page: Evolution Lab") # Guessing name
check_endpoint("http://localhost:5050/api/v1/evolution/status")

print("\n--- SPRINT 5: SYSTEM ZENITH ---")
check_file("frontend2/src/components/Taskbar/Taskbar.jsx", "Component: Taskbar")
check_file("frontend2/src/components/WindowManager/WindowWrapper.jsx", "Component: WinWrapper")
check_file("frontend2/src/components/KillSwitch/KillSwitch.jsx", "Component: KillSwitch")
check_endpoint("http://localhost:5050/api/v1/system/kill-switch", "POST")
