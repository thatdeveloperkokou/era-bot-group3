# Backend Worker Crash - Troubleshooting

## The Problem
Your backend worker is crashing after initialization:
```
✅ Using DATABASE_URL from environment
✅ Database tables created successfully
🌐 CORS: Allowing origins: ['https://era-bot-group3-nx3x.vercel.app']
[2025-11-17 19:27:24 +0000] [3] [ERROR] Worker (pid:4) exited with code 1
```

## What This Means
The initialization completes successfully, but then the worker crashes. This suggests:
1. An error when gunicorn tries to load the app
2. An error in a route handler that's evaluated at import time
3. A missing dependency or import error
4. An issue with the gunicorn configuration

## How to Debug

### Step 1: Check Full Railway Logs
1. Go to Railway Dashboard → Your Backend Service
2. Click on **Deployments** → Latest deployment
3. Scroll through the logs to find the actual error message
4. Look for Python tracebacks or error messages after the initialization

### Step 2: Check for Import Errors
The error might be happening when Python imports the app module. Check:
- Are all dependencies installed? (Check `requirements.txt`)
- Are there any syntax errors in the code?
- Are there any missing imports?

### Step 3: Check Gunicorn Configuration
1. In Railway → Your Backend Service → Variables
2. Check if there's a `START_COMMAND` or similar variable
3. The default should be: `gunicorn app:app --bind 0.0.0.0:$PORT`

### Step 4: Test Locally
Try running the backend locally to see the actual error:
```bash
cd backend
python app.py
```

Or with gunicorn:
```bash
cd backend
gunicorn app:app --bind 0.0.0.0:5000
```

## Common Causes

### 1. Missing Dependencies
**Solution:** Make sure all packages in `requirements.txt` are installed

### 2. Import Error
**Solution:** Check for circular imports or missing modules

### 3. Database Connection Issue
**Solution:** Even though tables are created, there might be an issue with the connection pool

### 4. Email Configuration Error
**Solution:** If email config is invalid, it might cause issues (though we've added error handling for this)

## Quick Fixes to Try

### Fix 1: Check Railway Logs for Actual Error
The most important thing is to see the actual error message. Check Railway logs carefully.

### Fix 2: Simplify Startup
Temporarily comment out non-essential code to isolate the issue.

### Fix 3: Check Gunicorn Workers
In Railway Variables, you can try:
```
GUNICORN_WORKERS=1
GUNICORN_TIMEOUT=120
```

### Fix 4: Use Development Mode
Temporarily set in Railway Variables:
```
FLASK_ENV=development
```

This will give more detailed error messages.

## Next Steps

1. **Check Railway logs** for the actual error message (most important!)
2. Share the full error traceback if you can find it
3. Try running locally to reproduce the error
4. Check if all environment variables are set correctly

The error handling improvements I've added should help catch and log the error, but we need to see the actual error message from Railway logs to fix it properly.

