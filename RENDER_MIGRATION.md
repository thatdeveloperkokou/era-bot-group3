# Render PostgreSQL Database Setup Guide

This guide will help you set up a new PostgreSQL database on Render for your backend and cron jobs.

## 📋 Prerequisites

1. **Render Account**: Sign up at [render.com](https://render.com) (free tier available)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **Optional - Migrating Existing Data**: If you have data in an old database (Railway, local, etc.), export it first before setting up the new Render database

## 🚀 Step-by-Step Setup

### Step 1: Create Services on Render

#### Option A: Using render.yaml (Recommended)

1. **Push render.yaml to your repository** (already created in the root directory)
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click **"New +"** → **"Blueprint"**
4. Connect your GitHub repository
5. Select the repository containing your code
6. Render will automatically detect `render.yaml` and create all services

#### Option B: Manual Setup

If you prefer manual setup or need to customize:

##### 1.1 Create PostgreSQL Database

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"PostgreSQL"**
3. Configure:
   - **Name**: `era-bot-postgres` (or your preferred name)
   - **Database**: `electricity_logger`
   - **User**: `electricity_user` (or auto-generated)
   - **Region**: Choose closest to your users
   - **Plan**: Free (or upgrade for production)
4. Click **"Create Database"**
5. **Save the connection string** - you'll need it for the backend

##### 1.2 Create Backend Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `era-bot-backend`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && gunicorn app:app --bind 0.0.0.0:$PORT`
   - **Plan**: Free (or upgrade for production)
4. **Environment Variables**:
   - `DATABASE_URL`: Copy from PostgreSQL service (Render auto-provides this)
   - `SECRET_KEY`: Generate a random string (e.g., use `openssl rand -hex 32`)
   - `FRONTEND_URL`: Your frontend URL (e.g., `https://your-frontend.vercel.app`)
   - `RESEND_API_KEY`: (Optional) If using Resend for emails
   - `RESEND_FROM_EMAIL`: (Optional) Your Resend email
   - `PORT`: `10000` (Render sets this automatically, but good to have)
5. Click **"Create Web Service"**

##### 1.3 Create Cron Job

1. Click **"New +"** → **"Cron Job"**
2. Connect your GitHub repository
3. Configure:
   - **Name**: `era-bot-auto-logger`
   - **Environment**: `Python 3`
   - **Schedule**: `0 * * * *` (every hour at minute 0)
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `cd backend && python auto_logger.py`
   - **Plan**: Free
4. **Environment Variables**:
   - `DATABASE_URL`: Copy from PostgreSQL service
   - `SECRET_KEY`: Same as backend service
5. Click **"Create Cron Job"**

### Step 2: Initialize Database

The database tables will be created automatically when you first run the backend service. No manual setup required!

**Optional - If Migrating Data from Old Database:**

If you have existing data to migrate:

1. Export from your old database:
   ```bash
   # From Railway (if migrating)
   pg_dump "YOUR_OLD_DATABASE_URL" > backup.sql
   
   # From local PostgreSQL
   pg_dump -U postgres electricity_logger > backup.sql
   ```

2. Get your Render PostgreSQL connection string:
   - Go to your PostgreSQL service in Render
   - Go to **"Info"** tab
   - Copy the **"Internal Database URL"** (for services in same Render account)
   - Or use **"External Connection String"** if importing from outside Render

3. Import your backup:
   ```bash
   # Using psql
   psql "YOUR_RENDER_DATABASE_URL" < backup.sql
   
   # Or using pg_restore for custom format
   pg_restore -d "YOUR_RENDER_DATABASE_URL" backup.dump
   ```

**Alternative**: Use Render's built-in database tools or a database client like pgAdmin.

### Step 3: Update Frontend API URL

1. Update your frontend environment variables:
   - In Vercel (or your frontend host), update `REACT_APP_API_URL`
   - Set it to: `https://era-bot-backend.onrender.com/api` (or your Render service URL)

2. Update CORS settings:
   - In Render backend service, ensure `FRONTEND_URL` environment variable matches your frontend URL

### Step 4: Test Everything

1. **Test Backend Health**:
   ```bash
   curl https://your-backend.onrender.com/
   ```
   Should return: `{"status": "ok", "database": "connected"}`

2. **Test Database Connection**:
   - Try logging in/registering
   - Check that data is being saved

3. **Test Cron Job**:
   - Wait for the next scheduled run (or trigger manually)
   - Check Render logs to see if `auto_logger.py` runs successfully

### Step 5: Update DNS/URLs (if using custom domains)

If you want to use a custom domain:
1. Add custom domain in Render dashboard
2. Update DNS records to point to Render
3. Update frontend API URLs

## 🔧 Configuration Details

### Environment Variables

| Variable | Render | Notes |
|----------|--------|-------|
| `DATABASE_URL` | Auto-provided | Automatically linked when using `render.yaml` |
| `PORT` | Auto-set | Render sets this automatically |
| `SECRET_KEY` | Manual | Generate with `openssl rand -hex 32` |
| `FRONTEND_URL` | Manual | Your frontend URL (e.g., `https://your-frontend.vercel.app`) |

### Cron Jobs

- **Type**: Separate Cron Job service (independent from web service)
- **Schedule**: `0 * * * *` (runs every hour at minute 0)
- **Environment**: Shares same environment variables as backend
- **Runs**: Independently, even if web service is sleeping

### Database Connection

- **Internal Connection**: Use "Internal Database URL" for services in the same Render account (faster, more secure)
- **External Connection**: Use "External Connection String" only if connecting from outside Render
- **Auto-linking**: When using `render.yaml`, Render automatically links the database to your services

## 📝 Important Notes

1. **Free Tier Limitations**:
   - Render free tier services spin down after 15 minutes of inactivity
   - First request after spin-down may be slow (~30 seconds)
   - Consider upgrading to paid plan for production
   - Free tier PostgreSQL has size limitations (check current limits)

2. **Database Backups**:
   - Render provides automatic backups on paid plans
   - Free tier: Manual backups recommended
   - Export data regularly using `pg_dump`
   - Keep backups of important data

3. **Cron Job Timing**:
   - Cron jobs run on schedule regardless of web service status
   - Ensure cron job has proper error handling
   - Check logs regularly to ensure cron jobs are running successfully

4. **Environment Variables**:
   - Render allows syncing variables between services
   - Use `fromService` in `render.yaml` to share variables
   - `DATABASE_URL` is automatically provided when database is linked

5. **Database Initialization**:
   - Tables are created automatically on first backend startup
   - No manual SQL scripts needed
   - Database schema is managed by SQLAlchemy

## ✅ Verification Checklist

- [ ] PostgreSQL database created on Render
- [ ] Database connection string copied and added to backend service
- [ ] Backend web service deployed and running
- [ ] Health check endpoint returns success (check `/` endpoint)
- [ ] Database tables created automatically (check logs)
- [ ] User registration/login works
- [ ] Power logging works
- [ ] Data persists correctly
- [ ] Cron job created and scheduled
- [ ] Cron job runs successfully (check logs)
- [ ] Frontend updated with new API URL
- [ ] CORS configured correctly
- [ ] All environment variables set
- [ ] (Optional) Old database data migrated successfully

## 🆘 Troubleshooting

### Database Connection Issues

**Error**: "could not connect to server" or "could not translate host name"

**Solution**: 
- Ensure you're using the correct `DATABASE_URL` from Render
- Use the "Internal Database URL" for services in the same Render account
- Use "External Connection String" only if connecting from outside Render
- Check that the database service is running (not paused)
- Verify the database name matches what you configured

### Cron Job Not Running

**Check**:
1. Go to Cron Job service → **"Logs"** tab
2. Verify the schedule is correct
3. Check for errors in logs
4. Ensure `DATABASE_URL` is set correctly

### Backend Not Starting

**Check**:
1. Go to Web Service → **"Logs"** tab
2. Verify build command succeeds
3. Check start command syntax
4. Ensure all dependencies are in `requirements.txt`

### CORS Errors

**Solution**:
- Set `FRONTEND_URL` environment variable in Render
- Include protocol: `https://your-frontend.vercel.app`
- Restart the service after updating

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [Render PostgreSQL Guide](https://render.com/docs/databases)
- [Render Cron Jobs](https://render.com/docs/cron-jobs)
- [Render Environment Variables](https://render.com/docs/environment-variables)

## 🎉 Setup Complete!

Once everything is verified and working, your application is successfully running on Render with PostgreSQL!

**Benefits of Render**:
- ✅ Simple deployment process
- ✅ Automatic SSL certificates
- ✅ Built-in PostgreSQL support
- ✅ Easy cron job setup
- ✅ Free tier available
- ✅ Great documentation
- ✅ Automatic database linking with `render.yaml`
- ✅ Reliable and scalable infrastructure

