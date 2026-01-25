"""
FX Service - Foreign Exchange Rate Management

Phase 56: Provides real-time FX rates, currency conversion,
and cash optimization features.

Features:
- Real-time FX rate tracking
- Multi-currency balance management
- Sweep suggestions for idle cash
- Repo rate comparison

Usage:
    service = FXService()
    rates = await service.get_fx_rates()
    result = await service.execute_conversion("USD", "EUR", 10000)
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from enum import Enum
import logging

logger = logging.getLogger(__name__)


class Currency(Enum):
    """Supported currencies."""
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    JPY = "JPY"
    CHF = "CHF"
    CAD = "CAD"


@dataclass
class FXRate:
    """Foreign exchange rate."""
    pair: str
    base: str
    quote: str
    rate: float
    bid: float
    ask: float
    spread_bps: float
    change_24h: float
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class CurrencyBalance:
    """Currency balance."""
    currency: str
    amount: float
    amount_usd: float
    interest_rate: float
    allocation_pct: float = 0.0


@dataclass
class SweepSuggestion:
    """Cash sweep suggestion."""
    id: str
    from_currency: str
    to_vehicle: str
    amount: float
    projected_yield: float
    risk: str  # "low", "medium", "high"
    description: str


@dataclass
class RepoRate:
    """Overnight repo rate."""
    region: str
    name: str
    rate: float
    change: float


@dataclass
class ConversionResult:
    """FX conversion result."""
    from_currency: str
    to_currency: str
    from_amount: float
    to_amount: float
    rate_used: float
    spread_cost: float
    timestamp: str


class FXService:
    """
    Service for foreign exchange and cash management.
    
    Provides FX rates, conversion, and cash optimization.
    """
    
    def __init__(self) -> None:
        """Initialize the FX service."""
        self._balances: Dict[str, CurrencyBalance] = {}
        self._initialize_mock_balances()
        logger.info("FXService initialized")
    
    def _initialize_mock_balances(self) -> None:
        """Initialize mock balances for demo."""
        self._balances = {
            "USD": CurrencyBalance("USD", 125000.0, 125000.0, 5.25),
            "EUR": CurrencyBalance("EUR", 45000.0, 48600.0, 4.0),
            "GBP": CurrencyBalance("GBP", 25000.0, 31750.0, 5.0),
            "JPY": CurrencyBalance("JPY", 5000000.0, 33333.0, 0.1),
            "CHF": CurrencyBalance("CHF", 10000.0, 11765.0, 1.5),
            "CAD": CurrencyBalance("CAD", 15000.0, 11029.0, 4.75),
        }
    
    async def get_fx_rates(self) -> List[FXRate]:
        """
        Get current FX rates.
        
        Returns:
            List of FX rates for major pairs
        """
        # Mock FX rates
        rates = [
            FXRate("EUR/USD", "EUR", "USD", 1.08, 1.0798, 1.0802, 3.7, 0.15),
            FXRate("GBP/USD", "GBP", "USD", 1.27, 1.2698, 1.2702, 3.1, -0.08),
            FXRate("USD/JPY", "USD", "JPY", 150.0, 149.98, 150.02, 2.7, 0.22),
            FXRate("USD/CHF", "USD", "CHF", 0.85, 0.8498, 0.8502, 4.7, -0.12),
            FXRate("USD/CAD", "USD", "CAD", 1.36, 1.3598, 1.3602, 2.9, 0.05),
            FXRate("EUR/GBP", "EUR", "GBP", 0.85, 0.8498, 0.8502, 4.7, 0.10),
        ]
        return rates
    
    async def get_balances(self) -> List[CurrencyBalance]:
        """
        Get all currency balances.
        
        Returns:
            List of currency balances
        """
        return list(self._balances.values())
    
    async def get_total_value_usd(self) -> float:
        """Get total portfolio value in USD."""
        return sum(b.amount_usd for b in self._balances.values())
    
    async def execute_conversion(
        self,
        from_currency: str,
        to_currency: str,
        amount: float
    ) -> ConversionResult:
        """
        Execute FX conversion.

        Args:
            from_currency: Source currency
            to_currency: Target currency
            amount: Amount to convert

        Returns:
            ConversionResult with execution details
        """
        rates = await self.get_fx_rates()

        # Find appropriate rate
        pair = f"{from_currency}/{to_currency}"
        reverse_pair = f"{to_currency}/{from_currency}"

        rate_obj = next((r for r in rates if r.pair == pair), None)
        is_reverse = False

        if not rate_obj:
            rate_obj = next((r for r in rates if r.pair == reverse_pair), None)
            is_reverse = True

        if not rate_obj:
            # Use USD as intermediary
            from_usd = 1.0 if from_currency == "USD" else next(
                (r.rate for r in rates if r.pair == f"{from_currency}/USD"), 1.0
            )
            to_usd = 1.0 if to_currency == "USD" else next(
                (r.rate for r in rates if r.pair == f"USD/{to_currency}"), 1.0
            )
            rate = from_usd * to_usd
            spread_cost = amount * 0.001  # 10bps
        else:
            rate = 1 / rate_obj.rate if is_reverse else rate_obj.rate
            spread_cost = amount * (rate_obj.spread_bps / 10000)

        to_amount = amount * rate

        # Update balances
        if from_currency in self._balances:
            self._balances[from_currency].amount -= amount

        if to_currency in self._balances:
            self._balances[to_currency].amount += to_amount

        logger.info("Converted %s %s to %.2f %s", amount, from_currency, to_amount, to_currency)

        return ConversionResult(
            from_currency=from_currency,
            to_currency=to_currency,
            from_amount=amount,
            to_amount=to_amount,
            rate_used=rate,
            spread_cost=spread_cost,
            timestamp=datetime.now().isoformat()
        )

    async def get_sweep_suggestions(self) -> List[SweepSuggestion]:
        """
        Get cash sweep suggestions.

        Returns:
            List of suggestions for optimizing idle cash
        """
        usd_balance = self._balances.get("USD")
        suggestions = []

        if usd_balance and usd_balance.amount > 50000:
            idle_amount = usd_balance.amount - 50000

            suggestions.append(SweepSuggestion(
                id="sweep-mmf-1",
                from_currency="USD",
                to_vehicle="Government MMF",
                amount=idle_amount * 0.5,
                projected_yield=5.1,
                risk="low",
                description="Move to government money market fund for 5.1% yield"
            ))

            suggestions.append(SweepSuggestion(
                id="sweep-tbill-1",
                from_currency="USD",
                to_vehicle="3M T-Bill",
                amount=idle_amount * 0.3,
                projected_yield=5.25,
                risk="low",
                description="Purchase 3-month Treasury bills"
            ))

            if idle_amount > 100000:
                suggestions.append(SweepSuggestion(
                    id="sweep-repo-1",
                    from_currency="USD",
                    to_vehicle="Overnight Repo",
                    amount=idle_amount * 0.2,
                    projected_yield=5.3,
                    risk="low",
                    description="Overnight repo for maximum liquidity"
                ))

        return suggestions

    async def get_repo_rates(self) -> List[RepoRate]:
        """
        Get overnight repo rates by region.

        Returns:
            List of repo rates for major markets
        """
        return [
            RepoRate("US", "Fed Funds Rate", 5.33, 0.0),
            RepoRate("US", "SOFR", 5.31, -0.01),
            RepoRate("EU", "€STR", 3.90, 0.0),
            RepoRate("UK", "SONIA", 5.19, 0.0),
            RepoRate("JP", "TONAR", 0.07, 0.0),
            RepoRate("CH", "SARON", 1.45, -0.05),
        ]

    async def detect_carry_trade_opportunity(self) -> Dict:
        """
        Detect carry trade opportunities.

        Looks for interest rate differentials.

        Returns:
            Carry trade opportunity if exists
        """
        balances = await self.get_balances()

        # Find highest and lowest yield currencies
        highest = max(balances, key=lambda b: b.interest_rate)
        lowest = min(balances, key=lambda b: b.interest_rate)

        spread = highest.interest_rate - lowest.interest_rate

        if spread > 4.0:
            return {
                "opportunity": True,
                "borrow_currency": lowest.currency,
                "invest_currency": highest.currency,
                "spread_percent": spread,
                "description": f"Borrow {lowest.currency} at {lowest.interest_rate}%, invest in {highest.currency} at {highest.interest_rate}%"
            }

        return {"opportunity": False}

    async def check_exposure_limit(
        self,
        currency: str,
        additional_amount_usd: float
    ) -> bool:
        """
        Check if currency exposure exceeds 15% limit.

        Args:
            currency: Currency to check
            additional_amount_usd: Additional exposure in USD

        Returns:
            True if limit would be exceeded
        """
        total = await self.get_total_value_usd()
        current = self._balances.get(currency)
        current_usd = current.amount_usd if current else 0

        new_exposure = (current_usd + additional_amount_usd) / total
        return new_exposure > 0.15

    def get_supported_currencies(self) -> List[str]:
        """Get list of supported currencies."""
        return [c.value for c in Currency]


# Singleton instance
_fx_service: Optional[FXService] = None


def get_fx_service() -> FXService:
    """Get or create FX service singleton."""
    global _fx_service
    if _fx_service is None:
        _fx_service = FXService()
    return _fx_service
