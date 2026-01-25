# Contributing to AI Investor

Thank you for your interest in contributing to AI Investor! This document provides guidelines for contributing.

## Code of Conduct

- Be respectful and inclusive
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Respect different viewpoints

## Getting Started

1. Fork the repository
2. Clone your fork
3. Create a feature branch: `git checkout -b feature/your-feature`
4. Make your changes
5. Commit with clear messages
6. Push to your fork
7. Create a Pull Request

## Development Workflow

### 1. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Changes

- Write clean, readable code
- Follow existing code style
- Add tests for new features
- Update documentation

### 3. Commit Changes

```bash
git add .
git commit -m "feat: add new feature"
```

### 4. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub.

## Code Style

### Python

- Follow PEP 8
- Use `black` for formatting
- Use `isort` for imports
- Maximum line length: 120 characters

### JavaScript/TypeScript

- Follow ESLint rules
- Use Prettier for formatting
- Use meaningful variable names

## Testing

### Write Tests

- Unit tests for all new functions
- Integration tests for workflows
- E2E tests for user journeys

### Run Tests

```bash
# Backend
pytest

# Frontend
cd frontend2 && npm test
```

## Pull Request Process

1. **Update Documentation**: Update relevant docs
2. **Add Tests**: Include tests for new features
3. **Update CHANGELOG**: Add entry if applicable
4. **Ensure Tests Pass**: All CI checks must pass
5. **Get Review**: Wait for code review
6. **Address Feedback**: Make requested changes

## Commit Message Format

Use conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Test additions/changes
- `chore:` Maintenance tasks

Example:
```
feat: add user onboarding flow
fix: resolve portfolio calculation bug
docs: update API documentation
```

## Review Process

1. PR is reviewed by maintainers
2. Address any feedback
3. Once approved, PR is merged
4. Feature is included in next release

## Questions?

- Open an issue for questions
- Check existing documentation
- Ask in discussions

Thank you for contributing! 🎉

---

**Last Updated**: 2026-01-21
