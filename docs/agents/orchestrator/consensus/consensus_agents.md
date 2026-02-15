# Consensus Department Agents (`consensus/`)

The Consensus department manages the multi-agent voting system used to authorize high-value decisions.

## Consensus Engine (`consensus_engine.py`)
### Description
The `ConsensusEngine` evaluates votes from different agents to determine if a proposal has sufficient support to proceed.

### Role
Acts as the "Democracy Matrix" of the Sovereign OS.

### Logic
- **Weighted Voting**: Agents with higher historical accuracy (reputation) or seniority have higher vote weights.
- **Thresholds**: Requires a minimum number of voters and a weighted majority to approve a trade.

---

## Vote Aggregator (`vote_aggregator.py`)
### Description
The `VoteAggregator` is a service that tracks individual agent votes, their justifications (personas), and their weights for any given proposal ID.

### Integration
- **Debate Chamber**: Captures votes emitted during the adversarial debate process.
- **Persistence**: Final vote counts are logged for transparency and future auditing by the `Auditor` department.
