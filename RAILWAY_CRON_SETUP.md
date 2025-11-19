# Railway Cron Job Setup for Auto Logger

This guide explains how to set up the hourly cron job to run `backend/auto_logger.py` in Railway.

## Option 1: Railway Dashboard (Recommended)

Railway's cron jobs are typically configured through the dashboard as separate Cron services:

### Steps:

1. **Go to Railway Dashboard**
   - Navigate to your Railway project
   - Click on your backend service

2. **Add a Cron Service**
   - In your project, click **"+ New"** or **"Add Service"**
   - Select **"Cron"** from the service types
   - Or go to **Settings** → **Cron Jobs** (if available)

3. **Configure the Cron Job**
   - **Name**: `auto-logger` (or any descriptive name)
   - **Schedule**: `0 * * * *` (runs at the start of every hour)
   - **Command**: `python backend/auto_logger.py`
   - **Service**: Select your backend service (this ensures it runs in the same environment)

4. **Add Dry-Run Variant (Optional, for Diagnostics)**
   - Create a second cron job:
   - **Name**: `auto-logger-dry-run`
   - **Schedule**: `0 */6 * * *` (runs every 6 hours, adjust as needed)
   - **Command**: `python backend/auto_logger.py --dry-run`
   - **Service**: Select your backend service

5. **Save and Deploy**
   - Railway will automatically deploy and start running the cron jobs

## Option 2: Railway CLI (Alternative)

If you prefer using the Railway CLI:

```bash
railway cron create \
  --schedule "0 * * * *" \
  --command "python backend/auto_logger.py" \
  --service <your-backend-service-id>
```

## Cron Schedule Format

- `0 * * * *` - Every hour at minute 0 (e.g., 1:00, 2:00, 3:00)
- `0 */6 * * *` - Every 6 hours (for dry-run diagnostics)
- `*/30 * * * *` - Every 30 minutes (if you need more frequent runs)

## Verification

After setup, you can verify the cron job is working by:

1. **Check Railway Logs**
   - Go to your backend service → **Logs** tab
   - Look for output from `auto_logger.py` at the scheduled times
   - You should see: `Auto logger processed X regions and queued Y events`

2. **Check Database**
   - Verify that new `PowerLog` entries are being created with `auto_generated=True`
   - Check timestamps to confirm they're being created hourly

3. **Dry-Run Test**
   - The dry-run variant will show what would be created without actually inserting records
   - Look for: `Auto logger processed X regions and queued Y events (dry-run)`

## Troubleshooting

### Cron Job Not Running
- Verify the schedule format is correct
- Check that the backend service is deployed and running
- Ensure the command path is correct relative to the service's working directory

### Command Not Found
- Make sure Python is available in the service environment
- Verify the path to `auto_logger.py` is correct
- Check that all dependencies are installed in the backend service

### Database Connection Issues
- Ensure the cron job is running in the same service context as your backend
- Verify database environment variables are set correctly
- Check that the database is accessible from the cron job context

## Notes

- The cron job runs in the context of your backend service, so it has access to all environment variables and database connections
- The `auto_logger.py` script uses Flask's application context, so it should work correctly when called from a cron job
- Railway cron jobs run in UTC time by default
- The dry-run variant is useful for testing and diagnostics without affecting production data

