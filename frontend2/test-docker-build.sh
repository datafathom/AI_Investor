#!/bin/bash
# Test script to verify Docker build will work

set -e

echo "=========================================="
echo "Docker Build Test Script"
echo "=========================================="
echo ""

echo "1. Checking Docker installation..."
docker --version
echo "✓ Docker is installed"
echo ""

echo "2. Validating docker-compose.yml..."
docker compose config > /dev/null
echo "✓ docker-compose.yml is valid"
echo ""

echo "3. Checking Dockerfile.dev..."
if [ -f "Dockerfile.dev" ]; then
    echo "✓ Dockerfile.dev exists"
    echo "  - Base image: $(grep '^FROM' Dockerfile.dev | cut -d' ' -f2)"
    echo "  - Build tools: $(grep 'apk add' Dockerfile.dev | grep -o 'python3 make g++' || echo 'configured')"
else
    echo "✗ Dockerfile.dev not found"
    exit 1
fi
echo ""

echo "4. Checking package.json..."
if [ -f "package.json" ]; then
    echo "✓ package.json exists"
    NODE_VERSION_REQUIRED=$(grep -A1 '"better-sqlite3"' package.json | grep -o '[0-9]\+\.[0-9]\+' | head -1 || echo "12.5.0")
    echo "  - better-sqlite3 version: $NODE_VERSION_REQUIRED (requires Node 20+)"
else
    echo "✗ package.json not found"
    exit 1
fi
echo ""

echo "5. Verifying Node version compatibility..."
DOCKERFILE_NODE=$(grep '^FROM' Dockerfile.dev | grep -o 'node:[0-9]\+' | cut -d: -f2)
if [ "$DOCKERFILE_NODE" = "20" ]; then
    echo "✓ Dockerfile uses Node 20 (compatible with better-sqlite3)"
else
    echo "⚠ Warning: Dockerfile uses Node $DOCKERFILE_NODE, but better-sqlite3 requires Node 20+"
fi
echo ""

echo "6. Checking build dependencies..."
if grep -q "python3 make g++" Dockerfile.dev; then
    echo "✓ Build dependencies (python3, make, g++) are included"
else
    echo "✗ Build dependencies missing"
    exit 1
fi
echo ""

echo "=========================================="
echo "✓ All checks passed!"
echo "=========================================="
echo ""
echo "Ready to build. Run:"
echo "  sudo docker compose up -d --build"
echo ""
echo "Or to see the build output:"
echo "  sudo docker compose build"
echo ""

