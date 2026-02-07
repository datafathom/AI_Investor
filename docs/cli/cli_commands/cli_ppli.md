# CLI Command: ppli

## Description
Private Placement Life Insurance (PPLI) & MEC Testing.

## Main Help Output
```text

Command: ppli
Description: Private Placement Life Insurance (PPLI) & MEC Testing.

Available subcommands:
  check-mec            Run the IRS 7-pay test to avoid MEC status.
  optimize-premium     Optimize premium cadence to maximize IRR within MEC limits.
  rank-assets          Rank portfolio assets by tax drag to identify PPLI candidates.
  value                Check cash value and borrowing headroom for a policy.


```

## Subcommands

### Subcommand: `ppli check-mec`
Run the IRS 7-pay test to avoid MEC status.

#### Help Output
```text

Command: ppli check-mec
Description: Run the IRS 7-pay test to avoid MEC status.

Arguments:
  premium              Cumulative premium paid (Required)
  limit                IRS 7-pay premium limit (Required)


```

### Subcommand: `ppli value`
Check cash value and borrowing headroom for a policy.

#### Help Output
```text

Command: ppli value
Description: Check cash value and borrowing headroom for a policy.

Arguments:
  id                   Policy ID (Required)


```

### Subcommand: `ppli optimize-premium`
Optimize premium cadence to maximize IRR within MEC limits.

#### Help Output
```text

Command: ppli optimize-premium
Description: Optimize premium cadence to maximize IRR within MEC limits.

Arguments:
  total                Total planned investment (Required)
  years                Number of years to spread payments (Required)

Flags:
  --rate               Projected ROI percentage (default 6.0) (Default: 6.0)


```

### Subcommand: `ppli rank-assets`
Rank portfolio assets by tax drag to identify PPLI candidates.

#### Help Output
```text

Command: ppli rank-assets
Description: Rank portfolio assets by tax drag to identify PPLI candidates.


```

