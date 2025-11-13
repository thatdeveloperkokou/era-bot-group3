# Frontend Connection Issue Fix

## The Problem
Error: `Cannot connect to backend server. Please check if the backend is running at https://era-bot-group3-production.up.railway.app/api`

The backend URL is working, but the frontend can't connect to it.

## Common Causes

### 1. REACT_APP_API_URL Not Set in Vercel

**Fix:**
1. Go to your Vercel project dashboard
2. Go to **Settings** → **Environment Variables**
3. Add a new variable:
   - **Key:** `REACT_APP_API_URL`
   - **Value:** `https://era-bot-group3-production.up.railway.app/api`
   - **Important:** Make sure it ends with `/api`
4. **Redeploy** your frontend (Vercel should auto-redeploy, or trigger manually)

### 2. CORS Issue - Backend Not Allowing Frontend Domain

**Fix:**
1. Go to your Railway backend service
2. Go to **Variables** tab
3. Add or update:
   - **Key:** `FRONTEND_URL`
   - **Value:** Your Vercel frontend URL (e.g., `https://your-app.vercel.app`)
   - **Important:** Don't include `/api` or trailing slash
4. **Redeploy** your backend

### 3. Wrong API URL Format

**Check:**
- The `REACT_APP_API_URL` should be: `https://era-bot-group3-production.up.railway.app/api`
- Make sure it includes `/api` at the end
- Make sure it uses `https://` not `http://`

## Step-by-Step Fix

### Step 1: Verify Backend is Working
1. Open: `https://era-bot-group3-production.up.railway.app`
2. You should see a JSON response with API status
3. If this works, your backend is running ✅

### Step 2: Set REACT_APP_API_URL in Vercel
1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Go to **Settings** → **Environment Variables**
4. Check if `REACT_APP_API_URL` exists
5. If not, add it:
   ```
   Key: REACT_APP_API_URL
   Value: https://era-bot-group3-production.up.railway.app/api
   ```
6. Make sure it's set for **Production** environment
7. **Redeploy** (go to Deployments → Redeploy)

### Step 3: Set FRONTEND_URL in Railway
1. Go to [Railway Dashboard](https://railway.app)
2. Select your backend service
3. Go to **Variables** tab
4. Add or update:
   ```
   Key: FRONTEND_URL
   Value: https://your-vercel-app.vercel.app
   ```
   (Replace with your actual Vercel frontend URL)
5. **Redeploy** your backend

### Step 4: Test
1. Wait for both deployments to complete
2. Open your Vercel frontend URL
3. Try to register/login
4. Check browser console (F12) for any errors
5. Check Network tab to see if API calls are being made

## Debugging

### Check Browser Console
1. Open your frontend in browser
2. Press F12 to open Developer Tools
3. Go to **Console** tab
4. Look for error messages
5. Go to **Network** tab
6. Try to register/login
7. Check if API requests are being made
8. Check the request URL and response

### Check Vercel Build Logs
1. Go to Vercel → Your Project → Deployments
2. Click on the latest deployment
3. Check the build logs
4. Look for `REACT_APP_API_URL` in the logs
5. Verify it's set correctly

### Check Railway Logs
1. Go to Railway → Your Backend Service
2. Check the logs
3. Look for CORS errors
4. Look for incoming requests from your frontend

## Quick Checklist

- [ ] `REACT_APP_API_URL` is set in Vercel environment variables
- [ ] `REACT_APP_API_URL` value is: `https://era-bot-group3-production.up.railway.app/api`
- [ ] `FRONTEND_URL` is set in Railway environment variables
- [ ] `FRONTEND_URL` value is your Vercel frontend URL (without `/api`)
- [ ] Both services have been redeployed after setting variables
- [ ] Backend is accessible at: `https://era-bot-group3-production.up.railway.app`
- [ ] Frontend is accessible at your Vercel URL

## Still Not Working?

1. **Check browser console** for specific error messages
2. **Check Network tab** to see what URL is being called
3. **Verify the backend URL** works by visiting it directly
4. **Check CORS errors** in browser console - they'll show if it's a CORS issue
5. **Try clearing browser cache** and hard refresh (Ctrl+Shift+R)

## Common Error Messages

### "Network Error" or "No response from server"
- Backend might be down
- Wrong API URL
- CORS blocking the request

### "CORS policy" error
- `FRONTEND_URL` not set in Railway
- Wrong frontend URL in `FRONTEND_URL`
- Backend needs to be redeployed

### "404 Not Found"
- API URL might be wrong (missing `/api`)
- Backend route doesn't exist

