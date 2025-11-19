# Quick Fix: Add region_id Column to verification_codes

## The Problem
The `VerificationCode` model now has a `region_id` field, but the database table doesn't have this column yet, causing a 500 error during registration.

## ✅ Quick Fix (Choose One Method)

### Method 1: Using Flask-Migrate (Recommended)

```bash
cd backend

# Step 1: Initialize migrations (first time only)
python migrate.py init

# Step 2: Create migration
python migrate.py migrate "Add region_id to verification_codes"

# Step 3: Apply migration
python migrate.py upgrade
```

### Method 2: Direct SQL (Fastest - if you have database access)

Connect to your PostgreSQL database and run:

```sql
ALTER TABLE verification_codes ADD COLUMN region_id VARCHAR(50);
```

### Method 3: Railway CLI

```bash
railway run python backend/migrate.py upgrade
```

## 🚀 For Railway Deployment

### Option A: Run Migration via Railway CLI

1. **Install Railway CLI** (if not installed):
   ```bash
   npm i -g @railway/cli
   ```

2. **Link to your project:**
   ```bash
   railway link
   ```

3. **Run migration:**
   ```bash
   railway run python backend/migrate.py upgrade
   ```

### Option B: Add to Startup Script

Update `backend/start.sh` to run migrations on startup:

```bash
#!/bin/sh
# ... existing PORT handling ...

# Run migrations
echo "🔄 Running database migrations..."
python backend/migrate.py upgrade || echo "⚠️  Migration failed, continuing..."

# Start the application
exec gunicorn app:app --bind "0.0.0.0:${PORT}"
```

### Option C: Manual SQL via Railway Dashboard

1. Go to Railway → PostgreSQL service
2. Click **"Query"** or **"Connect"** tab
3. Run:
   ```sql
   ALTER TABLE verification_codes ADD COLUMN region_id VARCHAR(50);
   ```

## ✅ Verification

After running the migration, test registration:
- Should no longer get 500 error
- Verification code should be saved successfully
- User should be created with region_id after verification

## 📝 Next Steps

After fixing this, you can use Flask-Migrate for future schema changes:

```bash
# Make model changes in database.py
# Then:
python migrate.py migrate "Description of changes"
python migrate.py upgrade
```

