# Protector Agent (`protector_agent.py`)

## Description
Known as "The Warden," the `ProtectorAgent` is the final gatekeeper for all trade executions. It enforces rigid risk management protocols and the "Prime Directive" of capital preservation.

## Role in Department
Acts as the "Chief Risk Officer" for the entire system. No trade can reach the exchange without the Warden's approval.

## Input & Output
- **Input**: Trade execution requests (`VALIDATE_ORDER`) including amount, current balance, and daily loss meta-data.
- **Output**: `APPROVE` or `REJECT` decision with a clear reason.

## Risk Protocols enforced
- **Circuit Breaker**: Stops all trading if daily loss thresholds are exceeded or if the system detects excessive volatility.
- **1% Rule**: Prevents any single trade from risking more than 1% of the total account equity.
- **Validation**: Integrates with the `RiskManager` service for complex rule evaluation.

## Integration
- **Trader Department**: Sits at the end of the order routing pipeline.
- **Observability**: Emits high-priority traces on any security or risk violation.
