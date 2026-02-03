"""
Quick test script to verify API endpoints are working
"""
import requests
import time

BASE_URL = "http://localhost:5050"

def test_endpoint(path, method="GET", data=None):
    """Test an API endpoint"""
    try:
        url = f"{BASE_URL}{path}"
        if method == "GET":
            response = requests.get(url, timeout=5)
        else:
            response = requests.post(url, json=data, timeout=5)
        return response.status_code < 500, response.status_code
    except Exception as e:
        return False, str(e)

def main():
    print("Testing API endpoints...")
    
    endpoints = [
        ("/api/v1/analytics/performance-attribution?portfolio_id=test", "GET"),
        ("/api/news/trending?limit=5", "GET"),
        ("/api/watchlist/create", "POST", {"user_id": "test", "watchlist_name": "Test"}),
        ("/api/ai-predictions/price", "POST", {"symbol": "AAPL", "time_horizon": "1m"}),
        ("/api/ai-assistant/conversation/create", "POST", {"user_id": "test"}),
    ]
    
    results = []
    for endpoint, method, *args in endpoints:
        data = args[0] if args else None
        success, status = test_endpoint(endpoint, method, data)
        results.append((endpoint, success, status))
        print(f"{'✓' if success else '✗'} {method} {endpoint}: {status}")
        time.sleep(0.5)
    
    print(f"\nResults: {sum(1 for _, s, _ in results if s)}/{len(results)} passed")

if __name__ == "__main__":
    main()
