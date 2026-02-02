
import os
import sys
import time
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from services.neo4j.neo4j_service import neo4j_service

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
        # Check if users table exists by trying to access it
        try:
            cur.execute("SELECT 1 FROM users LIMIT 1;")
        except psycopg2.errors.UndefinedTable:
            conn.rollback() # Reset transaction state
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
                    INSERT INTO users (username, password_hash, created_at, role, is_verified)
                    VALUES ('admin', 'mock_hash_yenoMekam', NOW(), 'admin', TRUE);
                """)
                print("   OK Admin user created.")
            except Exception as e:
                print(f"   ERROR Failed to insert admin user: {e}")
        else:
            print("   Admin user exists. Updating password to ensure consistency...")
            try:
                cur.execute("""
                    UPDATE users SET password_hash = 'mock_hash_yenoMekam' WHERE username = 'admin';
                """)
            except Exception as e:
                print(f"   WARN Failed to update admin password: {e}")

        conn.close()
        print("OK Postgres seeding complete.")
        
        # 2. Neo4j Seeding
        print("🌱 Seeding Neo4j...")
        try:
            # Create default advisor node
            query = """
            MERGE (a:ADVISOR {id: 'demo-advisor'})
            SET a.name = 'Demo Advisor', a.role = 'advisor', a.is_active = TRUE
            """
            neo4j_service.execute_query(query)
            print("   OK Neo4j 'demo-advisor' node created/verified.")
        except Exception as e:
            print(f"   ERROR Neo4j seeding failed: {e}")

        print("OK Database seeding complete.")
        
    except Exception as e:
        print(f"ERROR Error seeding database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run_seed_db()
