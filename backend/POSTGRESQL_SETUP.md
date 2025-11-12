# PostgreSQL Setup Guide

This guide will help you set up PostgreSQL for the Electricity Supply Logger application.

## 🚀 Quick Setup

### Option 1: Railway (Recommended for Deployment)

Railway provides a free PostgreSQL database that's easy to set up:

1. **Create Railway Account:**
   - Go to [railway.app](https://railway.app)
   - Sign up with your GitHub account

2. **Create PostgreSQL Database:**
   - Click **"New Project"**
   - Click **"New"** → **"Database"** → **"Add PostgreSQL"**
   - Railway will automatically create a PostgreSQL database

3. **Get Connection URL:**
   - Click on your PostgreSQL service
   - Go to **"Variables"** tab
   - Copy the `DATABASE_URL` value
   - It will look like: `postgresql://user:password@host:port/database`

4. **Add to Environment Variables:**
   - In your backend service (or `.env` file)
   - Add: `DATABASE_URL=your-connection-url-here`
   - Railway will automatically use this URL

5. **Deploy:**
   - Push your code to GitHub
   - Railway will automatically deploy and connect to PostgreSQL
   - Database tables will be created automatically on first run

**That's it!** Your app is now using PostgreSQL. ✅

---

### Option 2: Local PostgreSQL (For Development)

1. **Install PostgreSQL:**
   - **Windows:** Download from [postgresql.org](https://www.postgresql.org/download/windows/)
   - **Mac:** `brew install postgresql`
   - **Linux:** `sudo apt-get install postgresql postgresql-contrib`

2. **Create Database:**
   ```bash
   # Start PostgreSQL service
   # Windows: PostgreSQL service should start automatically
   # Mac/Linux: sudo service postgresql start
   
   # Create database
   createdb electricity_logger
   
   # Or using psql:
   psql -U postgres
   CREATE DATABASE electricity_logger;
   \q
   ```

3. **Configure Environment Variables:**
   - Create `.env` file in `backend/` directory
   - Add:
     ```env
     DB_USER=postgres
     DB_PASSWORD=your-postgres-password
     DB_HOST=localhost
     DB_PORT=5432
     DB_NAME=electricity_logger
     ```
   - Or use `DATABASE_URL`:
     ```env
     DATABASE_URL=postgresql://postgres:password@localhost:5432/electricity_logger
     ```

4. **Run Application:**
   ```bash
   cd backend
   python app.py
   ```
   - Database tables will be created automatically

---

### Option 3: Other Cloud Providers

#### Heroku PostgreSQL
1. Create Heroku app
2. Add PostgreSQL: `heroku addons:create heroku-postgresql:hobby-dev`
3. Get DATABASE_URL: `heroku config:get DATABASE_URL`
4. Add to environment variables

#### Supabase (Free Tier)
1. Create account at [supabase.com](https://supabase.com)
2. Create new project
3. Go to **Settings** → **Database**
4. Copy connection string
5. Add to `DATABASE_URL` environment variable

#### ElephantSQL (Free Tier)
1. Create account at [elephantsql.com](https://www.elephantsql.com)
2. Create new instance
3. Copy connection URL
4. Add to `DATABASE_URL` environment variable

---

## 📊 Database Schema

The application creates the following tables automatically:

### `users`
- `username` (Primary Key)
- `password` (hashed)
- `email` (unique)
- `location`
- `email_verified`
- `created_at`
- `verified_devices` (array)

### `power_logs`
- `id` (Primary Key)
- `user_id` (Foreign Key → users.username)
- `event_type` ('on' or 'off')
- `timestamp`
- `date`
- `location`

### `verification_codes`
- `email` (Primary Key)
- `code`
- `expires_at`
- `username`
- `password` (hashed)
- `location`
- `device_id`

### `device_ids`
- `id` (Primary Key)
- `user_id` (Foreign Key → users.username)
- `device_id`

---

## 🔄 Migrating Existing Data

If you have existing data in JSON/CSV files, you can migrate it to PostgreSQL:

1. **Make sure PostgreSQL is set up and running**

2. **Run migration script:**
   ```bash
   cd backend
   python migrate_to_postgresql.py
   ```

3. **Verify migration:**
   - Check that users can login
   - Check that power logs are visible
   - Verify statistics are correct

4. **Backup original files:**
   - The migration script doesn't delete original files
   - You can delete them after verifying migration was successful

---

## 🔧 Troubleshooting

### Error: "could not connect to server"
- **Solution:** Make sure PostgreSQL is running
  - Windows: Check Services → PostgreSQL
  - Mac/Linux: `sudo service postgresql start`

### Error: "database does not exist"
- **Solution:** Create the database:
  ```bash
  createdb electricity_logger
  ```

### Error: "password authentication failed"
- **Solution:** Check your `DB_PASSWORD` or `DATABASE_URL` is correct
- Try resetting PostgreSQL password

### Error: "relation does not exist"
- **Solution:** Tables are created automatically on first run
- Make sure you're running the app at least once
- Check database connection is working

### Railway: "DATABASE_URL not found"
- **Solution:** 
  1. Go to Railway dashboard
  2. Select your PostgreSQL service
  3. Go to **"Variables"** tab
  4. Copy `DATABASE_URL`
  5. Add it to your backend service environment variables

---

## ✅ Verification

After setting up PostgreSQL, verify it's working:

1. **Check health endpoint:**
   ```bash
   curl http://localhost:5000/
   ```
   Should show: `"database": "connected"`

2. **Test registration:**
   - Register a new user
   - Check that user appears in database
   - Verify email verification works

3. **Test power logging:**
   - Log a power event
   - Check that it appears in database
   - Verify statistics are calculated correctly

---

## 📝 Environment Variables

### Required (choose one):

**Option 1: DATABASE_URL (Recommended)**
```env
DATABASE_URL=postgresql://user:password@host:port/database
```

**Option 2: Individual Parameters**
```env
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=electricity_logger
```

### Notes:
- `DATABASE_URL` takes precedence over individual parameters
- Railway/Heroku automatically provide `DATABASE_URL`
- For local development, you can use either method

---

## 🎉 You're Done!

Your application is now using PostgreSQL instead of file-based storage. Data will persist between deployments and server restarts.

**Benefits:**
- ✅ Data persists permanently
- ✅ Scalable and reliable
- ✅ Industry standard
- ✅ Better performance
- ✅ Built-in backups (on cloud providers)

---

## 📚 Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Railway PostgreSQL](https://docs.railway.app/databases/postgresql)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/)

