"""
SQLAlchemy database setup and utility functions.
"""
import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Session
from contextlib import contextmanager

logger = logging.getLogger(__name__)

# Base class for SQLAlchemy models
Base = declarative_base()

class SQLAlchemyManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SQLAlchemyManager, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if getattr(self, 'initialized', False):
            return
        
        self.database_url = os.getenv("DATABASE_URL")
        if not self.database_url:
            # Fallback for local dev if not in env
            self.database_url = "postgresql://neo4j:investor_password@localhost:5432/investor_db"
            
        self.engine = create_engine(self.database_url, pool_pre_ping=True)
        self._session_factory = sessionmaker(bind=self.engine)
        self.initialized = True
        logger.info("SQLAlchemy engine and session factory initialized.")

    @contextmanager
    def session_scope(self) -> Session:
        """Provide a transactional scope around a series of operations."""
        session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

# Global Instance
sqlalchemy_manager = SQLAlchemyManager()

def get_sqlalchemy_session():
    """Utility to get a session."""
    return sqlalchemy_manager._session_factory()
