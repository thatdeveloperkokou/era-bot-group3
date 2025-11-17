# Deployment Checklist - Fix Backend Connection & Mapbox Issues

## Issue 1: Backend Connection Error on Deployed Site

### Problem
Error: "Cannot connect to backend server. Please check if the backend is running at https://era-bot-group3-production.up.railway.app/api"

### Solution Steps

#### Step 1: Set Environment Variable in Vercel
1. Go to your [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Go to **Settings** → **Environment Variables**
4. Check if `REACT_APP_API_URL` exists
5. If not, or if it's incorrect, add/update it:
   - **Key:** `REACT_APP_API_URL`
   - **Value:** `https://era-bot-group3-production.up.railway.app/api`
   - **Important:** 
     - Must include `/api` at the end
     - Must use `https://` not `http://`
     - Select **Production** environment (and Preview/Development if needed)
6. **Redeploy** your frontend:
   - Go to **Deployments** tab
   - Click the three dots (⋯) on the latest deployment
   - Click **Redeploy**

#### Step 2: Verify Backend CORS Settings
1. Go to your [Railway Dashboard](https://railway.app)
2. Select your backend service
3. Go to **Variables** tab
4. Check if `FRONTEND_URL` is set
5. Set it to your Vercel frontend URL:
   - **Key:** `FRONTEND_URL`
   - **Value:** `https://your-vercel-app.vercel.app`
   - **Important:** 
     - Use your actual Vercel frontend URL (without `/api` or trailing slash)
     - Don't include `localhost` URLs
6. **Redeploy** your backend if you made changes

#### Step 3: Test Backend Connection
1. Open your browser's Developer Tools (F12)
2. Go to **Console** tab
3. Try to sign up again
4. Check for any CORS errors or network errors
5. The error message should now show the correct backend URL

---

## Issue 2: Mapbox Not Displaying Addresses

### Problem
- Mapbox not showing any address suggestions
- Only recognizing cities and towns, not streets

### Solution Steps

#### Step 1: Set Mapbox Token in Vercel
1. Go to your [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Go to **Settings** → **Environment Variables**
4. Check if `REACT_APP_MAPBOX_ACCESS_TOKEN` exists
5. If not, add it:
   - **Key:** `REACT_APP_MAPBOX_ACCESS_TOKEN`
   - **Value:** Your Mapbox public token (starts with `pk.`)
   - **How to get a token:**
     1. Go to [Mapbox Account](https://account.mapbox.com/)
     2. Go to **Access Tokens**
     3. Copy your **Default Public Token** (or create a new one)
     4. Make sure it has **Geocoding API** permissions
   - Select **Production** environment (and Preview/Development if needed)
6. **Redeploy** your frontend

#### Step 2: Verify Mapbox Token Format
- Token should start with `pk.` (public token)
- Should NOT start with `sk.` (secret token)
- Should have geocoding permissions enabled

#### Step 3: Test Mapbox Search
1. After redeploying, go to the signup page
2. Start typing a location in Nigeria
3. Try typing:
   - City names: "Lagos", "Abuja", "Port Harcourt"
   - Street names: "Victoria Island", "Lekki", "Ikeja"
   - Full addresses: "Allen Avenue, Ikeja, Lagos"
4. You should now see street-level addresses appearing in the suggestions

---

## Code Changes Made

### Mapbox Improvements
1. ✅ Updated search types to prioritize `address` and `poi` (points of interest)
2. ✅ Added result sorting to prioritize street addresses over cities
3. ✅ Increased search result limit from 5 to 8 for better coverage
4. ✅ Added support for `district` and `postcode` types for better street-level results

### Backend Connection
- The code already handles the API URL correctly
- The issue is purely configuration (environment variables)

---

## Quick Verification Checklist

After making the changes above, verify:

- [ ] `REACT_APP_API_URL` is set in Vercel to: `https://era-bot-group3-production.up.railway.app/api`
- [ ] `REACT_APP_MAPBOX_ACCESS_TOKEN` is set in Vercel with a valid Mapbox token
- [ ] `FRONTEND_URL` is set in Railway to your Vercel frontend URL
- [ ] Both frontend and backend have been redeployed after setting environment variables
- [ ] Backend is accessible at: `https://era-bot-group3-production.up.railway.app/api`
- [ ] Signup form can connect to backend (no connection errors)
- [ ] Location autocomplete shows street addresses, not just cities

---

## Troubleshooting

### Still seeing backend connection error?
1. Check browser console for the actual error
2. Verify the backend URL is correct: `https://era-bot-group3-production.up.railway.app/api`
3. Test the backend directly in browser: Open `https://era-bot-group3-production.up.railway.app/api` - should show JSON response
4. Check CORS errors in browser console - if present, update `FRONTEND_URL` in Railway

### Mapbox still not working?
1. Check browser console for Mapbox API errors
2. Verify token is set correctly in Vercel
3. Check Mapbox account to ensure token is active and has geocoding permissions
4. Try a simple test: Type "Lagos" - should show multiple results including streets

### Need help?
- Check the error messages in browser console (F12 → Console tab)
- Verify all environment variables are set correctly
- Make sure you redeployed after setting environment variables

