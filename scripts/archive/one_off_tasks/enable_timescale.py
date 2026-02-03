import os
import psycopg2
from dotenv import load_dotenv

def enable_timescale():
    load_dotenv()
    pg_url = os.getenv("DATABASE_URL")
    print(f"DEBUG: Using URL: {pg_url}")
    
    try:
        conn = psycopg2.connect(pg_url)
        conn.autocommit = True
        cur = conn.cursor()
        print("🔧 Enabling TimescaleDB extension...")
        cur.execute("CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE;")
        print("✅ SUCCESS: TimescaleDB extension enabled!")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ FAILURE: {e}")

if __name__ == "__main__":
    enable_timescale()
