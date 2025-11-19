# Setting Up Scheduler Service in Railway

## Yes, You'll Use the Same GitHub Repository!

The scheduler service uses the **same codebase** as your backend, just with a different start command. Here's how to set it up:

---

## Option 1: Deploy from GitHub (Recommended)

This is the easiest and keeps everything in sync.

### Step-by-Step:

1. **Go to Railway Dashboard:**
   - Visit: https://railway.app
   - Open your existing project (the one with your backend)

2. **Create New Service:**
   - In your Railway project, click **"+ New"** button
   - Select **"GitHub Repo"** (or **"Deploy from GitHub repo"**)
   - **Select the SAME repository** as your backend
   - Railway will create a new service

3. **Configure the Service:**
   - Railway will auto-detect it's a Python project
   - Go to **"Settings"** tab
   
   **Set Root Directory (if needed):**
   - If your backend is in a `backend/` folder, you might need to set:
   - **Root Directory:** `backend` (or leave empty if repo root is backend)
   
   **Set Start Command:**
   - Find **"Start Command"** field
   - Set it to: `python backend/scheduler_runner.py`
   - Or if root is already `backend/`: `python scheduler_runner.py`
   - Click **"Save"**

4. **Set Environment Variables:**
   - Go to **"Variables"** tab
   - Click **"New Variable"**
   
   **Required Variables:**
   - `DATABASE_URL` - Copy from your backend service's `DATABASE_URL`
   - `SECRET_KEY` - Copy from your backend service's `SECRET_KEY`
   
   **Optional:**
   - `MAIL_SUPPRESS_SEND` - Copy from backend if you have it
   - Any other variables your backend uses

5. **Link Database (Alternative Method):**
   - If your PostgreSQL is in the same Railway project:
   - Go to **"Variables"** tab
   - Click **"New Variable"**
   - Railway might show a **"Reference Variable"** option
   - Select your PostgreSQL service's `DATABASE_URL`
   - This automatically links them

6. **Deploy:**
   - Railway will automatically deploy when you connect the repo
   - Check **"Deployments"** tab to see progress
   - Once deployed, check **"Logs"** to verify it's running

---

## Option 2: Empty Service + GitHub (Alternative)

If you don't see "GitHub Repo" option:

1. **Create Empty Service:**
   - Click **"+ New"** → **"Empty Service"**
   - Name it: `scheduler` or `auto-logger`

2. **Connect GitHub:**
   - In the service, click **"Settings"** tab
   - Look for **"Connect GitHub"** or **"Source"** section
   - Click **"Connect GitHub"**
   - Authorize Railway to access your GitHub
   - Select your repository
   - Select the branch (usually `main` or `master`)

3. **Configure:**
   - Follow steps 3-6 from Option 1 above

---

## Option 3: Duplicate Backend Service (Quick Method)

If your backend is already set up:

1. **In Railway Dashboard:**
   - Find your backend service
   - Click the three dots (⋯) menu
   - Look for **"Duplicate"** or **"Clone"** option
   - If available, this creates a copy with same settings

2. **Modify the Duplicate:**
   - Rename it to `scheduler`
   - Change **Start Command** to: `python backend/scheduler_runner.py`
   - Keep all environment variables (they're already copied)

---

## Verification

After setup, verify it's working:

1. **Check Service Status:**
   - Should show green/running status
   - If red, check logs for errors

2. **Check Logs:**
   - Go to **"Deployments"** → Latest → **"View Logs"**
   - Should see: `🕐 Scheduler started`
   - Should see: `Interval: 3600 seconds (1.0 hours)`
   - Should see: `Running indefinitely...`

3. **Wait for First Execution:**
   - Scheduler runs every hour
   - After first hour, check logs for:
     - `Starting auto logger execution #1`
     - `Auto logger processed 11 regions and queued X events`

---

## Important Notes

### Same Repository, Different Service
- ✅ Both services use the same GitHub repo
- ✅ When you push code, both services can auto-update (if configured)
- ✅ They share the same codebase
- ✅ Only difference is the start command

### Environment Variables
- Both services need `DATABASE_URL` (to access same database)
- Both services need `SECRET_KEY` (for Flask app context)
- Scheduler doesn't need `FRONTEND_URL` (it doesn't serve HTTP)
- Scheduler doesn't need `PORT` (it's not a web service)

### Root Directory
- If your repo structure is:
  ```
  your-repo/
    backend/
      scheduler_runner.py
      app.py
      ...
  ```
  - Root Directory: Leave empty (default) OR set to `backend`
  - Start Command: `python backend/scheduler_runner.py`

- If your repo root IS the backend:
  ```
  your-repo/
    scheduler_runner.py
    app.py
    ...
  ```
  - Root Directory: Leave empty
  - Start Command: `python scheduler_runner.py`

---

## Troubleshooting

### Service Won't Start
- Check logs for Python errors
- Verify start command is correct
- Verify `scheduler_runner.py` exists in the repo
- Check that Python dependencies are installed

### Can't Connect to Database
- Verify `DATABASE_URL` is set correctly
- Copy exact value from backend service
- Check that PostgreSQL service is running
- Use public DATABASE_URL (not internal one)

### Scheduler Not Running
- Check service status (should be green)
- Check logs for execution messages
- Verify start command doesn't have typos
- Wait at least 1 hour for first execution

### Code Updates Not Reflecting
- Railway should auto-deploy on git push
- Check **"Settings"** → **"Source"** → Auto-deploy is enabled
- Manually trigger redeploy if needed

---

## Quick Setup Checklist

- [ ] Created new Railway service
- [ ] Connected to same GitHub repository as backend
- [ ] Set Start Command: `python backend/scheduler_runner.py`
- [ ] Set `DATABASE_URL` (copied from backend)
- [ ] Set `SECRET_KEY` (copied from backend)
- [ ] Service is deployed and running (green status)
- [ ] Logs show "Scheduler started" message
- [ ] Waiting for first hourly execution to verify

---

## Summary

**Yes, import from GitHub!** The scheduler service uses the same repository as your backend. The only difference is:
- **Backend service:** Runs `gunicorn app:app` (serves HTTP)
- **Scheduler service:** Runs `python backend/scheduler_runner.py` (runs cron job)

Both services:
- Use the same codebase
- Connect to the same database
- Share environment variables (DATABASE_URL, SECRET_KEY)
- Auto-update when you push to GitHub

This keeps everything in sync and makes updates easy!

