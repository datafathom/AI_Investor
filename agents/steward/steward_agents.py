from typing import Dict
from agents.base_agent import BaseAgent
from agents.steward.property_manager_agent import PropertyManagerAgent
from agents.steward.vehicle_fleet_ledger_agent import VehicleFleetLedgerAgent
from agents.steward.inventory_agent_agent import InventoryAgentAgent
from agents.steward.procurement_bot_agent import ProcurementBotAgent
from agents.steward.wellness_sync_agent import WellnessSyncAgent
from agents.steward.maintenance_scheduler_agent import MaintenanceSchedulerAgent

def get_steward_agents() -> Dict[str, BaseAgent]:
    """
    Factory function to instantiate all Steward department agents.
    """
    return {
        "steward.property_manager": PropertyManagerAgent(),
        "steward.vehicle_fleet_ledger": VehicleFleetLedgerAgent(),
        "steward.inventory_agent": InventoryAgentAgent(),
        "steward.procurement_bot": ProcurementBotAgent(),
        "steward.wellness_sync": WellnessSyncAgent(),
        "steward.maintenance_scheduler": MaintenanceSchedulerAgent(),
    }
