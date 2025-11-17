# Fix CORS Issue - Quick Steps

## The Problem
Your frontend is correctly configured and trying to connect to:
- ✅ `https://era-bot-group3-production.up.railway.app/api`
- ✅ Environment variable is set correctly

But you're getting "No response from server" - this is a **CORS issue**.

## ✅ Quick Fix (2 minutes)

### Step 1: Get Your Vercel Frontend URL
1. Go to your Vercel Dashboard
2. Your frontend URL should be something like: `https://era-bot-group3-xxxxx.vercel.app`
3. Copy the full URL (without trailing slash)

### Step 2: Set FRONTEND_URL in Railway
1. Go to [Railway Dashboard](https://railway.app)
2. Click on your **backend service** (the one running the API, not the database)
3. Go to **Variables** tab
4. Look for `FRONTEND_URL`:
   - **If it doesn't exist:** Click **"New Variable"**
   - **If it exists:** Click to edit it
5. Set the value:
   - **Key:** `FRONTEND_URL`
   - **Value:** Your Vercel frontend URL (e.g., `https://era-bot-group3-xxxxx.vercel.app`)
   - **Important:**
     - Use `https://` (not `http://`)
     - No trailing slash
     - No `/api` at the end
     - Just the base URL
6. Click **Save** or **Add**

### Step 3: Wait for Redeploy
- Railway will automatically redeploy when you add/update the variable
- Wait 1-2 minutes for deployment to complete
- You can check the **Deployments** tab to see progress

### Step 4: Verify It's Working
1. Check Railway logs:
   - Go to Railway → Your Backend Service → **Deployments** → Latest
   - Look for: `🌐 CORS: Allowing origins: ['https://your-vercel-url.vercel.app']`
   - This confirms CORS is configured correctly

2. Test your frontend:
   - Go to your Vercel frontend
   - Try to sign up
   - It should work now! ✅

## Alternative: Allow All Origins (Temporary Fix)

If you want to allow all origins temporarily (for testing), you can:

1. In Railway → Backend Service → Variables
2. **Delete** or **set** `FRONTEND_URL` to `*`
3. Redeploy

**Note:** This is less secure but useful for testing. For production, use the specific frontend URL.

## Still Not Working?

1. **Check Railway Logs:**
   - Look for CORS-related errors
   - Check if the backend is receiving requests

2. **Check Browser Network Tab:**
   - F12 → Network tab
   - Try to sign up
   - Look for the request to `/api/register`
   - Check the response headers for CORS errors

3. **Verify Frontend URL:**
   - Make sure the `FRONTEND_URL` in Railway matches your exact Vercel URL
   - Check for typos or extra characters

