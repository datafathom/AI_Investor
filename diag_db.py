import os
import psycopg2
from dotenv import load_dotenv
from pathlib import Path

# Force load .env
env_path = Path(__file__).parent / ".env"
print(f"Loading .env from: {env_path}")
load_dotenv(env_path, override=True)

postgres_host = os.getenv("POSTGRES_HOST")
database_url = os.getenv("DATABASE_URL")

print(f"DEBUG: POSTGRES_HOST={postgres_host}")
print(f"DEBUG: DATABASE_URL={database_url}")

try:
    print(f"Connecting to {postgres_host}...")
    conn = psycopg2.connect(
        host=postgres_host,
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        dbname=os.getenv("POSTGRES_DB"),
        connect_timeout=10
    )
    print("Connection via params: SUCCESS")
    conn.close()
except Exception as e:
    print(f"Connection via params: FAILED - {e}")

try:
    print(f"Connecting to {database_url}...")
    conn = psycopg2.connect(database_url, connect_timeout=10)
    print("Connection via URL: SUCCESS")
    conn.close()
except Exception as e:
    print(f"Connection via URL: FAILED - {e}")
