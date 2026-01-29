import requests
import json

BASE_URL = "http://localhost:5050/api/v1/institutional"

def test_endpoints():
    print("🚀 Verifying Institutional Endpoints...")
    
    # We need a token for login_required endpoints. 
    # For simplicity in this verification step, I'll check if the backend is at least responding to /health
    try:
        health = requests.get("http://localhost:5050/health")
        print(f"Health Check: {health.status_code} - {health.json()}")
    except Exception as e:
        print(f"FAILED to reach backend: {e}")
        return

    # Check Public/Auth endpoints if any or try with mock token if possible
    # Given the complexity of auth, I will at least check if the blueprint is registered
    # by looking for a 405 or 401 instead of 404 on the new routes.
    
    routes = [
        ("/clients", "GET"),
        ("/analytics/fees", "GET"),
        ("/analytics/risk/test_client", "GET"),
        ("/analytics/signatures/test_client", "GET"),
        ("/analytics/allocation/test_client", "GET"),
        ("/client/create", "POST")
    ]
    
    for route, method in routes:
        url = BASE_URL + route
        try:
            if method == "GET":
                resp = requests.get(url)
            else:
                resp = requests.post(url, json={})
            
            # 401 Unauthorized is GOOD - it means the route exists and is protected by login_required
            # 404 would mean the route is NOT registered.
            if resp.status_code == 401:
                print(f"✅ Route {route} [{method}] is registered and protected (401).")
            elif resp.status_code == 200:
                print(f"✅ Route {route} [{method}] returned 200.")
            else:
                print(f"ℹ️ Route {route} [{method}] returned {resp.status_code}.")
        except Exception as e:
            print(f"❌ Route {route} [{method}] FAILED: {e}")

if __name__ == "__main__":
    test_endpoints()
