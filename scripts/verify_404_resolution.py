import requests
import json

endpoints = [
    "http://127.0.0.1:5050/api/v1/brokerage/status",
    "http://127.0.0.1:5050/api/v1/brokerage/providers",
    "http://127.0.0.1:5050/api/v1/brokerage/positions",
    "http://127.0.0.1:5050/api/v1/homeostasis/status",
    "http://127.0.0.1:5050/api/v1/system/kafka/stats",
    "http://127.0.0.1:5050/api/v1/market/fear-greed",
    "http://127.0.0.1:5050/api/v1/politics/disclosures",
    "http://127.0.0.1:5050/api/v1/scanner/matches",
    "http://127.0.0.1:5050/api/v1/settlement/balances",
    "http://127.0.0.1:5050/api/v1/ai/debate/stream",
    "http://127.0.0.1:5050/api/v1/backtest/overfit?is_sharpe=2.45&oos_sharpe=1.12",
    "http://127.0.0.1:5050/health"
]

for url in endpoints:
    try:
        response = requests.get(url, timeout=5)
        print(f"URL: {url}")
        print(f"Status Code: {response.status_code}")
        # print(f"Response: {json.dumps(response.json(), indent=2)}")
    except Exception as e:
        print(f"Error for {url}: {e}")
