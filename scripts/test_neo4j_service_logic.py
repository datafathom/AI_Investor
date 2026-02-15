import os
import sys
import logging
import time

# Add project root to path
sys.path.append(os.getcwd())

logging.basicConfig(level=logging.INFO)
from services.neo4j.neo4j_service import get_neo4j

def test_service():
    print("Testing Neo4jService...")
    neo = get_neo4j()
    
    print("Step 1: Fetching Schema (should be fast mock feedback)")
    start = time.time()
    try:
        schema = neo.get_schema()
        end = time.time()
        print(f"Schema fetched in {end - start:.4f}s")
        print(f"Nodes: {schema.get('nodes')}")
    except Exception as e:
        print(f"Error fetching schema: {e}")

    print("\nStep 2: Executing Query (should be fast mock feedback)")
    start = time.time()
    try:
        results = neo.execute_query("MATCH (n) RETURN n LIMIT 5")
        end = time.time()
        print(f"Query executed in {end - start:.4f}s")
        print(f"Results: {len(results)} items")
    except Exception as e:
        print(f"Error executing query: {e}")

if __name__ == "__main__":
    test_service()
