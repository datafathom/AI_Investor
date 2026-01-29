"""
Trade Journal SQLAlchemy Model.
Stores high-fidelity records of every trade and decision.
"""
from sqlalchemy import Column, String, Integer, Numeric, DateTime, Boolean, JSON, BigInteger
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime
import uuid
from utils.db_sqlalchemy import Base

class TradeJournal(Base):
    """
    Trade Journaling record for performance auditing and forensic analysis.
    """
    __tablename__ = 'trade_journal'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    trade_id = Column(UUID(as_uuid=True), nullable=False, unique=True, default=uuid.uuid4)
    
    # Trade Details
    symbol = Column(String(20), nullable=False)
    direction = Column(String(10), nullable=False)  # LONG, SHORT
    entry_price = Column(Numeric(20, 8), nullable=False)
    exit_price = Column(Numeric(20, 8), nullable=True)
    stop_loss = Column(Numeric(20, 8), nullable=False)
    take_profit = Column(Numeric(20, 8), nullable=True)
    position_size = Column(Numeric(20, 8), nullable=False)
    
    # Execution
    entry_time = Column(DateTime(timezone=True), nullable=False)
    exit_time = Column(DateTime(timezone=True), nullable=True)
    status = Column(String(20), nullable=False, default='OPEN')  # OPEN, CLOSED, STOPPED, CANCELLED
    
    # Performance
    pnl_pips = Column(Numeric(10, 2), nullable=True)
    pnl_dollars = Column(Numeric(20, 2), nullable=True)
    r_multiple = Column(Numeric(10, 2), nullable=True)
    
    # Agent Logic
    agent_id = Column(String(100), nullable=False)
    trade_thesis = Column(String, nullable=False)
    trade_reason = Column(JSONB, nullable=False)
    confidence_score = Column(Numeric(5, 4), nullable=True)
    
    # Audit
    is_demo = Column(Boolean, nullable=False, default=True)
    hash_sha256 = Column(String(64), nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<TradeJournal(trade_id={self.trade_id}, symbol={self.symbol}, status={self.status})>"
