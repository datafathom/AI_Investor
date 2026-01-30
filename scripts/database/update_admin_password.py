import os
import psycopg2
from dotenv import load_dotenv

def update_admin_password():
    load_dotenv()
    pg_url = os.getenv("DATABASE_URL")
    
    # Calculate mock hash for 'makeMoney'
    # Logic from web/api/auth_api.py: f"mock_hash_{password[::-1]}"
    password = "makeMoney"
    mock_hash = f"mock_hash_{password[::-1]}"
    
    print(f"🔧 Updating admin password to '{password}' (Hash: {mock_hash})...")
    
    try:
        conn = psycopg2.connect(pg_url)
        conn.autocommit = True
        cur = conn.cursor()
        
        # Update user where username is 'admin' OR email is 'admin' or 'admin@example.com'
        cur.execute("""
            UPDATE users 
            SET password_hash = %s 
            WHERE username = 'admin' OR email = 'admin' OR email = 'admin@example.com';
        """, (mock_hash,))
        
        rows_affected = cur.rowcount
        print(f"✅ Success: Updated {rows_affected} user record(s).")
        
        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    update_admin_password()
