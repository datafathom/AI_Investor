# CLI Command: risk

## Description
Hidden Volatility & Gap Analysis for Private Assets.

## Main Help Output
```text

Command: risk
Description: Hidden Volatility & Gap Analysis for Private Assets.

Available subcommands:
  calc-gap             Analyze valuation gaps between private NAV and public proxies.
  true-vol             Calculate 'True' volatility by unsmoothing private returns.


```

## Subcommands

### Subcommand: `risk calc-gap`
Analyze valuation gaps between private NAV and public proxies.

#### Help Output
```text

Command: risk calc-gap
Description: Analyze valuation gaps between private NAV and public proxies.

Arguments:
  asset_name           Name of the private asset (Required)
  nav                  Current reported NAV (Required)
  ticker               Public proxy ticker (e.g. QQQ) (Required)


```

### Subcommand: `risk true-vol`
Calculate 'True' volatility by unsmoothing private returns.

#### Help Output
```text

Command: risk true-vol
Description: Calculate 'True' volatility by unsmoothing private returns.

Arguments:
  vol                  Reported volatility (e.g. 0.12) (Required)
  gap                  Valuation gap (e.g. 0.25) (Required)
  lockup               Liquidity lockup years (Required)


```

