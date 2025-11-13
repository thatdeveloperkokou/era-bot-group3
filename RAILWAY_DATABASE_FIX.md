# Railway Database Connection Fix

## The Problem
Error: `could not translate host name "postgres.railway.internal" to address: Name or service not known`

This happens when Railway provides an internal DATABASE_URL that doesn't resolve properly.

## Solution: Use Public DATABASE_URL

### Step 1: Get the Public DATABASE_URL
1. Go to your Railway project dashboard
2. Click on your **PostgreSQL** service (not the backend service)
3. Go to the **"Variables"** tab
4. Look for `DATABASE_URL` - you should see TWO versions:
   - One with `postgres.railway.internal` (internal - doesn't work)
   - One with a public hostname like `containers-us-west-xxx.railway.app` (public - use this!)

### Step 2: Copy the Public DATABASE_URL
- The public DATABASE_URL will look like:
  ```
  postgresql://postgres:password@containers-us-west-xxx.railway.app:5432/railway
  ```
- Or it might be in a variable called `PUBLIC_DATABASE_URL` or `DATABASE_URL_PUBLIC`
- Copy the entire URL

### Step 3: Update Backend Service
1. Go to your **backend service** in Railway
2. Go to the **"Variables"** tab
3. Find the `DATABASE_URL` variable
4. **Edit it** and replace it with the public DATABASE_URL you copied
5. Save

### Step 4: Redeploy
- Railway should auto-redeploy, or manually trigger a redeploy
- The connection should now work!

## Alternative: Ensure Services Are Linked

If both services are in the same Railway project:
1. Make sure both services are in the **same project**
2. Railway should automatically link them
3. If not linked, you may need to use the public URL anyway

## Verification

After updating DATABASE_URL, check the logs:
- Should see: `✅ Using DATABASE_URL from environment`
- Should see: `✅ Database tables created successfully`
- No more "could not translate host name" errors

## Notes

- Railway provides both internal and public URLs
- Internal URLs (`railway.internal`) only work when services are properly linked in the same private network
- Public URLs always work and are more reliable
- The public URL is safe to use - Railway handles security

