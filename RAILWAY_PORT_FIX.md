# Railway PORT Error Fix

## The Problem
Error: `'$PORT' is not a valid port number`

This error occurs when Railway tries to validate the PORT environment variable and finds the literal string "$PORT" instead of a numeric value.

## Root Cause
In your Railway service settings, the `PORT` environment variable might be manually set to the literal string `$PORT`. Railway automatically assigns PORT values, so you should **NOT** manually set it.

## Solution

### Step 1: Check Railway Service Settings
1. Go to your Railway project dashboard
2. Click on your backend service
3. Go to the **Variables** tab
4. Look for a `PORT` environment variable
5. **If it exists and is set to `$PORT` or any value, DELETE IT**
6. Railway will automatically assign the PORT value

### Step 2: Verify the Fix
The code has been updated to handle this gracefully:
- `start.sh` now validates PORT and defaults to 5000 if invalid
- Dockerfile uses shell form for proper variable expansion

### Step 3: Redeploy
After removing the PORT variable from Railway settings, trigger a new deployment.

## Why This Happens
Railway automatically injects a `PORT` environment variable with a numeric value (like `5000`, `8080`, etc.) when your service starts. If you manually set `PORT=$PORT` in the service settings, Railway sees the literal string "$PORT" and tries to validate it as a port number, which fails.

## Verification
After fixing, your Railway service should:
- Automatically receive a PORT value from Railway
- Start successfully without PORT errors
- The start.sh script will use Railway's assigned PORT or default to 5000

