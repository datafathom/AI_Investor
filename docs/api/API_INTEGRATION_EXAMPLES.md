# API Integration Examples

Examples for integrating with the AI Investor API.

## Authentication

### Get Access Token

```python
import requests

# Login
response = requests.post('https://api.ai-investor.com/api/v1/auth/login', json={
    'email': 'user@example.com',
    'password': 'your-password'
})

token = response.json()['data']['token']
```

### Use Token in Requests

```python
headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

response = requests.get('https://api.ai-investor.com/api/v1/portfolio', headers=headers)
```

---

## Portfolio Management

### Get Portfolio

```python
response = requests.get(
    'https://api.ai-investor.com/api/v1/portfolio',
    headers=headers
)

portfolio = response.json()['data']
```

### Get Portfolio Analytics

```python
response = requests.get(
    'https://api.ai-investor.com/api/v1/analytics/portfolio',
    headers=headers,
    params={'start_date': '2024-01-01', 'end_date': '2024-12-31'}
)

analytics = response.json()['data']
```

---

## Trading

### Place Order

```python
order_data = {
    'symbol': 'AAPL',
    'quantity': 10,
    'order_type': 'market',
    'side': 'buy'
}

response = requests.post(
    'https://api.ai-investor.com/api/v1/trading/orders',
    headers=headers,
    json=order_data
)

order = response.json()['data']
```

### Get Order Status

```python
order_id = 'order_123'
response = requests.get(
    f'https://api.ai-investor.com/api/v1/trading/orders/{order_id}',
    headers=headers
)

order_status = response.json()['data']
```

---

## Market Data

### Search Symbols

```python
response = requests.get(
    'https://api.ai-investor.com/api/v1/market/search',
    headers=headers,
    params={'q': 'AAPL'}
)

results = response.json()['data']
```

### Get Quote

```python
response = requests.get(
    'https://api.ai-investor.com/api/v1/market/quote/AAPL',
    headers=headers
)

quote = response.json()['data']
```

---

## Error Handling

### Example with Error Handling

```python
import requests
from requests.exceptions import RequestException

try:
    response = requests.get(
        'https://api.ai-investor.com/api/v1/portfolio',
        headers=headers,
        timeout=10
    )
    
    response.raise_for_status()
    data = response.json()
    
    if data.get('success'):
        portfolio = data['data']
    else:
        print(f"Error: {data.get('error')}")
        
except RequestException as e:
    print(f"Request failed: {e}")
except ValueError as e:
    print(f"Invalid response: {e}")
```

---

## Rate Limiting

### Handle Rate Limits

```python
import time

response = requests.get(url, headers=headers)

if response.status_code == 429:
    retry_after = int(response.headers.get('Retry-After', 60))
    print(f"Rate limited. Retry after {retry_after} seconds")
    time.sleep(retry_after)
    response = requests.get(url, headers=headers)
```

---

## WebSocket Example

### Real-Time Updates

```javascript
const ws = new WebSocket('wss://api.ai-investor.com/ws?token=YOUR_TOKEN');

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Update:', data);
};

ws.onopen = () => {
    console.log('Connected');
};

ws.onerror = (error) => {
    console.error('WebSocket error:', error);
};
```

---

## SDK Examples

### Python SDK (Future)

```python
from ai_investor import AIInvestorClient

client = AIInvestorClient(api_key='your-api-key')

# Get portfolio
portfolio = client.portfolio.get()

# Place order
order = client.trading.place_order(
    symbol='AAPL',
    quantity=10,
    order_type='market'
)
```

---

## Best Practices

1. **Use HTTPS**: Always use HTTPS in production
2. **Handle Errors**: Implement proper error handling
3. **Rate Limiting**: Respect rate limits
4. **Token Security**: Store tokens securely
5. **Timeout**: Set appropriate timeouts
6. **Retry Logic**: Implement retry for transient errors

---

**Last Updated**: 2026-01-21  
**Version**: 1.0
