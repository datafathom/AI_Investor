"""
Trade Journal Service.
Orchestrates trade logging, performance calculation, and integrity hashing.
"""
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime
from uuid import UUID
from utils.db_sqlalchemy import sqlalchemy_manager
from models.trade_journal import TradeJournal
from services.r_multiple_calculator import RMultipleCalculator
from services.trade_hash_generator import TradeHashGenerator

logger = logging.getLogger(__name__)

class TradeJournalService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TradeJournalService, cls).__new__(cls)
            cls._instance.initialized = False
        return cls._instance

    def __init__(self):
        if getattr(self, 'initialized', False):
            return
        self.initialized = True

    def open_trade(self, trade_data: Dict[str, Any]) -> TradeJournal:
        """
        Record a new opened trade in the journal.
        """
        with sqlalchemy_manager.session_scope() as session:
            entry = TradeJournal(
                trade_id=trade_data['trade_id'],
                symbol=trade_data['symbol'],
                direction=trade_data['direction'],
                entry_price=trade_data['entry_price'],
                stop_loss=trade_data['stop_loss'],
                take_profit=trade_data.get('take_profit'),
                position_size=trade_data['position_size'],
                entry_time=trade_data.get('entry_time', datetime.utcnow()),
                status='OPEN',
                agent_id=trade_data['agent_id'],
                trade_thesis=trade_data['trade_thesis'],
                trade_reason=trade_data.get('trade_reason', {}),
                confidence_score=trade_data.get('confidence_score'),
                is_demo=trade_data.get('is_demo', True)
            )
            
            # Generate initial audit hash
            entry.hash_sha256 = TradeHashGenerator.generate_hash(trade_data)
            
            session.add(entry)
            logger.info(f"Trade Journaled (OPEN): {entry.trade_id} - {entry.symbol}")
            return entry

    def close_trade(
        self, 
        trade_id: UUID, 
        exit_price: float, 
        exit_time: Optional[datetime] = None
    ) -> Optional[TradeJournal]:
        """
        Close an existing trade, calculate PnL and R-Multiple.
        """
        with sqlalchemy_manager.session_scope() as session:
            entry = session.query(TradeJournal).filter_by(trade_id=trade_id).first()
            if not entry:
                logger.error(f"Trade not found for closing: {trade_id}")
                return None
            
            entry.exit_price = exit_price
            entry.exit_time = exit_time or datetime.utcnow()
            entry.status = 'CLOSED'
            
            # Calculate R-Multiple
            entry.r_multiple = RMultipleCalculator.calculate(
                float(entry.entry_price),
                float(entry.exit_price),
                float(entry.stop_loss),
                entry.direction
            )
            
            # Status could be STOPPED if hit SL (simple logic for now)
            if entry.direction == 'LONG' and entry.exit_price <= entry.stop_loss:
                entry.status = 'STOPPED'
            elif entry.direction == 'SHORT' and entry.exit_price >= entry.stop_loss:
                entry.status = 'STOPPED'
                
            logger.info(f"Trade Journaled (CLOSED): {entry.trade_id} - R: {entry.r_multiple}")
            return entry

    def get_trade(self, trade_id: UUID) -> Optional[TradeJournal]:
        """Retrieve a specific trade record."""
        session = sqlalchemy_manager._session_factory()
        try:
            return session.query(TradeJournal).filter_by(trade_id=trade_id).first()
        finally:
            session.close()

# Global Singleton
trade_journal_service = TradeJournalService()
