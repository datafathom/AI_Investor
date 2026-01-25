"""
==============================================================================
FILE: web/api/youtube_api.py
ROLE: YouTube API REST Endpoints
PURPOSE: RESTful endpoints for YouTube video search and transcript analysis.

INTEGRATION POINTS:
    - YouTubeClient: Video search and transcript retrieval
    - YouTubeTranscriptAnalyzer: Transcript analysis

ENDPOINTS:
    GET /api/v1/youtube/search - Search videos
    GET /api/v1/youtube/transcript/{video_id} - Get transcript
    GET /api/v1/youtube/analyze/{video_id} - Analyze video

AUTHOR: AI Investor Team
CREATED: 2026-01-21
==============================================================================
"""

from flask import Blueprint, request, jsonify
import logging
import asyncio

logger = logging.getLogger(__name__)

youtube_bp = Blueprint('youtube', __name__, url_prefix='/api/v1/youtube')


def _run_async(coro):
    """Helper to run async functions in sync context."""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(coro)


@youtube_bp.route('/search', methods=['GET'])
def search_videos():
    """Search for videos."""
    try:
        query = request.args.get('query', '')
        limit = int(request.args.get('limit', 5))
        
        if not query:
            return jsonify({"error": "Missing query parameter"}), 400
        
        from services.social.youtube_client import get_youtube_client
        client = get_youtube_client()
        
        videos = _run_async(client.search_videos(query, limit=limit))
        
        return jsonify({
            "query": query,
            "videos": videos,
            "count": len(videos)
        })
    except Exception as e:
        logger.error(f"Failed to search videos: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@youtube_bp.route('/transcript/<video_id>', methods=['GET'])
def get_transcript(video_id: str):
    """Get video transcript."""
    try:
        from services.social.youtube_client import get_youtube_client
        client = get_youtube_client()
        
        transcript = _run_async(client.get_video_transcript(video_id))
        
        return jsonify({
            "video_id": video_id,
            "transcript": transcript
        })
    except Exception as e:
        logger.error(f"Failed to get transcript: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@youtube_bp.route('/analyze/<video_id>', methods=['GET'])
def analyze_video(video_id: str):
    """Analyze video transcript."""
    try:
        from services.analysis.youtube_transcript_analyzer import get_youtube_analyzer
        analyzer = get_youtube_analyzer()
        
        analysis = _run_async(analyzer.analyze_video(video_id))
        
        return jsonify(analysis)
    except Exception as e:
        logger.error(f"Failed to analyze video: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
