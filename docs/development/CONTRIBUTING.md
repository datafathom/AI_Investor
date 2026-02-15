# Contributing to AI Investor

Thank you for your interest in contributing! This guide will help you get started.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [Getting Started](#getting-started)
3. [Development Workflow](#development-workflow)
4. [Code Style](#code-style)
5. [Testing](#testing)
6. [Pull Request Process](#pull-request-process)

---

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers
- Provide constructive feedback
- Focus on what's best for the community

---

## Getting Started

### 1. Fork and Clone

```bash
# Fork the repository on GitHub
# Then clone your fork
git clone https://github.com/your-username/ai-investor.git
cd ai-investor
```

### 2. Set Up Development Environment

See [SETUP.md](./SETUP.md) for detailed setup instructions.

### 3. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

---

## Development Workflow

### 1. Make Changes

- Write clean, readable code
- Follow existing patterns
- Add tests for new features
- Update documentation

### 2. Test Your Changes

```bash
# Backend tests
pytest

# Frontend tests
cd Frontend && npm test

# E2E tests
npm run test:e2e
```

### 3. Commit Changes

Use conventional commits:

```bash
git commit -m "feat: add new feature"
git commit -m "fix: resolve bug"
git commit -m "docs: update documentation"
```

### 4. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

---

## Code Style

### Python

- Follow PEP 8
- Use `black` for formatting
- Use `isort` for imports
- Maximum line length: 120 characters
- Type hints for function signatures

### JavaScript/TypeScript

- Follow ESLint rules
- Use Prettier for formatting
- Meaningful variable names
- Comment complex logic

### Example

```python
def calculate_portfolio_value(positions: List[Position]) -> float:
    """
    Calculate total portfolio value.
    
    Args:
        positions: List of positions
        
    Returns:
        Total portfolio value
    """
    return sum(pos.value for pos in positions)
```

---

## Testing

### Write Tests

- Unit tests for all new functions
- Integration tests for workflows
- E2E tests for user journeys
- Aim for high coverage

### Test Structure

```python
def test_calculate_portfolio_value():
    """Test portfolio value calculation."""
    positions = [
        Position(symbol='AAPL', shares=10, price=150.0),
        Position(symbol='TSLA', shares=5, price=200.0)
    ]
    
    result = calculate_portfolio_value(positions)
    
    assert result == 2500.0
```

### Run Tests

```bash
# All tests
pytest

# With coverage
pytest --cov=services --cov=web --cov-report=html

# Specific test
pytest tests/unit/test_portfolio_service.py
```

---

## Pull Request Process

### Before Submitting

1. **Update Documentation**
   - Update relevant docs
   - Add code comments
   - Update CHANGELOG if needed

2. **Add Tests**
   - Unit tests for new code
   - Integration tests if applicable
   - Update existing tests

3. **Ensure Quality**
   - Code passes linting
   - All tests pass
   - No new warnings

4. **Check CI**
   - All CI checks pass
   - No merge conflicts
   - Up to date with main

### PR Description

Include:
- What changes were made
- Why changes were needed
- How to test
- Screenshots if UI changes

### Review Process

1. PR is reviewed by maintainers
2. Address any feedback
3. Make requested changes
4. Once approved, PR is merged

---

## Commit Message Format

Use conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation
- `style:` Code style
- `refactor:` Refactoring
- `test:` Tests
- `chore:` Maintenance

Examples:
```
feat: add user onboarding flow
fix: resolve portfolio calculation bug
docs: update API documentation
test: add integration tests for legal flow
```

---

## Project Structure

```
ai-investor/
├── services/          # Backend services
├── web/              # Web API and routes
├── Frontend/         # React 19 + Vite 5 frontend
├── tests/            # Test files
├── scripts/          # CLI runners & utility scripts
├── config/           # CLI configuration & color palette
├── docs/             # Documentation
├── DEBUGGING/        # Frontend audit tools & results
└── cli.py            # Unified CLI entry point
```

---

## Questions?

- Open an issue for questions
- Check existing documentation
- Ask in discussions
- Contact maintainers

Thank you for contributing! 🎉

---

**Last Updated**: 2026-02-14
