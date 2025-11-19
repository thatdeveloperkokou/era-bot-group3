# Deployment Walkthrough - Step by Step

Let's walk through the deployment process together. Follow each step and check it off as you complete it.

## 📋 Step 1: Generate SECRET_KEY

First, we need to generate a secure secret key for JWT tokens.

**Run this command:**
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Copy the output** - you'll need it in Step 3.

---

## 🗄️ Step 2: Verify Database Setup (Railway)

1. **Go to Railway Dashboard:**
   - Visit: https://railway.app
   - Log in to your account

2. **Check if PostgreSQL database exists:**
   - Look for a PostgreSQL service in your project
   - If it doesn't exist:
     - Click **"+ New"** → **"Database"** → **"Add PostgreSQL"**
     - Wait for it to provision (1-2 minutes)

3. **Verify DATABASE_URL is set:**
   - Click on your **backend service** (not the database)
   - Go to **"Variables"** tab
   - Look for `DATABASE_URL`
   - ✅ If it exists and starts with `postgresql://` → Good!
   - ❌ If it doesn't exist:
     - Go back to your PostgreSQL service
     - Click **"Variables"** tab
     - Copy the `DATABASE_URL` value
     - Go to your backend service → **"Variables"** → **"New Variable"**
     - Key: `DATABASE_URL`
     - Value: Paste the copied value
     - Click **"Add"**

**✅ Check this off when done:**
- [ ] PostgreSQL database exists
- [ ] DATABASE_URL is set in backend service

---

## 🔧 Step 3: Set Backend Environment Variables (Railway)

1. **Go to Railway Dashboard:**
   - Click on your **backend service**

2. **Go to "Variables" tab**

3. **Add/Update these variables one by one:**

   **a) SECRET_KEY:**
   - Key: `SECRET_KEY`
   - Value: Paste the secret key you generated in Step 1
   - Click **"Add"** or **"Update"**

   **b) FRONTEND_URL:**
   - Key: `FRONTEND_URL`
   - Value: Your Vercel frontend URL (e.g., `https://era-bot-group3-xxxxx.vercel.app`)
   - **Important:** 
     - No trailing slash
     - No `/api` at the end
     - Just the base URL
   - If you don't know your Vercel URL yet, we'll set this later
   - For now, you can set it to `*` (allows all origins - we'll fix this later)

   **c) MAIL_SUPPRESS_SEND (Optional - if email not configured):**
   - Key: `MAIL_SUPPRESS_SEND`
   - Value: `true`
   - This prevents email errors if email isn't set up yet

4. **After adding variables, Railway will auto-redeploy**
   - Wait for deployment to complete (check the **"Deployments"** tab)

**✅ Check this off when done:**
- [ ] SECRET_KEY is set (not the default value!)
- [ ] FRONTEND_URL is set (or set to `*` temporarily)
- [ ] MAIL_SUPPRESS_SEND is set to `true` (if email not configured)
- [ ] Backend has redeployed successfully

---

## 🌐 Step 4: Get Your Vercel Frontend URL

1. **Go to Vercel Dashboard:**
   - Visit: https://vercel.com/dashboard
   - Log in to your account

2. **Find your project:**
   - Click on your frontend project

3. **Get the URL:**
   - Look at the top of the page or in the **"Domains"** section
   - Your URL will be something like: `https://era-bot-group3-xxxxx.vercel.app`
   - **Copy this URL** - you'll need it for the next steps

**✅ Check this off when done:**
- [ ] I have my Vercel frontend URL: `https://____________________.vercel.app`

---

## ⚙️ Step 5: Set Frontend Environment Variables (Vercel)

1. **In Vercel Dashboard:**
   - Click on your frontend project
   - Go to **"Settings"** → **"Environment Variables"**

2. **Add/Update these variables:**

   **a) REACT_APP_API_URL:**
   - Click **"Add New"**
   - Key: `REACT_APP_API_URL`
   - Value: `https://era-bot-group3-production.up.railway.app/api`
   - **CRITICAL:** Must include `/api` at the end!
   - Environment: Select **Production** (and Preview/Development if you want)
   - Click **"Save"**

   **b) REACT_APP_MAPBOX_ACCESS_TOKEN:**
   - Click **"Add New"**
   - Key: `REACT_APP_MAPBOX_ACCESS_TOKEN`
   - Value: Your Mapbox token (starts with `pk.`)
   - If you don't have one:
     - Go to https://account.mapbox.com/
     - Go to **"Access Tokens"**
     - Copy your **Default Public Token** (or create a new one)
   - Environment: Select **Production** (and Preview/Development if you want)
   - Click **"Save"**

3. **Redeploy Frontend:**
   - Go to **"Deployments"** tab
   - Click the three dots (⋯) on the latest deployment
   - Click **"Redeploy"**
   - Wait for deployment to complete (1-2 minutes)

**✅ Check this off when done:**
- [ ] REACT_APP_API_URL is set to `https://era-bot-group3-production.up.railway.app/api`
- [ ] REACT_APP_MAPBOX_ACCESS_TOKEN is set
- [ ] Frontend has been redeployed

---

## 🔄 Step 6: Update FRONTEND_URL in Railway (If Needed)

1. **Go back to Railway:**
   - Backend service → **"Variables"** tab

2. **Update FRONTEND_URL:**
   - If you set it to `*` earlier, now update it:
   - Key: `FRONTEND_URL`
   - Value: Your actual Vercel URL (from Step 4)
   - Example: `https://era-bot-group3-xxxxx.vercel.app`
   - **Important:** No trailing slash, no `/api`
   - Click **"Update"**

3. **Wait for redeploy** (Railway will auto-redeploy)

**✅ Check this off when done:**
- [ ] FRONTEND_URL is set to your actual Vercel URL
- [ ] Backend has redeployed

---

## 🗃️ Step 7: Seed Region Profiles

We need to populate the database with region profile data.

**Option A: Run locally (if you have database access)**
```bash
cd backend
python region_profiles_seed.py
```

**Option B: Run in Railway (Recommended)**
1. **Go to Railway Dashboard:**
   - Click on your backend service
   - Go to **"Deployments"** tab
   - Click on the latest deployment
   - Click **"View Logs"**

2. **Check if region profiles are already seeded:**
   - Look for messages about region profiles
   - Or test the endpoint (see Step 8)

**Option C: Use Railway CLI (if installed)**
```bash
railway run python backend/region_profiles_seed.py
```

**✅ Check this off when done:**
- [ ] Region profiles are seeded (we'll verify in next step)

---

## 🧪 Step 8: Test Backend Endpoints

Let's verify everything is working:

1. **Test Health Endpoint:**
   - Open in browser: `https://era-bot-group3-production.up.railway.app/api`
   - Should see JSON response: `{"status": "ok", ...}`
   - ✅ If you see this → Backend is running!

2. **Test Region Profiles:**
   - Open in browser: `https://era-bot-group3-production.up.railway.app/api/region-profiles`
   - Should see JSON with `"regions"` array
   - Should have 11 regions (all Nigerian DisCos)
   - ✅ If you see 11 regions → Database is seeded!

**✅ Check this off when done:**
- [ ] Health endpoint returns `{"status": "ok"}`
- [ ] Region profiles endpoint returns 11 regions

---

## ⏰ Step 9: Set Up Scheduler (Auto-Logger)

Choose one option:

### Option A: Separate Scheduler Service (Recommended)

1. **Create New Service in Railway:**
   - In Railway project, click **"+ New"** → **"Empty Service"**
   - Name it: `scheduler` or `auto-logger`

2. **Connect to Same Repository:**
   - Click **"Connect GitHub"** or **"Deploy from GitHub repo"**
   - Select the same repository as your backend

3. **Set Start Command:**
   - Go to **"Settings"** tab
   - Find **"Start Command"** field
   - Set to: `python backend/scheduler_runner.py`
   - Click **"Save"**

4. **Link Database:**
   - Go to **"Variables"** tab
   - Click **"New Variable"**
   - Key: `DATABASE_URL`
   - Value: Copy from your backend service's `DATABASE_URL`
   - Click **"Add"**

5. **Copy Other Environment Variables:**
   - Copy `SECRET_KEY` from backend service
   - Add it to scheduler service

6. **Deploy:**
   - Railway will auto-deploy
   - Check **"Deployments"** tab to verify it's running

### Option B: Railway Cron (Alternative)

1. **In Railway Dashboard:**
   - Click **"+ New"** → **"Cron"** (if available)
   - Or go to backend service → **"Settings"** → **"Cron Jobs"**

2. **Configure Cron:**
   - Name: `auto-logger`
   - Schedule: `0 * * * *` (runs every hour)
   - Command: `python backend/auto_logger.py`
   - Service: Select your backend service

3. **Save and deploy**

**✅ Check this off when done:**
- [ ] Scheduler service is created and running
- [ ] OR Cron job is configured
- [ ] Check logs to verify it's executing

---

## 🧪 Step 10: Test Frontend Connection

1. **Open your Vercel frontend:**
   - Go to your Vercel URL (from Step 4)

2. **Open Browser Console:**
   - Press `F12` or right-click → **"Inspect"**
   - Go to **"Console"** tab

3. **Try to Register:**
   - Go to signup page
   - Fill in the form
   - Try to register

4. **Check for Errors:**
   - ✅ If registration works → Everything is connected!
   - ❌ If you see errors:
     - Check the error message
     - Verify environment variables are set correctly
     - Check Railway logs for backend errors

**✅ Check this off when done:**
- [ ] Frontend loads without errors
- [ ] Can register a new user
- [ ] No CORS errors in console

---

## 📊 Step 11: Verify Auto-Logging (After 1 Hour)

The scheduler runs every hour. To verify it's working:

1. **Register a test user** (if you haven't already)
   - Use a location in Nigeria (e.g., "Lekki, Lagos")

2. **Wait for next hour** (or check logs immediately)

3. **Check Railway Logs:**
   - Go to scheduler service → **"Deployments"** → **"View Logs"**
   - Look for: `Auto logger processed 11 regions and queued X events`
   - ✅ If you see this → Scheduler is working!

4. **Check Database:**
   - Log in to your test user
   - Go to dashboard
   - Should see power logs appearing automatically
   - Check timestamps - they should align with hourly schedule

**✅ Check this off when done:**
- [ ] Scheduler logs show execution messages
- [ ] Auto-generated power logs appear in dashboard
- [ ] Logs have `auto_generated=True` in database

---

## 🎉 Step 12: Final Verification

Run through this checklist:

- [ ] Backend is running and accessible
- [ ] Frontend connects to backend (no connection errors)
- [ ] User registration works
- [ ] User login works
- [ ] Dashboard displays correctly
- [ ] Region profiles are accessible (11 regions)
- [ ] Scheduler is running
- [ ] Auto-generated logs appear (after scheduler runs)
- [ ] No errors in browser console
- [ ] No errors in Railway logs

---

## 🆘 Troubleshooting

### Backend Not Responding
- Check Railway service status (should be green)
- Check logs for errors
- Verify DATABASE_URL is set correctly

### Frontend Can't Connect
- Verify `REACT_APP_API_URL` includes `/api` at the end
- Check browser console for exact error
- Verify backend is running

### CORS Errors
- Verify `FRONTEND_URL` in Railway matches your Vercel URL exactly
- No trailing slashes
- Check Railway logs for CORS configuration message

### Scheduler Not Running
- Check if service is running (green status)
- Check logs for errors
- Verify DATABASE_URL is set in scheduler service

### Region Profiles Missing
- Run: `python backend/region_profiles_seed.py`
- Or check if seed script runs automatically on startup

---

## 📝 Quick Reference

**Railway Backend Variables:**
```
DATABASE_URL=<auto-set>
SECRET_KEY=<generated in Step 1>
FRONTEND_URL=https://your-vercel-app.vercel.app
```

**Vercel Frontend Variables:**
```
REACT_APP_API_URL=https://era-bot-group3-production.up.railway.app/api
REACT_APP_MAPBOX_ACCESS_TOKEN=pk.your-token
```

**Scheduler Start Command:**
```
python backend/scheduler_runner.py
```

---

## ✅ You're Done!

Once all steps are complete, your application is deployed and ready for production. Monitor the logs for the first few hours to catch any issues early.

**Remember:** Auto-logging will start on the next hourly run after deployment. Users will see their first auto-generated power log within 1 hour of registration.

