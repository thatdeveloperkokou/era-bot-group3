# Migration Guide: Railway to Render

This guide will help you migrate your backend, PostgreSQL database, and cron jobs from Railway to Render.

## 📋 Prerequisites

1. **Render Account**: Sign up at [render.com](https://render.com) (free tier available)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **Backup Your Data**: Export your PostgreSQL data from Railway before migration

## 🚀 Step-by-Step Migration

### Step 1: Export Data from Railway PostgreSQL

1. Go to your Railway dashboard
2. Open your PostgreSQL service
3. Go to the **"Connect"** or **"Data"** tab
4. Use the connection string to export your data:

```bash
# Using pg_dump (install PostgreSQL client tools)
pg_dump "YOUR_RAILWAY_DATABASE_URL" > backup.sql

# Or use Railway's built-in export feature if available
```

**Important**: Save this backup file - you'll need it to restore data on Render.

### Step 2: Create Services on Render

#### Option A: Using render.yaml (Recommended)

1. **Push render.yaml to your repository** (already created in the root directory)
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click **"New +"** → **"Blueprint"**
4. Connect your GitHub repository
5. Select the repository containing your code
6. Render will automatically detect `render.yaml` and create all services

#### Option B: Manual Setup

If you prefer manual setup or need to customize:

##### 2.1 Create PostgreSQL Database

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

##### 2.2 Create Backend Web Service

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

##### 2.3 Create Cron Job

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

### Step 3: Import Data to Render PostgreSQL

1. Get your Render PostgreSQL connection string:
   - Go to your PostgreSQL service in Render
   - Go to **"Info"** tab
   - Copy the **"Internal Database URL"** or **"External Connection String"**

2. Import your backup:

```bash
# Using psql
psql "YOUR_RENDER_DATABASE_URL" < backup.sql

# Or using pg_restore for custom format
pg_restore -d "YOUR_RENDER_DATABASE_URL" backup.dump
```

**Alternative**: Use Render's built-in database tools or a database client like pgAdmin.

### Step 4: Update Frontend API URL

1. Update your frontend environment variables:
   - In Vercel (or your frontend host), update `REACT_APP_API_URL`
   - Set it to: `https://era-bot-backend.onrender.com/api` (or your Render service URL)

2. Update CORS settings:
   - In Render backend service, ensure `FRONTEND_URL` environment variable matches your frontend URL

### Step 5: Test Everything

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

### Step 6: Update DNS/URLs (if using custom domains)

If you were using custom domains on Railway:
1. Update DNS records to point to Render
2. Add custom domain in Render dashboard
3. Update frontend API URLs

### Step 7: Clean Up Railway

**⚠️ Important**: Only do this after confirming everything works on Render!

1. Verify all data is migrated
2. Test all functionality
3. Update all external references (frontend, documentation, etc.)
4. Delete Railway services:
   - Go to Railway dashboard
   - Delete PostgreSQL service
   - Delete backend service
   - Delete cron job (if separate)

## 🔧 Configuration Differences

### Environment Variables

| Railway | Render | Notes |
|---------|--------|-------|
| Auto-provided `DATABASE_URL` | Auto-provided `DATABASE_URL` | Same |
| `PORT` (auto-set) | `PORT` (auto-set) | Same |
| Railway internal hostnames | Render internal hostnames | Both work similarly |

### Cron Jobs

| Railway | Render |
|---------|--------|
| Configured in `railway.json` | Separate Cron Job service |
| Runs as part of web service | Runs as independent service |
| Schedule: `0 * * * *` | Schedule: `0 * * * *` |

### Database Connection

- **Railway**: Uses `railway.internal` hostnames (internal) or public URLs
- **Render**: Uses internal connection strings automatically
- Both support `DATABASE_URL` environment variable

## 📝 Important Notes

1. **Free Tier Limitations**:
   - Render free tier services spin down after 15 minutes of inactivity
   - First request after spin-down may be slow (~30 seconds)
   - Consider upgrading to paid plan for production

2. **Database Backups**:
   - Render provides automatic backups on paid plans
   - Free tier: Manual backups recommended
   - Export data regularly

3. **Cron Job Timing**:
   - Cron jobs run on schedule regardless of web service status
   - Ensure cron job has proper error handling

4. **Environment Variables**:
   - Render allows syncing variables between services
   - Use `fromService` in `render.yaml` to share variables

## ✅ Verification Checklist

- [ ] PostgreSQL database created on Render
- [ ] Data successfully imported
- [ ] Backend web service deployed and running
- [ ] Health check endpoint returns success
- [ ] User registration/login works
- [ ] Power logging works
- [ ] Cron job created and scheduled
- [ ] Cron job runs successfully (check logs)
- [ ] Frontend updated with new API URL
- [ ] CORS configured correctly
- [ ] All environment variables set
- [ ] Railway services deleted (after verification)

## 🆘 Troubleshooting

### Database Connection Issues

**Error**: "could not translate host name"

**Solution**: 
- Ensure you're using the correct `DATABASE_URL` from Render
- Use the "Internal Database URL" for services in the same Render account
- Check that the database service is running

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

## 🎉 Migration Complete!

Once everything is verified and working, your application is successfully migrated to Render!

**Benefits of Render**:
- ✅ Simple deployment process
- ✅ Automatic SSL certificates
- ✅ Built-in PostgreSQL support
- ✅ Easy cron job setup
- ✅ Free tier available
- ✅ Great documentation

