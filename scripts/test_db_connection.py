import os
import psycopg2
from dotenv import load_dotenv

def test_conn():
    load_dotenv()
    pg_url = os.getenv("DATABASE_URL")
    print(f"DEBUG: Using URL: {pg_url}")
    
    try:
        conn = psycopg2.connect(pg_url)
        print("✅ SUCCESS: Connected to PostgreSQL!")
        cur = conn.cursor()
        cur.execute("SELECT version();")
        print(f"Version: {cur.fetchone()}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ FAILURE: {e}")

if __name__ == "__main__":
    test_conn()
