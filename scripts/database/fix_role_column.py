import os
import psycopg2
from dotenv import load_dotenv

def fix_column():
    load_dotenv()
    pg_url = os.getenv("DATABASE_URL")
    # Masked URL: ...
    
    conn = psycopg2.connect(pg_url)
    conn.autocommit = True
    cur = conn.cursor()
    
    print("🔧 Renaming 'roles' to 'role' in users table...")
    try:
        cur.execute("ALTER TABLE users RENAME COLUMN roles TO role;")
        print("✅ Column renamed successfully.")
    except psycopg2.errors.UndefinedColumn:
        print("⚠️  Column 'roles' not found (maybe already renamed?).")
    except psycopg2.errors.DuplicateColumn:
         print("⚠️  Column 'role' already exists.")
    except Exception as e:
        print(f"❌ Error: {e}")
            
    conn.close()

if __name__ == "__main__":
    fix_column()
