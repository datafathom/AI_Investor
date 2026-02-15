from typing import Dict
from agents.base_agent import BaseAgent
from agents.envoy.advisor_liaison_agent import AdvisorLiaisonAgent
from agents.envoy.subscription_negotiator_agent import SubscriptionNegotiatorAgent
from agents.envoy.family_office_coordinator_agent import FamilyOfficeCoordinatorAgent
from agents.envoy.philanthropy_scout_agent import PhilanthropyScoutAgent
from agents.envoy.professional_crm_agent import ProfessionalCrmAgent
from agents.envoy.pitch_deck_generator_agent import PitchDeckGeneratorAgent

def get_envoy_agents() -> Dict[str, BaseAgent]:
    """
    Factory function to instantiate all Envoy department agents.
    """
    return {
        "envoy.advisor_liaison": AdvisorLiaisonAgent(),
        "envoy.subscription_negotiator": SubscriptionNegotiatorAgent(),
        "envoy.family_office_coordinator": FamilyOfficeCoordinatorAgent(),
        "envoy.philanthropy_scout": PhilanthropyScoutAgent(),
        "envoy.professional_crm": ProfessionalCrmAgent(),
        "envoy.pitch_deck_generator": PitchDeckGeneratorAgent(),
    }
