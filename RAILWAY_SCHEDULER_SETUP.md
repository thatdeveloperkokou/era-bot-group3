# Railway Scheduler Runner Setup

This guide explains how to set up the scheduler runner to automatically execute `auto_logger.py` every hour.

## Option 1: Run Scheduler as Main Service (Recommended for Dedicated Scheduler)

If you want to run the scheduler as a separate service or replace the main service with the scheduler:

### Steps:

1. **Go to Railway Dashboard**
   - Navigate to your Railway project
   - Click on your backend service (or create a new service for the scheduler)

2. **Update Start Command**
   - Go to **Settings** tab
   - Find **"Start Command"** field
   - Set it to:
     ```
     python backend/scheduler_runner.py
     ```
   - Or for dry-run diagnostics:
     ```
     python backend/scheduler_runner.py --dry-run
     ```

3. **Save and Deploy**
   - Railway will automatically redeploy with the new start command
   - The scheduler will start running and execute `auto_logger.py` every hour

## Option 2: Run Both Flask App and Scheduler (Advanced)

If you need both the Flask app and scheduler running in the same service, you can use a process manager or run them in parallel. However, Railway typically runs one process per service, so you may want to:

1. **Keep Flask app as main service** (current setup)
2. **Create a separate service for the scheduler** with start command:
   ```
   python backend/scheduler_runner.py
   ```

## Scheduler Runner Options

The `scheduler_runner.py` script supports several options:

### Basic Usage (Hourly)
```bash
python backend/scheduler_runner.py
```

### Dry-Run Mode (for diagnostics)
```bash
python backend/scheduler_runner.py --dry-run
```

### Custom Interval
```bash
# Run every 30 minutes
python backend/scheduler_runner.py --interval 1800

# Run every 6 hours
python backend/scheduler_runner.py --interval 21600
```

### Initial Delay
```bash
# Wait 5 minutes before first execution
python backend/scheduler_runner.py --initial-delay 300
```

### Limited Iterations (for testing)
```bash
# Run only 3 times then stop
python backend/scheduler_runner.py --max-iterations 3
```

### Combined Options
```bash
# Dry-run, every 6 hours, with 10 minute initial delay
python backend/scheduler_runner.py --dry-run --interval 21600 --initial-delay 600
```

## Verification

After setup, verify the scheduler is working:

1. **Check Railway Logs**
   - Go to your service → **Logs** tab
   - You should see:
     ```
     🕐 Scheduler started
        Interval: 3600 seconds (1.0 hours)
        Running indefinitely...
     ```
   - After the first hour, you should see:
     ```
     [YYYY-MM-DD HH:MM:SS UTC] Starting auto logger execution #1
     Auto logger processed X regions and queued Y events
     [YYYY-MM-DD HH:MM:SS UTC] ✅ Auto logger execution #1 completed successfully
     ⏰ Next execution scheduled for: YYYY-MM-DD HH:MM:SS UTC
     ```

2. **Check Database**
   - Verify that new `PowerLog` entries are being created with `auto_generated=True`
   - Check timestamps to confirm they're being created hourly

## Troubleshooting

### Scheduler Not Running
- Verify the start command is set correctly in Railway settings
- Check that Python is available in the service environment
- Ensure the path to `scheduler_runner.py` is correct relative to the working directory

### Import Errors
- Make sure all dependencies are installed (check `requirements.txt`)
- Verify that `auto_logger.py` and `app.py` are in the same directory
- Check that the database connection is properly configured

### Scheduler Stops Unexpectedly
- Check Railway logs for error messages
- Verify database connectivity
- Ensure the service has sufficient resources allocated

### Multiple Executions
- If you see multiple schedulers running, check if you have multiple services with the same start command
- Ensure only one service is running the scheduler

## Notes

- The scheduler runs in UTC time by default
- The scheduler will continue running indefinitely unless stopped or an unrecoverable error occurs
- Errors during execution are logged but don't stop the scheduler
- Use `--dry-run` mode for testing without affecting production data
- The scheduler uses `time.sleep()` between executions, so it's lightweight and efficient

## Recommended Setup

For production, we recommend:

1. **Main Service**: Keep running Flask app with gunicorn (current setup)
2. **Scheduler Service**: Create a separate Railway service with:
   - Start Command: `python backend/scheduler_runner.py`
   - Same environment variables as backend service (for database access)
   - Same Dockerfile/build settings

This separation ensures:
- Flask app can scale independently
- Scheduler failures don't affect the main app
- Easier monitoring and debugging
- Better resource management

