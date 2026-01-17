
import logging
import datetime
from typing import List, Dict, Any
from utils.database_manager import db_manager

logger = logging.getLogger(__name__)

class InheritanceService:
    """
    Phase 41: The "Dead Man's Switch".
    Monitors tenant activity and triggers inheritance protocols.
    """
    
    def __init__(self):
        self.inactivity_threshold_days = 30
        
    def record_heartbeat(self, tenant_id: str):
        """Record last seen timestamp for a tenant."""
        conn = db_manager.get_pg_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO tenant_monitoring (tenant_id, last_heartbeat) "
                    "VALUES (%s, %s) "
                    "ON CONFLICT (tenant_id) DO UPDATE SET last_heartbeat = %s;",
                    (tenant_id, datetime.datetime.now(), datetime.datetime.now())
                )
                conn.commit()
            logger.info(f"Heartbeat recorded for tenant: {tenant_id}")
        except Exception as e:
            logger.error(f"Failed to record heartbeat: {e}")
        finally:
            db_manager.release_pg_connection(conn)

    def check_switches(self):
        """Check all active switches and trigger if expired."""
        conn = db_manager.get_pg_connection()
        try:
            with conn.cursor() as cur:
                # Find tenants who haven't checked in
                cur.execute(
                    "SELECT tenant_id FROM tenant_monitoring "
                    "WHERE last_heartbeat < NOW() - INTERVAL '%s days';",
                    (self.inactivity_threshold_days,)
                )
                expired_tenants = cur.fetchall()
                
                for (tenant_id,) in expired_tenants:
                    self._trigger_inheritance(tenant_id)
        except Exception as e:
            logger.error(f"Failed to check switches: {e}")
        finally:
            db_manager.release_pg_connection(conn)

    def _trigger_inheritance(self, tenant_id: str):
        """Execute asset transfer logic for a tenant."""
        logger.warning(f"!!! TRIGGERING INHERITANCE PROTOCOL FOR TENANT: {tenant_id} !!!")
        # In a real scenario, this would involve API calls to brokers to move funds
        # or sending encrypted keys to heirs.
        
    def set_inheritance_config(self, tenant_id: str, heir_wallets: List[str]):
        """Configure who receives funds on trigger."""
        conn = db_manager.get_pg_connection()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO inheritance_config (tenant_id, heir_wallets) "
                    "VALUES (%s, %s) "
                    "ON CONFLICT (tenant_id) DO UPDATE SET heir_wallets = %s;",
                    (tenant_id, heir_wallets, heir_wallets)
                )
                conn.commit()
            logger.info(f"Inheritance configured for tenant: {tenant_id}")
        except Exception as e:
            logger.error(f"Failed to config inheritance: {e}")
        finally:
            db_manager.release_pg_connection(conn)

inheritance_service = InheritanceService()
