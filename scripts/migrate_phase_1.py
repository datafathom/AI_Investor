import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def run_migration():
    db_url = os.getenv("DATABASE_URL")
    sql_file = r"c:\Users\astir\Desktop\AI_Company\AI_Investor\schemas\postgres\003_vector_memory.sql"
    
    print(f"🚀 Running migration: {sql_file}")
    try:
        conn = psycopg2.connect(db_url)
        conn.autocommit = True
        with conn.cursor() as cur:
            with open(sql_file, 'r') as f:
                sql = f.read()
                cur.execute(sql)
        conn.close()
        print("✅ Migration successful.")
    except Exception as e:
        print(f"❌ Migration failed: {e}")

if __name__ == "__main__":
    run_migration()
