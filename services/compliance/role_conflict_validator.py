import logging
from typing import List, Optional
from uuid import UUID
from schemas.professional_role import ProfessionalRole, RoleAssignment

logger = logging.getLogger(__name__)

class RoleConflictValidator:
    """Validates that role assignments don't create conflicts of interest."""
    
    def validate_assignment(self, current_roles: List[ProfessionalRole], new_role: ProfessionalRole) -> bool:
        """
        Check if the new role is mutually exclusive with any of the current roles.
        """
        for role in current_roles:
            if new_role.role_code in role.exclusive_with:
                logger.error(f"CONFLICT_LOG: Cannot assign {new_role.role_code} because user already has {role.role_code}")
                return False
            
            if role.role_code in new_role.exclusive_with:
                logger.error(f"CONFLICT_LOG: Cannot assign {new_role.role_code} - mutually exclusive with {role.role_code}")
                return False
                
        return True

    def check_fiduciary_clash(self, roles: List[ProfessionalRole]) -> bool:
        """Flags when fiduciary and non-fiduciary roles are mixed without disclosure."""
        has_fiduciary = any(r.fiduciary_standard for r in roles)
        has_non_fiduciary = any(not r.fiduciary_standard for r in roles)
        
        if has_fiduciary and has_non_fiduciary:
            logger.warning("CONFLICT_LOG: Mixing fiduciary and non-fiduciary roles. Disclosure REQUIRED.")
            return True
        return False
