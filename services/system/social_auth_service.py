import logging
import uuid
import json
import threading
from datetime import datetime
from typing import Dict, Any, Optional, List
from web.auth_utils import generate_token
from utils.database_manager import get_database_manager

class SocialAuthService:
    """
    Handles authentication and account creation via external financial vendors.
    Maps vendor-specific identifiers (sub/ID) to internal AI Investor accounts.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SocialAuthService, cls).__new__(cls)
            cls._instance._init_service()
        return cls._instance

    def _init_service(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.db = get_database_manager()
        self._db_initialized = False
        self._lock = threading.Lock() # Use a simple lock for initialization

    def _init_db(self, cur=None) -> None:
        """Ensures auth tables exist in Postgres and schema is up-to-date."""
        if cur is None:
            # If no cursor provided, wrap in a temporary context
            try:
                with self.db.pg_cursor() as new_cur:
                    self._init_db(cur=new_cur)
                return
            except Exception as e:
                self.logger.error("Failed to open connection for DB init: %s", e)
                return

        try:
            # 1. Users Table (Ensure it has modern columns)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # Check and add missing columns for Phase alignment
            self._ensure_column(cur, "users", "email", "VARCHAR(255) UNIQUE")
            self._ensure_column(cur, "users", "role", "VARCHAR(50) DEFAULT 'trader'")
            self._ensure_column(cur, "users", "is_verified", "BOOLEAN DEFAULT FALSE")
            self._ensure_column(cur, "users", "password_hash", "TEXT")
            self._ensure_column(cur, "users", "organization_id", "INTEGER")

            # Handle Legacy 'password' column (Drop NOT NULL if it exists)
            # Handle 'password_hash' column nullability
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.columns 
                    WHERE table_name = 'users' AND column_name = 'password_hash'
                    AND is_nullable = 'NO'
                );
            """)
            if cur.fetchone()[0]:
                self.logger.info("Migrating schema: making 'password_hash' column nullable")
                cur.execute("ALTER TABLE users ALTER COLUMN password_hash DROP NOT NULL;")

            # 2. Linked Accounts Table
            cur.execute("""
                CREATE TABLE IF NOT EXISTS linked_accounts (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    provider VARCHAR(50) NOT NULL,
                    vendor_id TEXT NOT NULL,
                    metadata JSONB DEFAULT '{}',
                    UNIQUE(provider, vendor_id)
                );
            """)
            
            # 3. Ensure Admin exists with modern schema
            cur.execute("SELECT id FROM users WHERE username = 'admin';")
            admin = cur.fetchone()
            if not admin:
                 cur.execute("""
                    INSERT INTO users (email, username, role, is_verified, password_hash)
                    VALUES (%s, %s, %s, %s, %s);
                """, ('admin@example.com', 'admin', 'admin', True, 'mock_hash_nimda'))
                
            self.logger.info("SocialAuthService database schema synchronized.")
        except Exception as e:
            self.logger.error("Failed to initialize SocialAuthService DB: %s", e)
            raise 

    def _ensure_column(self, cur, table: str, column: str, type_def: str) -> None:
        """Ensures a specific column exists in a table."""
        cur.execute(f"""
            SELECT EXISTS (
                SELECT FROM information_schema.columns 
                WHERE table_name = '{table}' AND column_name = '{column}'
            );
        """)
        if not cur.fetchone()[0]:
            self.logger.info("Migrating schema: Adding column %s to %s", column, table)
            cur.execute(f"ALTER TABLE {table} ADD COLUMN {column} {type_def};")

    def _ensure_initialized(self):
        """Lazy initialization of the database schema."""
        if self._db_initialized:
            return
        
        with self._lock:
            if not self._db_initialized:
                self.logger.info("SocialAuthService: First-run lazy initialization...")
                self._init_db()
                self._db_initialized = True

    def _get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Helper to fetch user data from DB (case-insensitive)."""
        self._ensure_initialized()
        if not email:
            return None
        email = email.strip().lower()
        try:
            with self.db.pg_cursor() as cur:
                cur.execute("""
                    SELECT id, email, username, role, is_verified, password_hash, organization_id 
                    FROM users WHERE LOWER(email) = %s;
                """, (email,))
                user = cur.fetchone()
                if user:
                    return {
                        "id": user[0], "email": user[1], "username": user[2],
                        "role": user[3], "is_verified": user[4], "password_hash": user[5],
                        "organization_id": user[6]
                    }
        except Exception as e:
            self.logger.error("Error fetching user %s: %s", email, e)
        return None

    def initiate_auth_flow(self, provider: str) -> str:
        """Generates the OAuth start URL for a given provider."""
        # In a real app, this would use the provider's SDK or build a URL
        return f"https://{provider}.com/oauth/authorize?client_id=mock_id&redirect_uri=callback"

    def handle_callback(self, provider: str, code: str) -> Dict[str, Any]:
        """
        Processes the OAuth callback, exchanges code for user info, 
        and performs login or account merging.
        """
        self._ensure_initialized()
        self.logger.info("Handling %s callback with code: %s", provider, code)
        
        # 1. Simulate fetching user profile from provider
        mock_id = code.split('_')[-1] if '_' in code else code
        vendor_id = f"{provider}_mock_{mock_id}"
        
        if 'merge' in code.lower():
            vendor_email = "admin@example.com"
        elif code.startswith('email:'):
            vendor_email = code.split(':')[1]
        else:
            vendor_email = f"user_{mock_id}@example.com"
        
        vendor_email = vendor_email.strip().lower()
        
        # Metadata from vendor (Simulated)
        vendor_metadata = {
            "vendor_id": vendor_id,
            "login_at": datetime.now().isoformat(),
            "name_hint": vendor_email.split('@')[0]
        }
        
        # 2. Find or Create User based on EMAIL
        user_data = self._get_user_by_email(vendor_email)
        is_new_user = False
        
        with self.db.pg_cursor() as cur:
            if user_data:
                self.logger.info("Merging/Logging into existing user: %s", vendor_email)
                # Ensure verified
                cur.execute("UPDATE users SET is_verified = TRUE WHERE id = %s;", (user_data["id"],))
                user_data["is_verified"] = True
            else:
                is_new_user = True
                # Create NEW user with UNIQUE username handling
                base_username = vendor_email.split('@')[0]
                username = base_username
                
                # Check for collision
                cur.execute("SELECT id FROM users WHERE username = %s;", (username,))
                if cur.fetchone():
                    # Collision! Append random suffix
                    username = f"{base_username}_{uuid.uuid4().hex[:4]}"
                    self.logger.info("Username collision for %s, using %s", base_username, username)

                cur.execute("""
                    INSERT INTO users (email, username, role, is_verified)
                    VALUES (%s, %s, %s, %s) RETURNING id;
                """, (vendor_email, username, 'trader', True))
                new_id = cur.fetchone()[0]
                user_data = {
                    "id": new_id, "email": vendor_email, 
                    "username": username, 
                    "role": "trader", "is_verified": True, "password_hash": None
                }
                self.logger.info("Created new account via %s: %s (User: %s)", provider, vendor_email, username)

            # Link provider
            cur.execute("""
                INSERT INTO linked_accounts (user_id, provider, vendor_id, metadata)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (provider, vendor_id) DO UPDATE SET metadata = EXCLUDED.metadata;
            """, (user_data["id"], provider, vendor_id, json.dumps(vendor_metadata)))

        # 4. Generate internal session token
        token = generate_token(user_id=user_data["id"], role=user_data["role"])
        
        return {
            "token": token,
            "user": {
                "id": user_data["id"],
                "username": user_data["username"],
                "email": vendor_email,
                "role": user_data["role"],
                "is_verified": user_data["is_verified"],
                "organization_id": user_data.get("organization_id"),
                "has_password": user_data.get("password_hash") is not None
            },
            "new_user": is_new_user
        }

    def _get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Helper to fetch user data from DB by ID."""
        self._ensure_initialized()
        try:
            with self.db.pg_cursor() as cur:
                cur.execute("""
                    SELECT id, email, username, role, is_verified, password_hash, organization_id 
                    FROM users WHERE id = %s;
                """, (user_id,))
                user = cur.fetchone()
                if user:
                    return {
                        "id": user[0], "email": user[1], "username": user[2],
                        "role": user[3], "is_verified": user[4], "password_hash": user[5],
                        "organization_id": user[6]
                    }
        except Exception as e:
            self.logger.error("Error fetching user %s: %s", user_id, e)
        return None

    def set_password(self, email: str, password: str, user_id: int = None) -> bool:
        """Sets or updates password for a user."""
        self._ensure_initialized()
        if user_id:
             try:
                password_hash = f"mock_hash_{password[::-1]}"
                with self.db.pg_cursor() as cur:
                    cur.execute("UPDATE users SET password_hash = %s WHERE id = %s;", (password_hash, user_id))
                self.logger.info("Password set for user ID: %s", user_id)
                return True
             except Exception as e:
                self.logger.error("Failed to set password for ID %s: %s", user_id, e)
                return False

        user = self._get_user_by_email(email)
        if not user:
            return False
        
        return self.set_password(email, password, user_id=user["id"])

    def verify_email(self, email: str) -> bool:
        """Marks a user as email-verified."""
        self._ensure_initialized()
        try:
            with self.db.pg_cursor() as cur:
                cur.execute("UPDATE users SET is_verified = TRUE WHERE email = %s;", (email,))
            self.logger.info("Email verified for user: %s", email)
            return True
        except Exception as e:
            self.logger.error("Failed to verify email for %s: %s", email, e)
            return False

    def reset_database(self) -> None:
        """Clears all users and linked accounts for a fresh start."""
        self._ensure_initialized()
        try:
            with self.db.pg_cursor() as cur:
                cur.execute("TRUNCATE linked_accounts, users RESTART IDENTITY CASCADE;")
                # Re-add admin using the SAME cursor/transaction
                self._init_db(cur=cur)
            self.logger.info("Postgres auth database has been reset.")
        except Exception as e:
            self.logger.error("Failed to reset auth DB: %s", e)

    def get_linked_finance_vendors(self, email: str) -> List[str]:
        """Returns list of linked finance-capable providers."""
        self._ensure_initialized()
        user = self._get_user_by_email(email)
        if not user:
            return []
        
        finance_vendors = ["paypal", "venmo", "plaid", "stripe", "square"]
        try:
            with self.db.pg_cursor() as cur:
                cur.execute("""
                    SELECT provider FROM linked_accounts 
                    WHERE user_id = %s AND provider = ANY(%s);
                """, (user["id"], finance_vendors))
                results = cur.fetchall()
                return [r[0] for r in results]
        except Exception as e:
            self.logger.error("Error fetching linked vendors for %s: %s", email, e)
            return []

    def transfer_funds(self, email: str, vendor: str, amount: float, direction: str) -> Dict[str, Any]:
        """Simulates fund transfer via linked vendor API."""
        linked = self.get_linked_finance_vendors(email)
        if vendor not in linked:
            return {"success": False, "error": f"Vendor {vendor} not linked to this account"}
            
        self.logger.info("Initiating %s transfer of $%s via %s for %s", direction, amount, vendor, email)
        
        # In mock mode, we always succeed
        return {
            "success": True,
            "transaction_id": f"tx_{uuid.uuid4().hex[:8]}",
            "provider": vendor,
            "amount": amount,
            "direction": direction,
            "status": "completed",
            "timestamp": datetime.now().isoformat()
        }

# Global Accessor
def get_social_auth_service() -> SocialAuthService:
    return SocialAuthService()
