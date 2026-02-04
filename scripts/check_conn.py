import requests

def check(url):
    try:
        r = requests.get(url, timeout=2)
        print(f"{url}: {r.status_code}")
    except Exception as e:
        print(f"{url}: FAILED - {e}")

check("http://localhost:5050/health")
check("http://127.0.0.1:5050/health")
check("http://localhost:5173")
check("http://127.0.0.1:5173")
