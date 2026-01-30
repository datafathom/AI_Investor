import os
import psycopg2
from dotenv import load_dotenv

def make_password_nullable():
    load_dotenv()
    pg_url = os.getenv("DATABASE_URL")
    
    conn = psycopg2.connect(pg_url)
    conn.autocommit = True
    cur = conn.cursor()
    
    print("🔧 Making password_hash nullable...")
    try:
        cur.execute("ALTER TABLE users ALTER COLUMN password_hash DROP NOT NULL;")
        print("✅ Limit relaxed: password_hash is now nullable.")
    except Exception as e:
        print(f"❌ Error: {e}")
            
    conn.close()

if __name__ == "__main__":
    make_password_nullable()
