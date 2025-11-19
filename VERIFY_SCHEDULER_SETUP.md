# Verify Scheduler Setup - Quick Checklist

## ✅ Step 1: Check Service Status

1. **Go to Railway Dashboard:**
   - Open your project
   - Find your **scheduler service**

2. **Check Status:**
   - Should show **green/running** status
   - If red/yellow, check logs for errors

**✅ Status:** [ ] Green/Running

---

## ✅ Step 2: Check Logs

1. **View Logs:**
   - Click on scheduler service
   - Go to **"Deployments"** tab
   - Click on latest deployment
   - Click **"View Logs"** or **"Logs"** tab

2. **Look for These Messages:**
   - `🕐 Scheduler started`
   - `Interval: 3600 seconds (1.0 hours)`
   - `Running indefinitely...`

**✅ Logs Show:** [ ] Scheduler started message

---

## ✅ Step 3: Verify Environment Variables

1. **Go to Variables Tab:**
   - Scheduler service → **"Variables"** tab

2. **Check These Are Set:**
   - [ ] `DATABASE_URL` - Should match backend's DATABASE_URL
   - [ ] `SECRET_KEY` - Should match backend's SECRET_KEY

**✅ Variables Set:** [ ] DATABASE_URL and SECRET_KEY are present

---

## ✅ Step 4: Test Auto-Logger (Dry Run)

You can test if the auto-logger works without waiting an hour:

1. **In Railway:**
   - Go to scheduler service
   - Click **"Settings"** tab
   - Temporarily change **Start Command** to:
     ```
     python backend/auto_logger.py --dry-run
     ```
   - Save (this will redeploy)

2. **Check Logs:**
   - Should see: `Auto logger processed 11 regions and queued X events (dry-run)`
   - This confirms it's working!

3. **Change Back:**
   - Change Start Command back to: `python backend/scheduler_runner.py`
   - Save to redeploy

**✅ Dry Run Test:** [ ] Completed successfully

---

## ✅ Step 5: Wait for First Real Execution

The scheduler runs every hour. To verify it's working:

1. **Note the Current Time:**
   - Example: 2:30 PM

2. **Wait Until Next Hour:**
   - Example: Wait until 3:00 PM (next hour mark)

3. **Check Logs:**
   - Should see: `Starting auto logger execution #1`
   - Should see: `Auto logger processed 11 regions and queued X events`
   - Should see: `Next execution scheduled for: [time]`

**✅ First Execution:** [ ] Logs show execution at next hour

---

## ✅ Step 6: Verify Database (Optional)

1. **Register a Test User:**
   - Go to your frontend
   - Register with location: "Lekki, Lagos" (or any Nigerian location)

2. **Wait for Next Hour:**
   - Scheduler will create auto-generated power logs

3. **Check Dashboard:**
   - Log in as test user
   - Go to dashboard
   - Should see power logs appearing automatically
   - Check timestamps - should align with hourly schedule

**✅ Database Test:** [ ] Auto-generated logs appear in dashboard

---

## 🎉 Success Indicators

If you see these, everything is working:

✅ Scheduler service is running (green status)
✅ Logs show "Scheduler started"
✅ Logs show execution messages every hour
✅ Auto-generated power logs appear in user dashboards
✅ No errors in logs

---

## 🆘 Troubleshooting

### Service Not Running
- Check logs for Python errors
- Verify start command is correct
- Check environment variables are set

### No Execution Messages
- Wait for next hour (scheduler runs at :00 minutes)
- Check if service is actually running
- Verify database connection

### Database Errors
- Verify DATABASE_URL is correct
- Check PostgreSQL service is running
- Use public DATABASE_URL (not internal)

---

## 📝 Next Steps

Once verified:
1. ✅ Monitor logs for first few hours
2. ✅ Test user registration and auto-logging
3. ✅ Verify dashboard shows auto-generated logs
4. ✅ Check that region profiles are working

**You're all set!** 🎉

