
import os
import sys
import time
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Default to the local dev database URL if not set
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://investor_user:investor_password@localhost:5432/investor_db")

def run_seed_db():
    """
    Seeds the database with initial required data (Admin User, etc).
    """
    print(f"🌱 Seeding database at {DATABASE_URL}...")
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        conn.autocommit = True
        cur = conn.cursor()
        
        # 1. Create Admin User
        # Using a raw query for simplicity and speed without loading full ORM models yet
        # Password handling should ideally be hashed, but for dev seeding we use plain text 
        # or a known hash if the auth system requires it. 
        # Assuming the auth system might hash on login or expects a hash. 
        # For now, inserting a placeholder.
        
        # Check if users table exists first
        cur.execute("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'users');")
        table_exists = cur.fetchone()[0]
        
        if not table_exists:
            print("WARN 'users' table not found. Has the backend migration run?")
            print("   Please ensure the backend has started at least once to create tables.")
            return

        print("👤 Checking for Admin user...")
        cur.execute("SELECT id FROM users WHERE username = 'admin';")
        user = cur.fetchone()
        
        if not user:
            print("   Creating Admin user ('admin')...")
            try:
                cur.execute("""
                    INSERT INTO users (username, password, created_at)
                    VALUES ('admin', 'password123', NOW());
                """)
                print("   OK Admin user created.")
            except Exception as e:
                print(f"   ERROR Failed to insert admin user: {e}")
        else:
            print("   OK Admin user already exists.")

        conn.close()
        print("OK Database seeding complete.")
        
    except Exception as e:
        print(f"ERROR Error seeding database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_seed_db()
