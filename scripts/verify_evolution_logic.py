import requests
import time

BASE_URL = "http://localhost:5050/api/v1/evolution"

def test_evolution_logic():
    print("🚀 Verifying Evolution Lab Logic...")
    
    # 1. Auth Setup (Using fixed user to avoid "logging in again" redundancy)
    auth_url = "http://localhost:5050/api/auth/login"
    session = requests.Session()
    email = "audit@fathom.ai"
    password = "Password123!"
    headers = {}

    try:
        res = session.post(auth_url, json={"email": email, "password": password})
        if res.status_code == 200:
            token = res.json().get('token')
            headers = {"Authorization": f"Bearer {token}"}
            print("  [Auth] ✓ Session Active")
        else:
            # Try to register if missing, but only as fallback
            requests.post("http://localhost:5050/api/auth/register", json={"email": email, "password": password})
            res = session.post(auth_url, json={"email": email, "password": password})
            token = res.json().get('token')
            headers = {"Authorization": f"Bearer {token}"}
            print("  [Auth] ✓ Session Recovered")
    except:
        print("  [Auth] ❌ Auth context failed")
        return

    # 2. Initialize Evolution (Required for Ph 37 logic)
    try:
        print("  [Logic] Initializing Distillery...")
        requests.post(f"{BASE_URL}/start", headers=headers)
    except:
        pass

    # 3. Status Check
    try:
        res = requests.get(f"{BASE_URL}/status", headers=headers)
        if res.status_code == 200:
            print("  [API] ✓ Service Online")
        else:
            print(f"  [API] ❌ Status Check: {res.status_code}")
    except:
        print("  [API] ❌ Connection Failed")

    # 3. Initialize Evolution (Required for Ph 37 logic)
    try:
        print("  [Logic] Initializing Distillery...")
        res = requests.post(f"{BASE_URL}/start", headers=headers)
        if res.status_code == 200:
             print("  [Logic] ✓ Distillery Started")
        else:
             print(f"  [Logic] ❌ Failed to start Distillery: {res.text}")
    except Exception as e:
        print(f"  [Logic] ❌ Start Error: {e}")

    # 4. Status Check Again (Now should be 200)
    try:
        res = requests.get(f"{BASE_URL}/status")
        if res.status_code == 200:
            print("  [API] ✓ Status Verified")
        else:
            print(f"  [API] ❌ Status Failed: {res.status_code}")
    except:
        pass

    # 5. Test Splicing (New Payload)
    try:
        p1 = {"id": "p1", "genes": {"rsi_period": 14, "rsi_buy": 30, "rsi_sell": 70, "stop_loss": 0.05}}
        p2 = {"id": "p2", "genes": {"rsi_period": 21, "rsi_buy": 25, "rsi_sell": 75, "stop_loss": 0.08}}
        
        payload = {
            "parent1_id": p1['id'], "parent2_id": p2['id'],
            "parent1_genes": p1['genes'], "parent2_genes": p2['genes']
        }
        
        res = requests.post(f"{BASE_URL}/splice", json=payload, headers=headers)
        if res.status_code == 200:
            child = res.json()['data']
            print(f"  [Logic] ✓ Splicing Success: Created Hybrid")
        else:
            print(f"  [Logic] ❌ Splicing Failed: {res.text}")
    except Exception as e:
        print(f"  [Logic] ❌ Splicing Error: {e}")

if __name__ == "__main__":
    test_evolution_logic()
