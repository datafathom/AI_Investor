from typing import Dict
from agents.base_agent import BaseAgent
from agents.front_office.inbox_gatekeeper_agent import InboxGatekeeperAgent
from agents.front_office.calendar_concierge_agent import CalendarConciergeAgent
from agents.front_office.voice_advocate_agent import VoiceAdvocateAgent
from agents.front_office.logistics_researcher_agent import LogisticsResearcherAgent
from agents.front_office.document_courier_agent import DocumentCourierAgent
from agents.front_office.executive_buffer_agent import ExecutiveBufferAgent
from agents.front_office.general_purchasing_agent import GeneralPurchasingAgent
from agents.front_office.travel_concierge_agent import TravelConciergeAgent
from agents.front_office.personal_assistant_agent import PersonalAssistantAgent

def get_front_office_agents() -> Dict[str, BaseAgent]:
    """
    Factory function to instantiate all Front Office department agents.
    """
    return {
        "front_office.inbox_gatekeeper": InboxGatekeeperAgent(),
        "front_office.calendar_concierge": CalendarConciergeAgent(),
        "front_office.voice_advocate": VoiceAdvocateAgent(),
        "front_office.logistics_researcher": LogisticsResearcherAgent(),
        "front_office.document_courier": DocumentCourierAgent(),
        "front_office.executive_buffer": ExecutiveBufferAgent(),
        "front_office.general_purchasing_agent": GeneralPurchasingAgent(),
        "front_office.travel_concierge_agent": TravelConciergeAgent(),
        "front_office.personal_assistant_agent": PersonalAssistantAgent(),
    }
