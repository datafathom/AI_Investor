import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

logger = logging.getLogger(__name__)

# Default to a local Postgres instance (Dockerized)
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://investor_user:investor_password@localhost:5432/investor_db"
)

try:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_size=10, max_overflow=20)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    logger.info("Database configuration initialized.")
except Exception as e:
    logger.error(f"Failed to initialize database engine: {e}")
    engine = None
    SessionLocal = None
    Base = declarative_base() # Fallback

def get_db():
    """Dependency for getting DB session."""
    if SessionLocal is None:
        raise RuntimeError("Database engine not initialized.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
