# CLI Command: lend

## Description
UHNW Stock-Based Lending & Margin Management.

## Main Help Output
```text

Command: lend
Description: UHNW Stock-Based Lending & Margin Management.

Available subcommands:
  analyze-spread       Compare cost of borrowing vs. taxes from liquidation.
  calc-capacity        Check borrowing capacity against a stock position.


```

## Subcommands

### Subcommand: `lend calc-capacity`
Check borrowing capacity against a stock position.

#### Help Output
```text

Command: lend calc-capacity
Description: Check borrowing capacity against a stock position.

Arguments:
  symbol               Ticker symbol (e.g. AAPL) (Required)
  value                Current position value (e.g. 10,000,000) (Required)

Flags:
  --vol                Symbol volatility % (Default: 20.0)


```

### Subcommand: `lend analyze-spread`
Compare cost of borrowing vs. taxes from liquidation.

#### Help Output
```text

Command: lend analyze-spread
Description: Compare cost of borrowing vs. taxes from liquidation.

Arguments:
  value                Total position value (Required)
  basis                Original cost basis (Required)


```

