#!/bin/bash
# Frontend Verification Script
# Verifies the frontend is properly set up and working

set -e

echo "🔍 Frontend Verification Script"
echo "================================"
echo ""

cd frontend2

# Check Node.js version
echo "1. Checking Node.js version..."
NODE_VERSION=$(node -v)
echo "   ✅ Node.js: $NODE_VERSION"
if ! node -v | grep -qE "v(18|19|20|21|22)"; then
    echo "   ⚠️  Warning: Node.js 18+ recommended"
fi

# Check if dependencies are installed
echo ""
echo "2. Checking dependencies..."
if [ ! -d "node_modules" ]; then
    echo "   ⚠️  node_modules not found. Installing..."
    npm install --legacy-peer-deps
else
    echo "   ✅ node_modules exists"
fi

# Check package.json scripts
echo ""
echo "3. Checking package.json scripts..."
if grep -q '"dev"' package.json; then
    echo "   ✅ dev script found"
else
    echo "   ❌ dev script not found"
    exit 1
fi

# Check for main entry point
echo ""
echo "4. Checking entry points..."
if [ -f "src/main.jsx" ] || [ -f "src/main.js" ] || [ -f "src/index.jsx" ] || [ -f "src/index.js" ]; then
    echo "   ✅ Entry point found"
else
    echo "   ❌ Entry point not found"
    exit 1
fi

# Check for App component
echo ""
echo "5. Checking App component..."
if [ -f "src/App.jsx" ] || [ -f "src/App.js" ]; then
    echo "   ✅ App component found"
else
    echo "   ❌ App component not found"
    exit 1
fi

# Check vite config
echo ""
echo "6. Checking Vite configuration..."
if [ -f "vite.config.js" ]; then
    echo "   ✅ vite.config.js found"
else
    echo "   ⚠️  vite.config.js not found"
fi

# Try to build (quick syntax check)
echo ""
echo "7. Running build check..."
if npm run build 2>&1 | grep -q "error"; then
    echo "   ❌ Build has errors"
    npm run build
    exit 1
else
    echo "   ✅ Build successful"
fi

# Check if dist was created
if [ -d "dist" ]; then
    echo "   ✅ dist directory created"
else
    echo "   ⚠️  dist directory not found after build"
fi

echo ""
echo "================================"
echo "✅ Frontend verification complete!"
echo ""
echo "Next steps:"
echo "1. Start dev server: npm run dev"
echo "2. Open http://localhost:3000"
echo "3. Check browser console for errors"
echo "4. Test navigation and key features"
