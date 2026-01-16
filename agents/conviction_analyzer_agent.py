"""
==============================================================================
AI Investor - Conviction Analyzer Agent
==============================================================================
PURPOSE:
    Analyzes investment opportunities for "Sure Thing" high-conviction plays.
    
    SURE THING CRITERIA:
    1. MOAT DETECTION:
       - Technology corner (NVIDIA CUDA, ARM architecture)
       - Network effects (Visa, Mastercard payment rails)
       - Switching costs (Enterprise software, CrowdStrike)
       
    2. CATALYST DETECTION:
       - Government contracts (COVID biotech, defense)
       - Corporate insurance events (vendor lock-in after incident)
       - Regulatory capture (pharmacy benefit managers)
       
    3. VALUE DISLOCATION:
       - Market panic selling (systematic, not fundamental)
       - Misunderstood earnings (one-time charges)
       - Sector rotation (temporary outflow)

PATTERN:
    - Analyzes news, filings, and market data
    - Scores conviction level (LOW, MEDIUM, HIGH, SURE_THING)
    - Recommends position sizing and leverage
    - Feeds into StackerAgent for execution
==============================================================================
"""
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from enum import Enum
import logging

from agents.base_agent import BaseAgent
from services.portfolio_manager import ConvictionLevel

logger = logging.getLogger(__name__)


class MoatType(Enum):
    """Types of competitive moats."""
    TECHNOLOGY_CORNER = "technology_corner"     # NVIDIA CUDA, ARM
    NETWORK_EFFECTS = "network_effects"         # Visa, Facebook
    SWITCHING_COSTS = "switching_costs"         # Enterprise software
    REGULATORY_CAPTURE = "regulatory_capture"   # Utilities, PBMs
    BRAND_LOYALTY = "brand_loyalty"             # Apple, luxury brands
    COST_ADVANTAGE = "cost_advantage"           # Amazon, Walmart
    INTANGIBLE_ASSETS = "intangible_assets"     # Patents, licenses


class CatalystType(Enum):
    """Types of catalysts for sure-thing plays."""
    GOVERNMENT_CONTRACT = "government_contract"     # Defense, healthcare
    CORPORATE_INSURANCE = "corporate_insurance"     # Vendor lock-in after incident
    MARKET_PANIC = "market_panic"                   # Systematic selling
    EARNINGS_MISREAD = "earnings_misread"           # One-time charges
    SECTOR_ROTATION = "sector_rotation"             # Temporary outflow
    REGULATORY_APPROVAL = "regulatory_approval"     # FDA, FCC
    ACQUISITION_TARGET = "acquisition_target"       # M&A premium


@dataclass
class ConvictionAnalysis:
    """Result of a conviction analysis."""
    symbol: str
    conviction_level: ConvictionLevel
    moat_types: List[MoatType]
    catalysts: List[CatalystType]
    thesis: str
    recommended_leverage: float
    recommended_allocation: float  # % of aggressive portfolio
    risk_factors: List[str]
    confidence_score: float  # 0.0 to 1.0


class ConvictionAnalyzerAgent(BaseAgent):
    """
    Analyzes opportunities for high-conviction "Sure Thing" plays.
    
    Detects moats, catalysts, and value dislocations to identify
    opportunities for leveraged aggressive positions.
    """
    
    # Leverage recommendations by conviction level
    LEVERAGE_RECOMMENDATIONS = {
        ConvictionLevel.LOW: 1.0,
        ConvictionLevel.MEDIUM: 1.0,
        ConvictionLevel.HIGH: 1.5,
        ConvictionLevel.SURE_THING: 2.0
    }
    
    # Allocation recommendations by conviction level (% of aggressive portfolio)
    ALLOCATION_RECOMMENDATIONS = {
        ConvictionLevel.LOW: 0.02,      # 2%
        ConvictionLevel.MEDIUM: 0.05,   # 5%
        ConvictionLevel.HIGH: 0.10,     # 10%
        ConvictionLevel.SURE_THING: 0.20  # 20%
    }
    
    def __init__(self) -> None:
        super().__init__(name='ConvictionAnalyzerAgent')
        self.analyses: List[ConvictionAnalysis] = []
    
    def process_event(self, event: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Process analysis events.
        
        Args:
            event: Event containing analysis parameters.
        """
        event_type = event.get('type')
        
        if event_type == 'ANALYZE_OPPORTUNITY':
            return self._analyze_opportunity(event)
        elif event_type == 'CHECK_MOAT':
            return self._check_moat(event)
        elif event_type == 'CHECK_CATALYST':
            return self._check_catalyst(event)
        
        return None
    
    def _analyze_opportunity(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze an investment opportunity for conviction level.
        
        Args:
            event: Contains symbol, context, and optional signals.
        """
        symbol = event.get('symbol', 'UNKNOWN')
        context = event.get('context', {})
        
        # Detect moats
        moats = self._detect_moats(symbol, context)
        
        # Detect catalysts
        catalysts = self._detect_catalysts(symbol, context)
        
        # Calculate conviction
        conviction = self._calculate_conviction(moats, catalysts, context)
        
        # Generate thesis
        thesis = self._generate_thesis(symbol, moats, catalysts, context)
        
        # Calculate risk factors
        risks = self._identify_risks(symbol, context)
        
        analysis = ConvictionAnalysis(
            symbol=symbol,
            conviction_level=conviction,
            moat_types=moats,
            catalysts=catalysts,
            thesis=thesis,
            recommended_leverage=self.LEVERAGE_RECOMMENDATIONS[conviction],
            recommended_allocation=self.ALLOCATION_RECOMMENDATIONS[conviction],
            risk_factors=risks,
            confidence_score=self._calculate_confidence(moats, catalysts)
        )
        
        self.analyses.append(analysis)
        
        return {
            'action': 'ANALYSIS_COMPLETE',
            'symbol': symbol,
            'conviction': conviction.name,
            'thesis': thesis,
            'recommendation': {
                'leverage': analysis.recommended_leverage,
                'allocation': analysis.recommended_allocation,
                'portfolio': 'AGGRESSIVE' if conviction.value >= ConvictionLevel.HIGH.value else 'DEFENSIVE'
            }
        }
    
    def _detect_moats(self, symbol: str, context: Dict[str, Any]) -> List[MoatType]:
        """Detect competitive moats for the given symbol."""
        moats = []
        
        # Example logic - in production, this would analyze real data
        moat_indicators = context.get('moat_indicators', [])
        
        if 'technology_lead' in moat_indicators:
            moats.append(MoatType.TECHNOLOGY_CORNER)
        if 'network_effects' in moat_indicators:
            moats.append(MoatType.NETWORK_EFFECTS)
        if 'high_switching_costs' in moat_indicators:
            moats.append(MoatType.SWITCHING_COSTS)
        if 'regulatory_protection' in moat_indicators:
            moats.append(MoatType.REGULATORY_CAPTURE)
        
        # Known moat companies (simplified examples)
        known_moats = {
            'NVDA': [MoatType.TECHNOLOGY_CORNER],
            'V': [MoatType.NETWORK_EFFECTS],
            'MSFT': [MoatType.SWITCHING_COSTS, MoatType.NETWORK_EFFECTS],
            'AAPL': [MoatType.BRAND_LOYALTY, MoatType.SWITCHING_COSTS]
        }
        
        if symbol in known_moats:
            moats.extend(known_moats[symbol])
        
        return list(set(moats))  # Remove duplicates
    
    def _detect_catalysts(self, symbol: str, context: Dict[str, Any]) -> List[CatalystType]:
        """Detect catalysts that could drive the opportunity."""
        catalysts = []
        
        catalyst_signals = context.get('catalyst_signals', [])
        
        if 'government_contract' in catalyst_signals:
            catalysts.append(CatalystType.GOVERNMENT_CONTRACT)
        if 'incident_vendor_lock' in catalyst_signals:
            catalysts.append(CatalystType.CORPORATE_INSURANCE)
        if 'market_panic' in catalyst_signals:
            catalysts.append(CatalystType.MARKET_PANIC)
        if 'earnings_misunderstood' in catalyst_signals:
            catalysts.append(CatalystType.EARNINGS_MISREAD)
        
        return catalysts
    
    def _calculate_conviction(
        self,
        moats: List[MoatType],
        catalysts: List[CatalystType],
        context: Dict[str, Any]
    ) -> ConvictionLevel:
        """Calculate conviction level based on moats and catalysts."""
        score = 0
        
        # Score moats (each moat = 2 points)
        score += len(moats) * 2
        
        # Score catalysts (each catalyst = 1 point)
        score += len(catalysts)
        
        # Bonus for technology corner + catalyst
        if MoatType.TECHNOLOGY_CORNER in moats and len(catalysts) > 0:
            score += 2
        
        # Bonus for switching costs + incident
        if MoatType.SWITCHING_COSTS in moats and CatalystType.CORPORATE_INSURANCE in catalysts:
            score += 3
        
        # Convert score to conviction
        if score >= 8:
            return ConvictionLevel.SURE_THING
        elif score >= 5:
            return ConvictionLevel.HIGH
        elif score >= 3:
            return ConvictionLevel.MEDIUM
        else:
            return ConvictionLevel.LOW
    
    def _generate_thesis(
        self,
        symbol: str,
        moats: List[MoatType],
        catalysts: List[CatalystType],
        context: Dict[str, Any]
    ) -> str:
        """Generate investment thesis string."""
        parts = [f"{symbol}:"]
        
        if moats:
            moat_str = ", ".join(m.value for m in moats)
            parts.append(f"Moats: {moat_str}.")
        
        if catalysts:
            cat_str = ", ".join(c.value for c in catalysts)
            parts.append(f"Catalysts: {cat_str}.")
        
        custom_thesis = context.get('thesis', '')
        if custom_thesis:
            parts.append(custom_thesis)
        
        return " ".join(parts)
    
    def _identify_risks(self, symbol: str, context: Dict[str, Any]) -> List[str]:
        """Identify risk factors for the opportunity."""
        risks = context.get('risk_factors', [])
        
        # Add standard risks
        default_risks = [
            "Market volatility",
            "Sector rotation",
            "Regulatory changes"
        ]
        
        return risks + default_risks
    
    def _calculate_confidence(
        self,
        moats: List[MoatType],
        catalysts: List[CatalystType]
    ) -> float:
        """Calculate confidence score (0.0 to 1.0)."""
        base = 0.5
        
        # Each moat adds 0.1, max 0.3
        moat_bonus = min(len(moats) * 0.1, 0.3)
        
        # Each catalyst adds 0.05, max 0.2
        catalyst_bonus = min(len(catalysts) * 0.05, 0.2)
        
        return min(base + moat_bonus + catalyst_bonus, 1.0)
    
    def _check_moat(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Check if a company has a specific moat."""
        symbol = event.get('symbol')
        moat_type = event.get('moat_type')
        
        # Simplified check
        return {
            'symbol': symbol,
            'moat_type': moat_type,
            'has_moat': True,  # Would be actual analysis in production
            'strength': 'STRONG'
        }
    
    def _check_catalyst(self, event: Dict[str, Any]) -> Dict[str, Any]:
        """Check for active catalysts."""
        symbol = event.get('symbol')
        
        return {
            'symbol': symbol,
            'active_catalysts': [],
            'pending_catalysts': []
        }
    
    def get_sure_things(self) -> List[ConvictionAnalysis]:
        """Return all SURE_THING level analyses."""
        return [a for a in self.analyses if a.conviction_level == ConvictionLevel.SURE_THING]
