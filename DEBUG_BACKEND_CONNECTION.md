# Debug: Backend Connection Issue

## ✅ What's Working
- Backend is running: `https://era-bot-group3-production.up.railway.app/api` responds with `{"status":"ok"}`
- Environment variable is set in Vercel: `REACT_APP_API_URL`

## 🔍 Next Steps to Debug

### Step 1: Verify Frontend Was Redeployed
**Important:** After setting an environment variable in Vercel, you MUST redeploy!

1. Go to Vercel Dashboard → Your Project → **Deployments**
2. Check the latest deployment timestamp
3. If it was deployed BEFORE you set the environment variable, you need to redeploy:
   - Click the three dots (⋯) on the latest deployment
   - Click **Redeploy**
   - Wait for it to complete (1-2 minutes)

### Step 2: Check Browser Console
1. Open your deployed frontend site
2. Press **F12** to open Developer Tools
3. Go to **Console** tab
4. Try to sign up
5. Look for these messages:
   - `REACT_APP_API_URL env var: NOT SET - This is the problem!` ← If you see this, the env var isn't being used
   - `REACT_APP_API_URL env var: https://era-bot-group3-production.up.railway.app/api` ← This is correct
   - `Attempted to connect to: http://localhost:5000/api` ← Wrong! Means env var not set
   - `Attempted to connect to: https://era-bot-group3-production.up.railway.app/api` ← Correct!

### Step 3: Check Network Tab
1. In Developer Tools, go to **Network** tab
2. Try to sign up
3. Look for a request to `/api/register` or `/api/login`
4. Check:
   - **Request URL**: Should be `https://era-bot-group3-production.up.railway.app/api/register`
   - **Status**: 
     - `200` = Success! ✅
     - `CORS error` = Need to set FRONTEND_URL in Railway
     - `Failed` or `Network Error` = Backend might be down or URL wrong

### Step 4: Fix CORS (If Needed)
If you see CORS errors in the console:

1. **Get Your Vercel Frontend URL:**
   - It should be something like: `https://era-bot-group3-xxxxx.vercel.app`
   - Check your Vercel dashboard for the exact URL

2. **Set FRONTEND_URL in Railway:**
   - Go to Railway Dashboard
   - Select your **backend service** (not the database)
   - Go to **Variables** tab
   - Add or update:
     - **Key:** `FRONTEND_URL`
     - **Value:** Your Vercel frontend URL (e.g., `https://era-bot-group3-xxxxx.vercel.app`)
     - **Important:** 
       - No trailing slash
       - No `/api` at the end
       - Must use `https://`
   - Railway will auto-redeploy

3. **Verify CORS is Working:**
   - Check Railway logs after redeploy
   - You should see: `🌐 CORS: Allowing origins: ['https://your-vercel-url.vercel.app']`

### Step 5: Verify Environment Variable Scope
In Vercel, make sure `REACT_APP_API_URL` is set for:
- ✅ **Production** (required)
- ✅ **Preview** (optional, but recommended)
- ✅ **Development** (optional)

## Common Issues

### Issue 1: "REACT_APP_API_URL env var: NOT SET"
**Solution:** 
- The environment variable isn't being picked up
- Make sure you redeployed AFTER setting it
- Check that it's set for the correct environment (Production)

### Issue 2: CORS Error
**Error looks like:**
```
Access to XMLHttpRequest at 'https://era-bot-group3-production.up.railway.app/api/register' 
from origin 'https://your-app.vercel.app' has been blocked by CORS policy
```

**Solution:**
- Set `FRONTEND_URL` in Railway to your Vercel frontend URL
- Redeploy backend

### Issue 3: Still Connecting to localhost
**If you see:** `Attempted to connect to: http://localhost:5000/api`

**Solution:**
- Environment variable not set correctly
- Frontend not redeployed after setting variable
- Check Vercel build logs to see if env var is being used

## Quick Test

1. Open browser console (F12)
2. Type: `console.log(process.env.REACT_APP_API_URL)`
3. If it shows `undefined`, the env var isn't set
4. If it shows the Railway URL, it's set correctly

**Note:** In production builds, `process.env` values are replaced at build time, so you might not see them in console. Check the Network tab instead to see what URL is being called.

