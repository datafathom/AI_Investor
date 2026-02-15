from typing import Dict
from agents.base_agent import BaseAgent
from agents.media_team.article_synthesizer_agent import ArticleSynthesizerAgent
from agents.media_team.visual_aesthetics_agent import VisualAestheticsAgent
from agents.media_team.video_director_agent import VideoDirectorAgent
from agents.media_team.document_drafter_agent import DocumentDrafterAgent
from agents.media_team.mesh_architect_agent import MeshArchitectAgent
from agents.media_team.presentation_designer_agent import PresentationDesignerAgent

def get_media_team_agents() -> Dict[str, BaseAgent]:
    """
    Factory function to instantiate all Media Team department agents.
    """
    return {
        "media.article_synthesizer": ArticleSynthesizerAgent(),
        "media.visual_aesthetics_agent": VisualAestheticsAgent(),
        "media.video_director": VideoDirectorAgent(),
        "media.document_drafter": DocumentDrafterAgent(),
        "media.mesh_architect": MeshArchitectAgent(),
        "media.presentation_designer": PresentationDesignerAgent(),
    }
