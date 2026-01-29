"""Extract API categories from Postman collection for GUI audit."""
import json

with open('docs/api/ai_investor_postman_collection.json', 'r') as f:
    data = json.load(f)

print("=" * 60)
print("API ENDPOINT CATEGORIES FROM POSTMAN COLLECTION")
print("=" * 60)

total_endpoints = 0
categories = []

for item in data.get('item', []):
    name = item.get('name', 'Unknown')
    endpoints = item.get('item', [])
    count = len(endpoints)
    total_endpoints += count
    categories.append((name, count))
    print(f"{name:40} {count:3} endpoints")

print("=" * 60)
print(f"TOTAL: {len(categories)} categories, {total_endpoints} endpoints")
print("=" * 60)
