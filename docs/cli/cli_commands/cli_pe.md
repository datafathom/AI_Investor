# CLI Command: pe

## Description
Private Equity (PE) LBO Modeling & Portfolio Insights.

## Main Help Output
```text

Command: pe
Description: Private Equity (PE) LBO Modeling & Portfolio Insights.

Available subcommands:
  calc-lbo             Run a quick LBO model (IRR/MOIC).
  sensitize            Run a Monte Carlo sensitivity analysis on the business plan.
  sim-cuts             Run an operational efficiency simulation (SG&A cuts).
  vintage-stats        Show historical performance for a PE vintage year.


```

## Subcommands

### Subcommand: `pe calc-lbo`
Run a quick LBO model (IRR/MOIC).

#### Help Output
```text

Command: pe calc-lbo
Description: Run a quick LBO model (IRR/MOIC).

Arguments:
  ebitda               Entry EBITDA (e.g. 50,000,000) (Required)
  multiple             Entry EBITDA Multiple (e.g. 8.5) (Required)

Flags:
  --equity-pct         Equity contribution percentage (default 0.3) (Default: 0.3)


```

### Subcommand: `pe vintage-stats`
Show historical performance for a PE vintage year.

#### Help Output
```text

Command: pe vintage-stats
Description: Show historical performance for a PE vintage year.

Arguments:
  year                 Vintage year (e.g. 2008) (Required)


```

### Subcommand: `pe sim-cuts`
Run an operational efficiency simulation (SG&A cuts).

#### Help Output
```text

Command: pe sim-cuts
Description: Run an operational efficiency simulation (SG&A cuts).

Arguments:
  ebitda               Starting EBITDA (Required)
  opex                 Baseline OpEx (Required)
  cut-pct              Percentage of OpEx to cut (e.g. 15) (Required)


```

### Subcommand: `pe sensitize`
Run a Monte Carlo sensitivity analysis on the business plan.

#### Help Output
```text

Command: pe sensitize
Description: Run a Monte Carlo sensitivity analysis on the business plan.

Arguments:
  ebitda               Projected EBITDA (Required)
  multiple             Exit Multiple (Required)


```

