# Frontend Verification Guide

Quick guide to verify the frontend is fully working.

## Quick Start

### 1. Navigate to Frontend Directory

```bash
cd frontend2
```

### 2. Install Dependencies (if needed)

```bash
npm install --legacy-peer-deps
```

### 3. Start Development Server

```bash
npm run dev
```

**Expected Output:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### 4. Open Browser

Open http://localhost:5173 (or the port shown) in your browser.

---

## What to Check

### ✅ Basic Functionality

1. **App Loads**
   - [ ] Page loads without errors
   - [ ] No blank white screen
   - [ ] Console shows no critical errors (F12)

2. **Navigation**
   - [ ] Menu bar appears at top
   - [ ] Can click menu items
   - [ ] Routes dropdown works
   - [ ] Can navigate between pages

3. **Key Pages**
   - [ ] Dashboard loads (`/workspace/terminal`)
   - [ ] Mission Control loads (`/workspace/mission-control`)
   - [ ] Settings accessible
   - [ ] Legal pages accessible (`/legal/terms`, `/legal/privacy`)

4. **Components**
   - [ ] No "Component not found" errors
   - [ ] Error boundaries catch errors gracefully
   - [ ] Loading states display
   - [ ] Error messages display (if API not running)

### ✅ Browser Console Check

Open Developer Tools (F12) and check:

- **Console Tab**: No red errors
- **Network Tab**: API calls (may fail if backend not running - that's OK)
- **Elements Tab**: HTML structure renders

### ✅ Common Issues

#### Issue: Blank Page
**Check:**
- Browser console for errors
- Network tab for failed requests
- Verify `src/main.jsx` exists
- Verify `src/App.jsx` exists

#### Issue: Module Not Found
**Fix:**
```bash
npm install --legacy-peer-deps
```

#### Issue: Port Already in Use
**Fix:**
- Change port in `vite.config.js`
- Or kill process using port 5173

#### Issue: API Connection Errors
**Note:** This is normal if backend isn't running. The frontend should still load and show error messages gracefully.

---

## Testing Checklist

### Manual Testing

- [ ] **Homepage**: Loads and displays content
- [ ] **Login**: Login modal appears (if not authenticated)
- [ ] **Navigation**: All menu items work
- [ ] **Routes**: All 30+ routes accessible
- [ ] **Error Handling**: Errors display gracefully
- [ ] **Responsive**: Works on different screen sizes

### Automated Testing

```bash
# Run unit tests
npm test

# Run E2E tests (requires backend)
npm run test:e2e
```

---

## Production Build Test

### Build for Production

```bash
npm run build
```

**Expected:**
- Build completes without errors
- `dist/` directory created
- No build warnings

### Preview Production Build

```bash
npm run serve
```

**Expected:**
- Production build loads
- All routes work
- Assets load correctly

---

## Quick Verification Commands

### Windows (PowerShell)

```powershell
cd frontend2
npm install --legacy-peer-deps
npm run dev
```

### Mac/Linux

```bash
cd frontend2
npm install --legacy-peer-deps
npm run dev
```

---

## Success Criteria

✅ **Frontend is working if:**
- Dev server starts without errors
- Browser loads the app
- No critical console errors
- Navigation works
- Pages render (even if API calls fail)

---

## Next Steps After Verification

1. **Test with Backend**: Start backend and test full integration
2. **Run Tests**: Execute test suites
3. **Check All Routes**: Navigate through all 30+ routes
4. **Test Features**: Test key features (login, dashboard, etc.)
5. **Production Build**: Test production build

---

**Last Updated**: 2026-01-21
