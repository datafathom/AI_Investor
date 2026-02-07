# Hunter Department Agents (`hunter/hunter_agents.py`)

The Hunter department focuses on "Venture Growth," identifying private equity opportunities, venture deals, and modeling complex cap-table scenarios.

## Cap-Table Modeler Agent (Agent 10.2)
### Description
The `CapTableModelerAgent` is a specialized financial modeler that analyzes venture deal terms, dilution risks, and exit scenarios.

### Capabilities
- **Waterfall Analysis**: Simulates exit distributions (e.g., a $1B exit) across different share classes (Series A, B, Common).
- **Round Modeling**: Simulates dilution for upcoming funding rounds based on pre-money valuations and new investment amounts.

### Integration
- **Venture Service**: Leverages a deep math engine for price-per-share and post-money valuation calculations.
- **Reporting**: Emits high-fidelity "Dilution Reports" used for investment decision-making.
