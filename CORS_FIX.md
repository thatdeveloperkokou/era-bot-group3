# CORS Error Fix - Quick Solution

## The Error
```
XMLHttpRequest at 'https://era-bot-group3-production.up.railway.app/api/login' 
from origin 'https://era-bot-group3-nx3x.vercel.app' has been blocked by CORS policy
```

## Quick Fix (2 minutes)

### Step 1: Add FRONTEND_URL to Railway

1. Go to [Railway Dashboard](https://railway.app)
2. Click on your **backend service** (the one with the API)
3. Go to **"Variables"** tab
4. Click **"New Variable"**
5. Add:
   - **Key:** `FRONTEND_URL`
   - **Value:** `https://era-bot-group3-nx3x.vercel.app`
   - **Important:** 
     - Use `https://` (not `http://`)
     - Don't include `/api` or trailing slash
     - Just the base URL: `https://era-bot-group3-nx3x.vercel.app`
6. Click **"Add"**

### Step 2: Redeploy Backend

1. Railway should auto-redeploy when you add the variable
2. Or go to **"Deployments"** tab and click **"Redeploy"**
3. Wait for deployment to complete (1-2 minutes)

### Step 3: Test

1. Go to your Vercel frontend: `https://era-bot-group3-nx3x.vercel.app`
2. Try to login or register
3. The CORS error should be gone! ✅

## Verify It's Working

After redeploying, check the Railway logs:
1. Go to Railway → Your Backend Service
2. Click on **"Deployments"** → Latest deployment
3. Check the logs - you should see:
   ```
   🌐 CORS: Allowing origins: ['https://era-bot-group3-nx3x.vercel.app']
   ```

## If You Have Multiple Frontend URLs

If you have multiple Vercel deployments (production, preview, etc.), you can add multiple URLs separated by commas:

**In Railway Variables:**
```
FRONTEND_URL=https://era-bot-group3-nx3x.vercel.app,https://era-bot-group3-git-main.vercel.app
```

## Still Not Working?

1. **Double-check the URL:**
   - Make sure it's exactly: `https://era-bot-group3-nx3x.vercel.app`
   - No trailing slash
   - No `/api` at the end
   - Must use `https://` not `http://`

2. **Check Railway logs:**
   - Look for the CORS configuration message
   - Make sure it shows your frontend URL

3. **Clear browser cache:**
   - Hard refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

4. **Check browser console:**
   - Open DevTools (F12)
   - Look for any other errors
   - Check Network tab to see the actual request

## What Changed in Code

- Improved CORS configuration to support multiple origins
- Added explicit `allow_headers` for Authorization header
- Added logging to show which origins are allowed
- Better handling of preflight OPTIONS requests

