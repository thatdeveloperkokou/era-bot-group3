# Flask-Migrate Setup Guide

Flask-Migrate is now set up for managing database schema changes. This allows you to safely update your database schema without losing data.

## ✅ What's Been Set Up

1. **Flask-Migrate added** to `requirements.txt`
2. **Migration wrapper script** created: `backend/migrate.py`
3. **Flask-Migrate initialized** in `app.py`

## 🚀 Quick Start

### Step 1: Install Dependencies

If you haven't already, install Flask-Migrate:
```bash
pip install -r backend/requirements.txt
```

### Step 2: Initialize Migrations (First Time Only)

This creates the `migrations/` folder:
```bash
cd backend
python migrate.py db init
```

**Note:** If you get an error about migrations already existing, skip this step.

### Step 3: Create Initial Migration (If Database Already Exists)

If your database already has tables, you need to tell Flask-Migrate about the current state:

```bash
python migrate.py db stamp head
```

This marks the current database state as the latest migration.

### Step 4: Create Migration for New Changes

After making changes to models (like adding `region_id` to `VerificationCode`):

```bash
python migrate.py db migrate -m "Add region_id to verification_codes"
```

This creates a new migration file in `migrations/versions/`.

### Step 5: Apply Migration

Apply the migration to your database:

```bash
python migrate.py db upgrade
```

## 📋 Common Commands

### Initialize Migrations (First Time)
```bash
python migrate.py db init
```

### Create a New Migration
```bash
python migrate.py db migrate -m "Description of changes"
```

### Apply Migrations
```bash
python migrate.py db upgrade
```

### Rollback Last Migration
```bash
python migrate.py db downgrade
```

### Check Current Migration Version
```bash
python migrate.py db current
```

### View Migration History
```bash
python migrate.py db history
```

## 🔧 For Railway Deployment

### Option 1: Run Migrations Manually (Recommended)

1. **Connect to Railway:**
   ```bash
   railway link
   railway shell
   ```

2. **Run migration:**
   ```bash
   cd backend
   python migrate.py db upgrade
   ```

### Option 2: Auto-Migrate on Startup

You can add migration to your startup script. Update `backend/start.sh`:

```bash
#!/bin/sh
# Run migrations
python backend/migrate.py db upgrade

# Start the application
exec gunicorn app:app --bind "0.0.0.0:${PORT}"
```

### Option 3: Railway CLI

```bash
railway run python backend/migrate.py db upgrade
```

## 🆕 Adding the region_id Column

Since we just added `region_id` to `VerificationCode`, here's how to migrate:

### If Database is Empty (No Data)
```bash
cd backend
python migrate.py db init          # First time only
python migrate.py db migrate -m "Add region_id to verification_codes"
python migrate.py db upgrade
```

### If Database Has Existing Data

1. **Create migration:**
   ```bash
   python migrate.py db migrate -m "Add region_id to verification_codes"
   ```

2. **Review the migration file** in `migrations/versions/` - it should add the column as nullable

3. **Apply migration:**
   ```bash
   python migrate.py db upgrade
   ```

The migration will add the `region_id` column as nullable, so existing rows won't be affected.

## 🔍 Troubleshooting

### Error: "Target database is not up to date"

This means your database schema doesn't match the migrations. Options:

1. **Stamp current state** (if database is correct):
   ```bash
   python migrate.py db stamp head
   ```

2. **Or upgrade to latest:**
   ```bash
   python migrate.py db upgrade
   ```

### Error: "Can't locate revision identified by..."

The migration history is out of sync. Fix:

```bash
python migrate.py db stamp head
python migrate.py db migrate -m "Sync migration state"
python migrate.py db upgrade
```

### Error: "Table already exists"

If tables exist but migrations don't:

```bash
python migrate.py db stamp head
```

This tells Flask-Migrate that the current database state is the latest migration.

## 📝 Migration Workflow

1. **Make changes** to models in `database.py`
2. **Create migration:**
   ```bash
   python migrate.py db migrate -m "Description"
   ```
3. **Review** the generated migration file in `migrations/versions/`
4. **Apply migration:**
   ```bash
   python migrate.py db upgrade
   ```
5. **Test** your changes
6. **Commit** both model changes and migration files to git

## ⚠️ Important Notes

- **Always commit migration files** to git (they're in `migrations/versions/`)
- **Don't edit migration files** after they've been applied to production
- **Test migrations** on a copy of production data first
- **Backup database** before running migrations in production

## 🎯 For Your Current Issue

To fix the `region_id` column issue:

```bash
cd backend

# If migrations not initialized
python migrate.py db init

# Create migration for region_id
python migrate.py db migrate -m "Add region_id to verification_codes"

# Apply migration
python migrate.py db upgrade
```

This will add the `region_id` column to your `verification_codes` table without losing any data.

