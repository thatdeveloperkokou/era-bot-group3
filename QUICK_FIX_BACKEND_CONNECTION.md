# Quick Fix: Backend Connection Error

## The Error
```
Cannot connect to backend server. Please check if the backend is running at https://era-bot-group3-production.up.railway.app/api.
```

## Most Likely Cause
The `REACT_APP_API_URL` environment variable is **NOT SET** in Vercel, so the frontend is trying to use the default `http://localhost:5000/api` which doesn't work in production.

## ✅ Quick Fix (2 minutes)

### Step 1: Set Environment Variable in Vercel

1. **Go to Vercel Dashboard:**
   - Visit: https://vercel.com/dashboard
   - Select your project

2. **Add Environment Variable:**
   - Click **Settings** → **Environment Variables**
   - Click **Add New**
   - Enter:
     - **Key:** `REACT_APP_API_URL`
     - **Value:** `https://era-bot-group3-production.up.railway.app/api`
     - **Environment:** Select **Production** (and Preview/Development if you want)
   - Click **Save**

3. **Redeploy:**
   - Go to **Deployments** tab
   - Find the latest deployment
   - Click the three dots (⋯) → **Redeploy**
   - Wait for deployment to complete (1-2 minutes)

### Step 2: Verify Backend is Running

1. **Test Backend Directly:**
   - Open in browser: `https://era-bot-group3-production.up.railway.app/api`
   - You should see JSON response like: `{"status": "API is running", ...}`
   - If you see an error, your backend is down - check Railway

2. **Check Railway:**
   - Go to https://railway.app
   - Check if your backend service is running
   - Check the logs for any errors

### Step 3: Fix CORS (If Still Not Working)

If you still get errors after setting the environment variable, it might be a CORS issue:

1. **Get Your Vercel Frontend URL:**
   - It should be something like: `https://era-bot-group3-xxxxx.vercel.app`
   - Check your Vercel dashboard for the exact URL

2. **Set FRONTEND_URL in Railway:**
   - Go to Railway Dashboard
   - Select your backend service
   - Go to **Variables** tab
   - Add/Update:
     - **Key:** `FRONTEND_URL`
     - **Value:** Your Vercel frontend URL (e.g., `https://era-bot-group3-xxxxx.vercel.app`)
     - **Important:** No trailing slash, no `/api`
   - Railway will auto-redeploy

## 🔍 How to Verify It's Fixed

1. **Check Browser Console:**
   - Open your deployed site
   - Press F12 → Console tab
   - Try to sign up
   - Look for the error message
   - It should now show the correct backend URL

2. **Check Network Tab:**
   - F12 → Network tab
   - Try to sign up
   - Look for requests to `/api/register`
   - Check if the request URL is correct

## ⚠️ Common Mistakes

- ❌ Setting `REACT_APP_API_URL` to `https://era-bot-group3-production.up.railway.app` (missing `/api`)
- ❌ Setting it to `http://` instead of `https://`
- ❌ Not redeploying after setting the variable
- ❌ Setting it only for Development, not Production
- ❌ Setting `FRONTEND_URL` in Railway with `/api` at the end

## ✅ Correct Configuration

**In Vercel:**
```
REACT_APP_API_URL = https://era-bot-group3-production.up.railway.app/api
```

**In Railway:**
```
FRONTEND_URL = https://your-vercel-app.vercel.app
```

## Still Not Working?

1. **Check Vercel Build Logs:**
   - Go to Deployments → Latest deployment → Build Logs
   - Look for any errors during build

2. **Check Browser Console:**
   - Look for the actual error message
   - Check what URL it's trying to connect to

3. **Test Backend Manually:**
   - Try: `https://era-bot-group3-production.up.railway.app/api/register`
   - Should return an error (method not allowed for GET), but proves backend is running

4. **Check Railway Logs:**
   - Look for CORS errors
   - Check if backend is receiving requests

