# Test Runner - Quick Reference Card

## Most Common Commands

```bash
# List all categories
python cli.py test list

# Run all tests
python cli.py test all

# Quick smoke tests
python cli.py test quick

# Backend services
python cli.py test backend

# Frontend components
python cli.py test frontend

# API endpoints
python cli.py test api

# Models
python cli.py test models

# Specific category
python cli.py test-category api-trading --coverage --verbose
```

## By Phase/Feature

```bash
# Backend by phase
python cli.py test-category backend-phase1
python cli.py test-category backend-phase2
python cli.py test-category backend-phase3
python cli.py test-category backend-phase4

# API by category
python cli.py test-category api-trading
python cli.py test-category api-payments
python cli.py test-category api-crypto
python cli.py test-category api-social
python cli.py test-category api-ai
python cli.py test-category api-financial
python cli.py test-category api-market
python cli.py test-category api-risk
python cli.py test-category api-tax

# Models by category
python cli.py test-category models-core
python cli.py test-category models-financial
python cli.py test-category models-platform
python cli.py test-category models-ai
```

## With Options

```bash
# Verbose output
python cli.py test backend --verbose

# With coverage
python cli.py test backend --coverage

# Stop on first failure
python cli.py test backend --fail-fast

# Parallel execution
python cli.py test backend --parallel

# HTML report
python cli.py test backend --html

# Combined
python cli.py test all --coverage --html --verbose
```

## All Platforms

```bash
# Use the unified CLI on any platform
python cli.py test list
python cli.py test backend
python cli.py test all --coverage
```
