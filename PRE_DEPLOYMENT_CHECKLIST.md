# Pre-Deployment Checklist

## 🚨 Critical Items (Must Do Before Deploying)

### 1. Backend Environment Variables (Railway)

**Required Variables:**
- [ ] `DATABASE_URL` - PostgreSQL connection string (usually auto-set by Railway)
- [ ] `SECRET_KEY` - Strong random string for JWT tokens (generate new one for production!)
- [ ] `FRONTEND_URL` - Your Vercel frontend URL (e.g., `https://your-app.vercel.app`)
- [ ] `MAIL_SUPPRESS_SEND` - Set to `true` if email not configured yet (optional)

**Optional (Email Configuration):**
- [ ] `MAIL_SERVER` - SMTP server (e.g., `smtp.gmail.com`)
- [ ] `MAIL_PORT` - SMTP port (usually `587`)
- [ ] `MAIL_USE_TLS` - Set to `true`
- [ ] `MAIL_USERNAME` - Email username or API key
- [ ] `MAIL_PASSWORD` - Email password or API key
- [ ] `MAIL_DEFAULT_SENDER` - Sender email address

**How to Set in Railway:**
1. Go to Railway Dashboard → Your Backend Service
2. Click **Variables** tab
3. Add each variable
4. **Redeploy** after adding variables

### 2. Frontend Environment Variables (Vercel)

**Required Variables:**
- [ ] `REACT_APP_API_URL` - Backend API URL (e.g., `https://era-bot-group3-production.up.railway.app/api`)
  - **MUST include `/api` at the end**
  - **MUST use `https://` not `http://`**
- [ ] `REACT_APP_MAPBOX_ACCESS_TOKEN` - Mapbox public token (starts with `pk.`)

**How to Set in Vercel:**
1. Go to Vercel Dashboard → Your Project
2. Click **Settings** → **Environment Variables**
3. Add each variable
4. Select **Production** environment (and Preview/Development if needed)
5. **Redeploy** after adding variables

### 3. Database Setup

- [ ] PostgreSQL database is created in Railway
- [ ] `DATABASE_URL` is set in backend service (usually auto-linked)
- [ ] Database tables are created (happens automatically on first run)
- [ ] Region profiles are seeded:
  ```bash
  # Run this once to seed region profiles
  python backend/region_profiles_seed.py
  ```
  Or verify in Railway logs that region profiles exist

### 4. Scheduler/Auto-Logger Setup

**Option A: Separate Scheduler Service (Recommended)**
- [ ] Create new Railway service for scheduler
- [ ] Set start command: `python backend/scheduler_runner.py`
- [ ] Link to same database as backend
- [ ] Copy all environment variables from backend service

**Option B: Cron Job in Railway**
- [ ] Set up Cron service in Railway dashboard
- [ ] Schedule: `0 * * * *` (hourly)
- [ ] Command: `python backend/auto_logger.py`
- [ ] Service: Select your backend service

**Option C: Combined with Backend (Not Recommended)**
- [ ] Modify backend start command (requires process manager)
- [ ] Not recommended - use separate service instead

### 5. Region Profiles Verification

- [ ] Verify region profiles are seeded:
  - Test endpoint: `GET https://your-backend-url/api/region-profiles`
  - Should return 11 regions (all Nigerian DisCos)
- [ ] Check that each region has:
  - `schedule_template` (array of time blocks)
  - `avg_offtake_mwh_per_hour`
  - `utilisation_percent`
  - `estimated_daily_mwh`

### 6. CORS Configuration

- [ ] `FRONTEND_URL` is set in Railway backend
- [ ] Frontend URL matches your actual Vercel deployment URL
- [ ] No trailing slashes in `FRONTEND_URL`
- [ ] Test CORS by making API call from frontend

---

## ✅ Pre-Deployment Testing

### Backend Testing

- [ ] **Health Check:**
  ```bash
  curl https://your-backend-url/api
  ```
  Should return: `{"status": "ok", ...}`

- [ ] **Region Profiles Endpoint:**
  ```bash
  curl https://your-backend-url/api/region-profiles
  ```
  Should return JSON with 11 regions

- [ ] **Database Connection:**
  - Check Railway logs for database connection errors
  - Should see: `✅ Database connected successfully`

- [ ] **Registration Endpoint:**
  - Test user registration via frontend or API
  - Verify user is created in database
  - Verify region is assigned based on location

### Frontend Testing

- [ ] **API Connection:**
  - Open browser console (F12)
  - Check for connection errors
  - Should connect to backend without errors

- [ ] **Mapbox Location Search:**
  - Test location autocomplete on signup page
  - Should show street addresses, not just cities
  - Verify location is saved correctly

- [ ] **User Registration:**
  - Register a new user with location
  - Verify region is assigned
  - Verify user can log in

- [ ] **Dashboard Display:**
  - Log in and view dashboard
  - Check that stats load correctly
  - Verify region profiles section works (if implemented)

### Scheduler Testing

- [ ] **Manual Test:**
  ```bash
  python backend/auto_logger.py --dry-run
  ```
  Should show: `Auto logger processed 11 regions and queued X events (dry-run)`

- [ ] **Check Logs:**
  - After scheduler runs, check Railway logs
  - Should see execution messages
  - Check database for auto-generated power logs

---

## 🔧 Configuration Verification

### Railway Backend Service

- [ ] Service is running (green status)
- [ ] No crash errors in logs
- [ ] Port is correctly configured (Railway auto-assigns)
- [ ] Database is linked and accessible
- [ ] All environment variables are set

### Vercel Frontend

- [ ] Deployment is successful
- [ ] No build errors
- [ ] Environment variables are set
- [ ] Frontend URL is accessible
- [ ] API calls work from frontend

### Database

- [ ] Tables exist: `users`, `power_logs`, `region_profiles`, `verification_codes`, `device_ids`
- [ ] Region profiles are populated (11 regions)
- [ ] Can query data successfully

---

## 🚨 Common Issues to Avoid

### ❌ Don't Forget:

1. **SECRET_KEY** - Must be changed from default!
   - Generate: `python -c "import secrets; print(secrets.token_hex(32))"`
   - Set in Railway backend variables

2. **REACT_APP_API_URL** - Must include `/api` suffix!
   - ✅ Correct: `https://backend-url/api`
   - ❌ Wrong: `https://backend-url`

3. **FRONTEND_URL** - Must match exact Vercel URL!
   - No trailing slashes
   - Include `https://`
   - Match production URL exactly

4. **Database URL** - Use public URL if internal doesn't work
   - Railway sometimes provides internal URL that doesn't resolve
   - Check "Connect" tab for public connection string

5. **Scheduler** - Must be running for auto-logging!
   - Without scheduler, no automatic power logs will be created
   - Users will only see manual logs

### ⚠️ Email Configuration (Optional)

If email is not configured:
- Set `MAIL_SUPPRESS_SEND=true` in Railway
- Verification codes will be printed in logs instead
- Users can still register and use the app

---

## 📋 Deployment Order

1. **Backend First:**
   - Set all environment variables
   - Deploy backend service
   - Verify it's running
   - Test API endpoints

2. **Database:**
   - Ensure database is linked
   - Seed region profiles if needed
   - Verify tables exist

3. **Frontend:**
   - Set environment variables
   - Deploy frontend
   - Test connection to backend

4. **Scheduler:**
   - Set up scheduler service or cron
   - Verify it's running
   - Check logs after first run

5. **Final Testing:**
   - End-to-end user flow
   - Register → Login → Dashboard
   - Verify auto-logging works (wait for next hour)

---

## 🧪 Post-Deployment Verification

After deployment, verify:

- [ ] User can register with location
- [ ] User can log in
- [ ] Dashboard displays correctly
- [ ] Stats are calculated
- [ ] Region profiles are accessible
- [ ] Scheduler is running (check logs)
- [ ] Auto-generated logs appear (after scheduler runs)
- [ ] Manual power logging works
- [ ] No console errors in browser
- [ ] No errors in Railway logs

---

## 📞 Quick Troubleshooting

### Backend Not Responding
1. Check Railway service status
2. Check logs for errors
3. Verify DATABASE_URL is set
4. Check PORT is not manually set (let Railway assign)

### Frontend Can't Connect
1. Verify `REACT_APP_API_URL` is set in Vercel
2. Check it includes `/api` suffix
3. Verify backend is running
4. Check CORS settings (FRONTEND_URL)

### Scheduler Not Running
1. Check if service is running
2. Check logs for errors
3. Verify database connection
4. Test manually: `python backend/scheduler_runner.py`

### Region Profiles Missing
1. Run: `python backend/region_profiles_seed.py`
2. Or check if seed script runs on startup
3. Verify database has region_profiles table

---

## 📝 Environment Variables Summary

### Railway Backend (Required)
```
DATABASE_URL=<auto-set by Railway>
SECRET_KEY=<generate new random string>
FRONTEND_URL=https://your-frontend.vercel.app
```

### Railway Backend (Optional - Email)
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
MAIL_SUPPRESS_SEND=false
```

### Vercel Frontend (Required)
```
REACT_APP_API_URL=https://your-backend-url/api
REACT_APP_MAPBOX_ACCESS_TOKEN=pk.your-mapbox-token
```

---

## ✅ Final Checklist

Before going live, ensure:

- [ ] All environment variables are set
- [ ] Backend is deployed and running
- [ ] Frontend is deployed and running
- [ ] Database is connected and seeded
- [ ] Scheduler is running (if using auto-logging)
- [ ] CORS is configured correctly
- [ ] All endpoints are tested
- [ ] No errors in logs
- [ ] User registration works
- [ ] Dashboard displays correctly
- [ ] Auto-logging works (test after deployment)

---

## 🎉 You're Ready!

Once all items are checked, your application is ready for production. Monitor logs for the first few hours to catch any issues early.

**Important:** The scheduler will start creating auto-generated power logs on the next hourly run after deployment. Users who register will see their first auto-log within 1 hour.

