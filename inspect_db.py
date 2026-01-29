import sys
import os
from pathlib import Path

# Add project root to path
project_root = str(Path(__file__).parent.parent.absolute())
sys.path.insert(0, project_root)

from utils.database_manager import get_database_manager

def inspect_user(email):
    db = get_database_manager()
    print(f"Inspecting user: {email}")
    try:
        with db.pg_cursor() as cur:
            cur.execute("SELECT id, email, username, password_hash, is_verified FROM users WHERE LOWER(email) = %s", (email.lower(),))
            user = cur.fetchone()
            if user:
                print(f"ID: {user[0]}")
                print(f"Email: {user[1]}")
                print(f"Username: {user[2]}")
                print(f"Hash: '{user[3]}'")
                print(f"Verified: {user[4]}")
            else:
                print("User not found in database.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        inspect_user(sys.argv[1])
    else:
        print("Usage: python inspect_db.py <email>")
