# Verify Frontend is Working - Step by Step

## Quick Verification (5 minutes)

### Step 1: Start the Frontend

Open a terminal and run:

```bash
cd frontend2
npm run dev
```

**What to expect:**
- Server starts on http://localhost:5173 (or similar port)
- You'll see: `VITE ready in xxx ms`
- No error messages

### Step 2: Open in Browser

1. Open your browser
2. Go to: **http://localhost:5173**
3. You should see the AI Investor interface

### Step 3: Check for Errors

Press **F12** to open Developer Tools, then:

1. **Console Tab**: Should have minimal/no red errors
2. **Network Tab**: May show API errors (OK if backend not running)
3. **Elements Tab**: Should show HTML structure

### Step 4: Test Navigation

1. **Menu Bar**: Should appear at top
2. **Click "Routes"**: Dropdown should open
3. **Click any route**: Page should navigate
4. **Try multiple routes**: Should all work

### Step 5: Test Key Features

- [ ] **Dashboard loads**: `/workspace/terminal`
- [ ] **Menu works**: All menu items clickable
- [ ] **No blank pages**: All routes show content
- [ ] **Error handling**: Errors display gracefully (if API not running)

---

## What Success Looks Like

✅ **Frontend is working if:**
- Page loads (not blank)
- Menu bar visible
- Can navigate between pages
- No critical console errors
- Pages render (even if API calls fail)

---

## Common Issues

### ❌ Blank Page
**Check:** Browser console (F12) for errors

### ❌ "Module not found"
**Fix:** Run `npm install --legacy-peer-deps` in `frontend2` directory

### ❌ Port already in use
**Fix:** Change port in `vite.config.js` or kill process using port

### ⚠️ API Connection Errors
**Note:** This is NORMAL if backend isn't running. Frontend should still work and show error messages.

---

## Full Test Checklist

Once basic verification passes:

- [ ] All 30+ routes accessible
- [ ] Login modal appears (if not authenticated)
- [ ] Settings page works
- [ ] Legal pages load (`/legal/terms`, `/legal/privacy`)
- [ ] Onboarding flow works (for new users)
- [ ] Error boundaries catch errors
- [ ] Responsive design works (resize window)

---

## Next: Test with Backend

Once frontend works standalone:

1. Start backend: `python -m web.app`
2. Test API integration
3. Test full user flows
4. Run E2E tests: `npm run test:e2e`

---

**Ready to test?** Run `npm run dev` in the `frontend2` directory!
