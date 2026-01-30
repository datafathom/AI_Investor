import os
import psycopg2
from dotenv import load_dotenv

def fix_user_schema():
    load_dotenv()
    pg_url = os.getenv("DATABASE_URL")
    
    conn = psycopg2.connect(pg_url)
    conn.autocommit = True
    cur = conn.cursor()
    
    print("🔧 Fixing users table schema...")
    
    # 1. Rename password -> password_hash
    try:
        cur.execute("ALTER TABLE users RENAME COLUMN password TO password_hash;")
        print("✅ Renamed password -> password_hash.")
    except Exception as e:
        print(f"⚠️  Rename failed (maybe done?): {e}")
        
    # 2. Add is_verified
    try:
        cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS is_verified BOOLEAN DEFAULT FALSE;")
        print("✅ Added is_verified.")
    except Exception as e:
        print(f"❌ Failed to add is_verified: {e}")

    # 3. Add organization_id
    try:
        cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS organization_id UUID;")
        print("✅ Added organization_id.")
    except Exception as e:
         print(f"❌ Failed to add organization_id: {e}")

    # 4. Set role for admin (if needed)
    try:
        cur.execute("UPDATE users SET role = 'admin', is_verified = TRUE WHERE username = 'admin';")
        print("✅ Updated admin role/verified.")
    except Exception as e:
        print(f"⚠️  Admin update issue: {e}")
            
    conn.close()

if __name__ == "__main__":
    fix_user_schema()
