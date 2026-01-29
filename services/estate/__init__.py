"""
Estate Planning Services Package

Provides estate planning and inheritance simulation capabilities.
"""

from services.estate.estate_planning_service import EstatePlanningService
from services.estate.inheritance_simulator import InheritanceSimulator
from services.estate.role_manager import RoleManager
from services.estate.ownership_service import OwnershipService
from services.estate.stipulation_service import StipulationService
from services.estate.dynasty_payout import DynastyPayoutEngine
from services.estate.legacy_simulator import LegacySimulator

__all__ = [
    "EstatePlanningService",
    "InheritanceSimulator",
    "RoleManager",
    "OwnershipService",
    "StipulationService",
    "DynastyPayoutEngine",
    "LegacySimulator",
]
