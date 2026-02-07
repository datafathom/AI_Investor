# CLI Command: rule144

## Description
Rule 144 Compliance & Market Anomaly Detection.

## Main Help Output
```text

Command: rule144
Description: Rule 144 Compliance & Market Anomaly Detection.

Available subcommands:
  audit                Audit insider status and promo spikes.
  check-bots           Analyze social volume for bot attacks.
  check-limit          Check Rule 144(e) volume limits.
  scan-anomalies       Scan watchlist for pump-and-dump anomalies.


```

## Subcommands

### Subcommand: `rule144 scan-anomalies`
Scan watchlist for pump-and-dump anomalies.

#### Help Output
```text

Command: rule144 scan-anomalies
Description: Scan watchlist for pump-and-dump anomalies.


```

### Subcommand: `rule144 check-bots`
Analyze social volume for bot attacks.

#### Help Output
```text

Command: rule144 check-bots
Description: Analyze social volume for bot attacks.

Arguments:
  ticker               Stock Ticker (Required)


```

### Subcommand: `rule144 audit`
Audit insider status and promo spikes.

#### Help Output
```text

Command: rule144 audit
Description: Audit insider status and promo spikes.

Arguments:
  ticker               Stock Ticker (Required)


```

### Subcommand: `rule144 check-limit`
Check Rule 144(e) volume limits.

#### Help Output
```text

Command: rule144 check-limit
Description: Check Rule 144(e) volume limits.

Arguments:
  ticker               Stock Ticker (Required)
  shares               Shares to sell (Required)
  outstanding          Total outstanding shares (Required)
  vol                  Average weekly volume (Required)


```

