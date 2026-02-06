import os
import sys
import time
import psycopg2
from pathlib import Path
from dotenv import load_dotenv
from services.neo4j.neo4j_service import neo4j_service

def mask_url(url: str) -> str:
    """Masks the password in a database connection URL."""
    try:
        from urllib.parse import urlparse, urlunparse
        parsed = urlparse(url)
        if parsed.password:
            # Replace the password with stars
            netloc = f"{parsed.username}:{'*' * 8}@{parsed.hostname}"
            if parsed.port:
                netloc += f":{parsed.port}"
            parsed = parsed._replace(netloc=netloc)
        return urlunparse(parsed)
    except Exception:
        return "DATABASE_URL_UNPARSABLE"

def run_seed_db():
    """
    Seeds the database with initial required data (Admin User, etc).
    """
    # Load .env from project root
    project_root = Path(__file__).resolve().parent.parent.parent
    env_path = project_root / '.env'
    load_dotenv(dotenv_path=env_path)
    
    # Use the DATABASE_URL exactly as specified in .env
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        database_url = "postgresql://investor_user:investor_password@127.0.0.1:5432/investor_db"
    
    print(f"🌱 Seeding Postgres database (Target: {mask_url(database_url)})")
    
    try:
        # Connect with a longer timeout to allow for container warm-up
        conn = psycopg2.connect(database_url, connect_timeout=30)
        conn.autocommit = True
        cur = conn.cursor()
        
        # 1. Create Admin User
        try:
            cur.execute("SELECT 1 FROM users LIMIT 1;")
        except psycopg2.errors.UndefinedTable:
            conn.rollback() 
            print("WARN 'users' table not found. Has the backend migration run?")
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
