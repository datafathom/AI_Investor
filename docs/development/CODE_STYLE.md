# Code Style Guide

This guide outlines the coding standards for AI Investor.

## Python Style

### General Rules

- Follow PEP 8
- Maximum line length: 120 characters
- Use 4 spaces for indentation (no tabs)
- Use type hints for function signatures
- Write docstrings for all functions and classes

### Naming Conventions

- **Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private**: Prefix with `_`

### Example

```python
from typing import List, Optional

class PortfolioService:
    """Portfolio management service."""
    
    MAX_POSITIONS = 100
    
    def calculate_value(self, positions: List[Position]) -> float:
        """
        Calculate total portfolio value.
        
        Args:
            positions: List of positions
            
        Returns:
            Total value
        """
        return sum(pos.value for pos in positions)
```

### Imports

- Group imports: standard library, third-party, local
- Use `isort` for import sorting
- Absolute imports preferred

```python
# Standard library
import os
from typing import List

# Third-party
from flask import Flask
import pandas as pd

# Local
from services.portfolio import PortfolioService
```

---

## JavaScript/TypeScript Style

### General Rules

- Use ESLint configuration
- Use Prettier for formatting
- Use meaningful variable names
- Comment complex logic

### Naming Conventions

- **Functions**: `camelCase`
- **Components**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Files**: `kebab-case` or `PascalCase` for components

### Example

```javascript
const MAX_RETRIES = 3;

function calculatePortfolioValue(positions) {
  return positions.reduce((sum, pos) => sum + pos.value, 0);
}

const PortfolioComponent = ({ portfolio }) => {
  const value = calculatePortfolioValue(portfolio.positions);
  return <div>Value: ${value}</div>;
};
```

---

## Documentation

### Docstrings

Use Google-style docstrings:

```python
def process_order(order: Order) -> bool:
    """
    Process a trading order.
    
    Args:
        order: Order to process
        
    Returns:
        True if successful, False otherwise
        
    Raises:
        ValueError: If order is invalid
    """
    pass
```

### Comments

- Explain **why**, not **what**
- Keep comments up to date
- Remove commented-out code

---

## Testing

### Test Structure

```python
def test_calculate_portfolio_value():
    """Test portfolio value calculation."""
    # Arrange
    positions = [Position(symbol='AAPL', value=1000)]
    
    # Act
    result = calculate_value(positions)
    
    # Assert
    assert result == 1000
```

### Test Naming

- Test files: `test_*.py`
- Test functions: `test_*`
- Descriptive test names

---

## Git Workflow

### Branch Naming

- Features: `feature/description`
- Fixes: `fix/description`
- Docs: `docs/description`

### Commit Messages

Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Code style
- `refactor:` Refactoring
- `test:` Tests
- `chore:` Maintenance

---

## Code Review Guidelines

### What to Review

- Code correctness
- Performance implications
- Security concerns
- Test coverage
- Documentation

### Review Checklist

- [ ] Code follows style guide
- [ ] Tests are included
- [ ] Documentation updated
- [ ] No security issues
- [ ] Performance acceptable
- [ ] Error handling present

---

**Last Updated**: 2026-01-21
