from services.system.social_auth_service import get_social_auth_service
from utils.database_manager import get_database_manager
from dotenv import load_dotenv

load_dotenv()
service = get_social_auth_service()
db = get_database_manager()

password = "admin"
new_hash = f"mock_hash_{password[::-1]}" # mock_hash_nimda

with db.pg_cursor() as cur:
    cur.execute("UPDATE users SET password_hash = %s WHERE username = 'admin';", (new_hash,))
    print(f"Updated admin hash to {new_hash}")
