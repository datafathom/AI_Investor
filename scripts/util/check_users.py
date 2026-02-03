from services.system.social_auth_service import get_social_auth_service
from utils.database_manager import get_database_manager
from dotenv import load_dotenv
import os

load_dotenv()
service = get_social_auth_service() # This triggers DB init
db = get_database_manager()
with db.pg_cursor() as cur:
    cur.execute("SELECT id, email, username, password_hash FROM users;")
    users = cur.fetchall()
    print("--- USERS IN DATABASE ---")
    for u in users:
        print(f"ID: {u[0]}, Email: {u[1]}, Username: {u[2]}, Hash: {u[3]}")
    print("-------------------------")
