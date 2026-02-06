import logging
from typing import List, Dict, Any, Optional
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from utils.scrubber import scrubber
# Assuming a database manager exists in the project
# from services.database_manager import db_manager 

logger = logging.getLogger(__name__)

class MemoryService:
    """
    Service for storing and recalling agent experiences using semantic vectors.
    """
    
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MemoryService, cls).__new__(cls)
            # Lazy load the model to save memory if service is not used
            cls._model = None 
        return cls._instance

    @property
    def model(self):
        if self._model is None:
            logger.info("Initializing SentenceTransformer model: nomic-ai/nomic-embed-text-v1.5")
            # Using a high-performance embedding model
            self._model = SentenceTransformer('nomic-ai/nomic-embed-text-v1.5', trust_remote_code=True)
        return self._model

    async def store_experience(self, 
                               dept_id: int, 
                               content: str, 
                               mission_id: Optional[str] = None, 
                               metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Redacts, vectorizes, and stores an agent experience.
        """
        try:
            from utils.database_manager import get_database_manager
            db = get_database_manager()
            
            # 1. Redact sensitive info
            safe_content = scrubber.scrub_experience(content)
            
            # 2. Generate embedding
            embedding = self.model.encode(f"search_document: {safe_content}").tolist()
            
            # 3. Store in Postgres (using pgvector)
            with db.pg_cursor() as cur:
                cur.execute("""
                    INSERT INTO agent_memories (dept_id, mission_id, content, embedding, metadata)
                    VALUES (%s, %s, %s, %s, %s)
                """, (dept_id, mission_id, safe_content, embedding, json.dumps(metadata or {})))
            
            logger.info(f"Stored experience for Dept {dept_id} (Mission: {mission_id})")
            return "SUCCESS"
        except Exception:
            logger.exception("Failed to store agent experience")
            return "FAILURE"

    async def recall_memories(self, 
                              query: str, 
                              limit: int = 5, 
                              min_similarity: float = 0.7) -> List[Dict[str, Any]]:
        """
        Retrieves relevant memories based on semantic similarity.
        """
        try:
            from utils.database_manager import get_database_manager
            db = get_database_manager()
            
            # 1. Vectorize query (with prefix for nomic v1.5)
            query_vector = self.model.encode(f"search_query: {query}").tolist()
            
            # 2. Query Postgres with similarity search (HNSW index)
            with db.pg_cursor() as cur:
                cur.execute("""
                    SELECT content, mission_id, metadata, 1 - (embedding <=> %s::vector) AS similarity 
                    FROM agent_memories 
                    WHERE 1 - (embedding <=> %s::vector) > %s 
                    ORDER BY similarity DESC 
                    LIMIT %s
                """, (query_vector, query_vector, min_similarity, limit))
                
                rows = cur.fetchall()
                memories = [
                    {"content": r[0], "mission_id": r[1], "metadata": r[2], "similarity": float(r[3])} 
                    for r in rows
                ]
                return memories
        except Exception:
            logger.exception("Failed to recall memories")
            return []

memory_service = MemoryService()
