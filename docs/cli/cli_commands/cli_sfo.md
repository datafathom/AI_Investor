# CLI Command: sfo

## Description
Single Family Office (SFO) Economics & Strategy.

## Main Help Output
```text

Command: sfo
Description: Single Family Office (SFO) Economics & Strategy.

Available subcommands:
  analyze              Analyze SFO economic viability vs external fees.
  audit-access         Audit privacy advantages and access logs.
  audit-governance     Audit and ratify family constitution and mission.
  budget-template      Output a standard SFO operating budget template.
  calc-spending        Calculate sustainable spending based on real returns.
  lockdown             Enable 'Black Hole' mode (Full privacy).


```

## Subcommands

### Subcommand: `sfo analyze`
Analyze SFO economic viability vs external fees.

#### Help Output
```text

Command: sfo analyze
Description: Analyze SFO economic viability vs external fees.

Arguments:
  aum                  Total Assets Under Management (e.g. 150,000,000) (Required)

Flags:
  --external-bps       External advisor fee in basis points (default 100) (Default: 100)


```

### Subcommand: `sfo budget-template`
Output a standard SFO operating budget template.

#### Help Output
```text

Command: sfo budget-template
Description: Output a standard SFO operating budget template.


```

### Subcommand: `sfo lockdown`
Enable 'Black Hole' mode (Full privacy).

#### Help Output
```text

Command: sfo lockdown
Description: Enable 'Black Hole' mode (Full privacy).

Arguments:
  office-id            Account identifier (Required)


```

### Subcommand: `sfo audit-access`
Audit privacy advantages and access logs.

#### Help Output
```text

Command: sfo audit-access
Description: Audit privacy advantages and access logs.


```

### Subcommand: `sfo calc-spending`
Calculate sustainable spending based on real returns.

#### Help Output
```text

Command: sfo calc-spending
Description: Calculate sustainable spending based on real returns.

Arguments:
  aum                  Total Portfolio Value (Required)
  returns              Nominal annual return % (Required)
  inflation            Annual inflation rate % (Required)


```

### Subcommand: `sfo audit-governance`
Audit and ratify family constitution and mission.

#### Help Output
```text

Command: sfo audit-governance
Description: Audit and ratify family constitution and mission.

Arguments:
  family-id            UUID of the family office (Required)


```

