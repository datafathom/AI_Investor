# CI/CD Pipeline Guide

This guide explains the Continuous Integration and Continuous Deployment pipelines for the AI Investor platform.

## Overview

The CI/CD pipeline is implemented using GitHub Actions and includes:

- **Continuous Integration (CI)**: Automated testing, linting, and security scanning on every push/PR
- **Continuous Deployment (CD)**: Automated deployment to staging and production environments

## Workflows

### 1. CI Pipeline (`ci.yml`)

Runs on every push and pull request to `main`, `develop`, or `staging` branches.

**Jobs**:
- **Backend Tests**: Unit tests, linting, code coverage
- **Frontend Tests**: Unit tests, linting, build verification
- **Security Scan**: Dependency and code security scanning
- **Docker Build Test**: Verifies Docker images build successfully
- **Integration Tests**: End-to-end integration testing

**Triggers**:
- Push to `main`, `develop`, `staging`
- Pull requests to `main`, `develop`, `staging`

### 2. Production Deployment (`production-deploy.yml`)

Deploys to production environment when code is pushed to `main` branch.

**Jobs**:
- **Pre-deployment Checks**: Validates environment and secrets
- **Build and Push**: Builds and pushes Docker images to registry
- **Run Migrations**: Executes database migrations
- **Deploy to Production**: Deploys to production server
- **Rollback**: Automatically rolls back on failure

**Triggers**:
- Push to `main` branch
- Manual workflow dispatch

**Approval Required**: Yes (via GitHub Environments)

### 3. Staging Deployment (`staging-deploy.yml`)

Deploys to staging environment automatically.

**Jobs**:
- **Run Tests**: Executes test suite
- **Deploy to Staging**: Deploys to staging server

**Triggers**:
- Push to `staging` or `develop` branch
- Manual workflow dispatch

### 4. Security Scan (`security-scan.yml`)

Comprehensive security scanning.

**Jobs**:
- **Dependency Scan**: Checks for vulnerable dependencies
- **Code Scan**: CodeQL analysis, Bandit, ESLint security
- **Container Scan**: Trivy scanning of Docker images
- **Secret Scan**: Gitleaks and TruffleHog

**Triggers**:
- Push to `main`, `develop`
- Pull requests
- Daily schedule (2 AM UTC)

### 5. Performance Tests (`performance-tests.yml`)

Performance and load testing.

**Jobs**:
- **Load Test**: k6 load testing
- **API Benchmarks**: Performance benchmarks for API endpoints
- **Frontend Performance**: Bundle size analysis, Lighthouse CI

**Triggers**:
- Push to `main`
- Pull requests
- Weekly schedule (Monday 3 AM UTC)
- Manual dispatch

## Setup Instructions

### 1. GitHub Secrets

Configure the following secrets in GitHub repository settings:

**Required Secrets**:
- `POSTGRES_HOST` - Production database host
- `POSTGRES_PORT` - Production database port
- `POSTGRES_USER` - Production database user
- `POSTGRES_PASSWORD` - Production database password
- `POSTGRES_DB` - Production database name
- `DOMAIN` - Production domain name
- `PRODUCTION_HOST` - Production server hostname/IP
- `PRODUCTION_USER` - SSH user for production server
- `PRODUCTION_SSH_KEY` - SSH private key for production server
- `STAGING_HOST` - Staging server hostname/IP
- `STAGING_USER` - SSH user for staging server
- `STAGING_SSH_KEY` - SSH private key for staging server
- `SLACK_WEBHOOK_URL` - Slack webhook for notifications (optional)
- `BACKEND_URL` - Backend API URL for frontend builds

### 2. GitHub Environments

Create environments in GitHub repository settings:

1. **staging**
   - No protection rules required
   - Add staging-specific secrets

2. **production**
   - Required reviewers: Add team members who can approve deployments
   - Deployment branches: Only `main` branch
   - Add production-specific secrets

### 3. Container Registry

The pipeline uses GitHub Container Registry (ghcr.io). Images are automatically pushed to:
- `ghcr.io/[owner]/[repo]-backend:latest`
- `ghcr.io/[owner]/[repo]-frontend:latest`

### 4. Code Coverage

Code coverage is uploaded to Codecov. Set up Codecov integration:
1. Sign up at https://codecov.io
2. Connect your GitHub repository
3. Add `CODECOV_TOKEN` secret (optional, auto-detected)

## Usage

### Running CI Locally

```bash
# Install act (GitHub Actions runner)
brew install act  # macOS
# or download from https://github.com/nektos/act

# Run CI workflow
act push
```

### Manual Deployment

1. Go to GitHub Actions tab
2. Select "Production Deployment" workflow
3. Click "Run workflow"
4. Select environment and branch
5. Click "Run workflow"

### Viewing Results

- **CI Results**: GitHub Actions tab → Workflow runs
- **Security Alerts**: Security tab → Code scanning alerts
- **Coverage Reports**: Codecov dashboard
- **Performance Results**: GitHub Actions artifacts

## Troubleshooting

### CI Fails on Tests

1. Check test logs in GitHub Actions
2. Run tests locally: `pytest tests/`
3. Verify environment variables are set correctly

### Deployment Fails

1. Check deployment logs in GitHub Actions
2. Verify SSH keys are configured correctly
3. Check server connectivity
4. Verify environment variables in GitHub secrets

### Security Scan Finds Issues

1. Review security alerts in GitHub Security tab
2. Update vulnerable dependencies
3. Fix code security issues
4. Re-run security scan

## Best Practices

1. **Always run CI locally before pushing**
2. **Review security alerts immediately**
3. **Test in staging before production**
4. **Monitor deployment health checks**
5. **Keep dependencies updated**
6. **Review performance benchmarks regularly**

## Next Steps

- [ ] Set up GitHub Environments
- [ ] Configure GitHub Secrets
- [ ] Test CI pipeline with a test PR
- [ ] Set up Codecov integration
- [ ] Configure Slack notifications
- [ ] Test staging deployment
- [ ] Test production deployment (with approval)
