import os
import psycopg2
from dotenv import load_dotenv

def clean_migrations():
    load_dotenv()
    pg_url = os.getenv("DATABASE_URL")
    
    conn = psycopg2.connect(pg_url)
    conn.autocommit = True
    cur = conn.cursor()
    
    print("🧹 Cleaning rollback entries from schema_migrations...")
    
    # 1. Delete rollback entries
    cur.execute("DELETE FROM schema_migrations WHERE version LIKE '%rollback%';")
    print(f"   Deleted {cur.rowcount} rollback entries.")
    
    # 2. Delete entries for migrations that need re-running (because they were rolled back)
    # We suspect phase1_001 was rolled back.
    # And maybe phase2_002, phase6_005 if they had rollbacks.
    
    re_run_list = [
        'phase1_001_user_workspaces',
        'phase2_002_fear_greed',
        'phase2_003_hypemeter',
        'phase6_004_legal_documents',
        'phase6_005_user_onboarding'
    ]
    
    for version in re_run_list:
        cur.execute("DELETE FROM schema_migrations WHERE version = %s;", (version,))
        if cur.rowcount > 0:
            print(f"   Deleted {version} to force re-run.")
            
    conn.close()
    print("✅ Clean complete.")

if __name__ == "__main__":
    clean_migrations()
