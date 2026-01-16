"""
==============================================================================
AI Investor - Stacker Agent
==============================================================================
PURPOSE:
    Aggregates signals from multiple sources (Searcher, FFT, HMM) into
    execution-ready trading configurations. Acts as the "decision maker"
    that stacks evidence before committing to a trade.

PATTERN:
    - Receives signals from Searcher Agent (opportunities)
    - Receives regime signals from HMM Engine (Bull/Bear/Sideways)
    - Combines signals with configurable weights
    - Only outputs trade signals when confidence threshold is met
==============================================================================
"""
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
import logging
from neo4j import GraphDatabase

from agents.base_agent import BaseAgent
from utils.core.config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

logger = logging.getLogger(__name__)


@dataclass
class Signal:
    """Represents a single signal from an agent or service."""
    source: str
    signal_type: str
    direction: str  # 'LONG', 'SHORT', 'NEUTRAL'
    confidence: float  # 0.0 to 1.0
    data: Dict[str, Any] = field(default_factory=dict)


class StackerAgent(BaseAgent):
    """
    The Stacker Agent - Decision Aggregator.
    
    Collects and weighs signals from multiple sources to produce
    high-confidence trade recommendations.
    """
    
    # Signal source weights (configurable)
    DEFAULT_WEIGHTS = {
        'SearcherAgent': 0.30,
        'HMM_Engine': 0.35,
        'FFT_Engine': 0.20,
        'ProtectorAgent': 0.15,  # Negative signals carry weight
        'OptionsFlow': 0.25      # Whale detection weight
    }
    
    # Minimum confidence to emit a trade signal
    CONFIDENCE_THRESHOLD = 0.65
    
    def __init__(self, weights: Optional[Dict[str, float]] = None) -> None:
        """
        Initialize the Stacker Agent.
        
        Args:
            weights: Optional custom weights for signal sources.
        """
        super().__init__(name='StackerAgent')
        self.weights = weights or self.DEFAULT_WEIGHTS
        self.signal_stack: List[Signal] = []
        self.pending_trade: Optional[Dict[str, Any]] = None
        
        # Initialize Neo4j Driver for whale tracking
        try:
            self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        except Exception as e:
            logger.error(f"Failed to initialize Neo4j Driver in StackerAgent: {e}")
            self.driver = None
    
    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process incoming signals and aggregate them.
        
        Args:
            event: Signal event from another agent or service.
            
        Returns:
            Trade signal if confidence threshold is met.
        """
        event_type = event.get('type')
        
        if event_type == 'SIGNAL':
            return self._add_signal(event)
        elif event_type == 'OPTIONS_FLOW':
            return self._handle_options_flow(event)
        elif event_type == 'MACRO_REGIME':
            return self._handle_macro_regime(event)
        elif event_type == 'EVALUATE':
            return self._evaluate_stack()
        elif event_type == 'CLEAR_STACK':
            return self._clear_stack()
        
        return None

    def _handle_macro_regime(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle macro-economic regime updates by persisting to Neo4j.
        """
        status = event.get("status", "UNKNOWN")
        
        # 1. Persist to Neo4j
        if self.driver:
            try:
                with self.driver.session() as session:
                    # Map Macro Regime Node
                    query = """
                    MERGE (m:Regime {type: 'MACRO'})
                    SET m.status = $status,
                        m.signals = $signals,
                        m.yield_curve = $yield_curve,
                        m.inflation = $inflation,
                        m.unemployment = $unrate,
                        m.updated_at = $timestamp
                    """
                    metrics = event.get("metrics", {})
                    session.run(query,
                        status=status,
                        signals=event.get("signals", []),
                        yield_curve=metrics.get("YIELD_CURVE"),
                        inflation=metrics.get("INFLATION"),
                        unrate=metrics.get("UNEMPLOYMENT"),
                        timestamp=event.get("timestamp")
                    )
                    logger.info(f"Persisted Macro Regime to Neo4j: {status}")
            except Exception as e:
                logger.error(f"Failed to persist macro regime to Neo4j: {e}")

        # 2. Add as a signal if it's a critical regime shift
        # Recession warning is a strong SHORT signal for growth assets
        confidence = 0.9 if status == "RECESSION_WARNING" else 0.5
        direction = "SHORT" if status == "RECESSION_WARNING" else "NEUTRAL"
        
        signal_event = {
            "source": "MacroEngine",
            "signal_type": "REGIME_SHIFT",
            "direction": direction,
            "confidence": confidence,
            "data": event
        }
        
        return self._add_signal(signal_event)

    def _handle_options_flow(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle unusual options flow by persisting to Neo4j and stacking as a signal.
        """
        symbol = event.get("symbol")
        alert_type = event.get("alert_type", "UNKNOWN")
        
        # 1. Persist to Neo4j
        if self.driver:
            try:
                with self.driver.session() as session:
                    # Map Asset -> OptionsContract relationship
                    query = """
                    MERGE (a:Asset {symbol: $symbol})
                    MERGE (c:OptionsContract {
                        symbol: $symbol,
                        strike: $strike,
                        expiration: $expiration,
                        type: $type
                    })
                    MERGE (a)-[r:HAS_FLOW]->(c)
                    SET r.alert_type = $alert_type,
                        r.volume = $volume,
                        r.open_interest = $oi,
                        r.timestamp = $timestamp
                    """
                    session.run(query,
                        symbol=symbol,
                        strike=event.get("strike"),
                        expiration=event.get("expiration"),
                        type=event.get("type"),
                        alert_type=alert_type,
                        volume=event.get("volume"),
                        oi=event.get("open_interest"),
                        timestamp=event.get("timestamp")
                    )
            except Exception as e:
                logger.error(f"Failed to persist options flow to Neo4j: {e}")

        # 2. Add as a signal to the stack if confidence is high
        # Whale flow is a high-confidence sentiment signal
        confidence = 0.8 if alert_type == "WHALE_FLOW" else 0.6
        direction = "LONG" if event.get("type", "").lower() == "call" else "SHORT"
        
        signal_event = {
            "source": "OptionsFlow",
            "signal_type": alert_type,
            "direction": direction,
            "confidence": confidence,
            "data": event
        }
        
        return self._add_signal(signal_event)
    
    def _add_signal(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Add a new signal to the stack."""
        signal = Signal(
            source=event.get('source', 'Unknown'),
            signal_type=event.get('signal_type', 'UNKNOWN'),
            direction=event.get('direction', 'NEUTRAL'),
            confidence=event.get('confidence', 0.5),
            data=event.get('data', {})
        )
        
        self.signal_stack.append(signal)
        logger.info(f"Signal stacked: {signal.source} -> {signal.direction} ({signal.confidence:.2f})")
        
        return {
            'action': 'SIGNAL_STACKED',
            'stack_size': len(self.signal_stack)
        }
    
    def _evaluate_stack(self) -> Dict[str, Any]:
        """
        Evaluate all stacked signals and determine if trade should be executed.
        
        Uses weighted average of signal confidences, adjusted by direction agreement.
        """
        if not self.signal_stack:
            return {
                'action': 'NO_SIGNALS',
                'recommendation': 'HOLD'
            }
        
        # Aggregate signals
        long_score = 0.0
        short_score = 0.0
        total_weight = 0.0
        
        for signal in self.signal_stack:
            weight = self.weights.get(signal.source, 0.1)
            weighted_confidence = signal.confidence * weight
            
            if signal.direction == 'LONG':
                long_score += weighted_confidence
            elif signal.direction == 'SHORT':
                short_score += weighted_confidence
            
            total_weight += weight
        
        # Normalize scores
        if total_weight > 0:
            long_score /= total_weight
            short_score /= total_weight
        
        # Determine direction and confidence
        if long_score > short_score:
            direction = 'LONG'
            confidence = long_score
        elif short_score > long_score:
            direction = 'SHORT'
            confidence = short_score
        else:
            direction = 'NEUTRAL'
            confidence = 0.5
        
        # Check threshold
        if confidence >= self.CONFIDENCE_THRESHOLD:
            self.pending_trade = {
                'direction': direction,
                'confidence': confidence,
                'signal_count': len(self.signal_stack)
            }
            
            return {
                'action': 'TRADE_SIGNAL',
                'direction': direction,
                'confidence': confidence,
                'signal_count': len(self.signal_stack),
                'execute': True
            }
        
        return {
            'action': 'BELOW_THRESHOLD',
            'direction': direction,
            'confidence': confidence,
            'threshold': self.CONFIDENCE_THRESHOLD,
            'recommendation': 'HOLD'
        }
    
    def _clear_stack(self) -> Dict[str, Any]:
        """Clear all stacked signals."""
        count = len(self.signal_stack)
        self.signal_stack = []
        self.pending_trade = None
        
        return {
            'action': 'STACK_CLEARED',
            'cleared_count': count
        }
    
    def get_stack_summary(self) -> Dict[str, Any]:
        """Get a summary of the current signal stack."""
        return {
            'stack_size': len(self.signal_stack),
            'signals': [
                {
                    'source': s.source,
                    'direction': s.direction,
                    'confidence': s.confidence
                }
                for s in self.signal_stack
            ],
            'pending_trade': self.pending_trade
        }
