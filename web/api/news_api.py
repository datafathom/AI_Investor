from fastapi import APIRouter, HTTPException, Query, WebSocket, WebSocketDisconnect
from typing import List, Optional, Dict
from pydantic import BaseModel
import asyncio
import json
import logging

from services.news.aggregator import NewsAggregator
from services.news.rumor_classifier import RumorClassifier

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/news", tags=["News"])

# --- Models ---
class ArticleResponse(BaseModel):
    id: str
    title: str
    source: str
    published_at: str
    sentiment_label: str

class SavedSearchRequest(BaseModel):
    name: str
    filters: Dict

# --- News Aggregator Endpoints ---

@router.get("/articles")
async def get_articles(
    limit: int = 20, 
    cursor: Optional[str] = None,
    source: Optional[str] = None,
    ticker: Optional[str] = None,
    tag: Optional[str] = None
):
    service = NewsAggregator()
    return await service.get_articles(limit, cursor, source, ticker, tag)

@router.get("/articles/{id}")
async def get_article_details(id: str):
    service = NewsAggregator()
    article = await service.get_article_details(id)
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.get("/sources")
async def list_sources():
    service = NewsAggregator()
    return await service.get_sources()

@router.post("/saved-searches")
async def create_saved_search(req: SavedSearchRequest):
    service = NewsAggregator()
    return await service.create_saved_search(req.name, req.filters)

@router.get("/saved-searches")
async def list_saved_searches():
    service = NewsAggregator()
    return await service.list_saved_searches()

# --- Rumor Mill Endpoints ---

@router.get("/rumors")
async def list_rumors():
    service = RumorClassifier()
    return await service.list_rumors()

@router.get("/rumors/{id}")
async def get_rumor(id: str):
    service = RumorClassifier()
    r = await service.get_rumor(id)
    if not r:
        raise HTTPException(status_code=404, detail="Rumor not found")
    return r

@router.post("/rumors/{id}/vote")
async def vote_rumor(id: str, vote_type: str = Query(..., regex="^(up|down)$")):
    service = RumorClassifier()
    r = await service.vote(id, vote_type)
    if not r:
        raise HTTPException(status_code=404, detail="Rumor not found")
    return r

# --- WebSockets ---

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                pass

manager = ConnectionManager()

@router.websocket("/stream")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive, consume messages if any
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)

# Mock background task to simulate real-time news
async def mock_news_stream():
    service = NewsAggregator()
    while True:
        await asyncio.sleep(5) # Emit every 5 seconds
        if manager.active_connections:
            # Pick a random article and re-emit it as "new"
            if service.cached_articles:
                article = service.cached_articles[0] 
                # Shallow copy and update timestamp
                new_article = article.copy()
                new_article['published_at'] = datetime.now().isoformat()
                new_article['title'] = f"[LIVE] {article['title']}"
                await manager.broadcast({"type": "news", "data": new_article})

# Note: In a real app, `mock_news_stream` would be started by the app lifecycle
