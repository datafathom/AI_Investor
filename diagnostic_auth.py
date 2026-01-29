
import os
import sys
from pathlib import Path

# Add project root to sys.path
_project_root = Path(__file__).resolve().parent
sys.path.insert(0, str(_project_root))

# Load .env manually if dotenv not installed
try:
    from dotenv import load_dotenv
    load_dotenv()
    print(".env loaded via python-dotenv")
except ImportError:
    print("python-dotenv not installed, parsing .env manually")
    if os.path.exists(".env"):
        with open(".env") as f:
            for line in f:
                if "=" in line and not line.startswith("#"):
                    key, value = line.strip().split("=", 1)
                    os.environ[key] = value

from utils.database_manager import get_database_manager
from services.system.social_auth_service import get_social_auth_service

def check_users():
    db = get_database_manager()
    print("\nChecking users table...")
    try:
        with db.pg_cursor() as cur:
            cur.execute("SELECT id, email, username, password_hash, role FROM users;")
            users = cur.fetchall()
            if not users:
                print("No users found.")
            for u in users:
                print(f"ID: {u[0]}, Email: {u[1]}, Username: {u[2]}, Hash: {u[3]}, Role: {u[4]}")
    except Exception as e:
        print(f"Error checking users: {e}")

def check_linked_accounts():
    db = get_database_manager()
    print("\nChecking linked_accounts table...")
    try:
        with db.pg_cursor() as cur:
            cur.execute("SELECT id, user_id, provider, vendor_id FROM linked_accounts;")
            accounts = cur.fetchall()
            if not accounts:
                print("No linked accounts found.")
            for a in accounts:
                print(f"ID: {a[0]}, UserID: {a[1]}, Provider: {a[2]}, VendorID: {a[3]}")
    except Exception as e:
        print(f"Error checking linked accounts: {e}")

def test_google_init():
    from services.auth.google_auth import get_google_auth_service
    print("\nTesting Google Auth initiation...")
    try:
        service = get_google_auth_service(mock=True)
        url = service.get_authorization_url(state="test_state")
        print(f"Auth URL: {url}")
    except Exception as e:
        print(f"Error initiating Google Auth: {e}")

if __name__ == "__main__":
    print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")
    check_users()
    check_linked_accounts()
    test_google_init()
