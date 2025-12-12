# Render Quick Start Guide

This is a quick reference for deploying to Render. For detailed migration instructions, see [RENDER_MIGRATION.md](./RENDER_MIGRATION.md).

## 🚀 Quick Deploy (Using render.yaml)

1. **Push `render.yaml` to your GitHub repository**

2. **Go to Render Dashboard**:
   - Visit [dashboard.render.com](https://dashboard.render.com)
   - Click **"New +"** → **"Blueprint"**
   - Connect your GitHub repository
   - Select the repository
   - Render will automatically create:
     - ✅ Backend Web Service
     - ✅ PostgreSQL Database
     - ✅ Random data generator available

3. **Set Environment Variables** (in Backend Web Service):
   - `FRONTEND_URL`: Your frontend URL (e.g., `https://your-frontend.vercel.app`)
   - `RESEND_API_KEY`: (Optional) For email functionality
   - `RESEND_FROM_EMAIL`: (Optional) Your Resend email

4. **Import Data** (if migrating):
   - Export from Railway: `pg_dump "RAILWAY_URL" > backup.sql`
   - Import to Render: `psql "RENDER_URL" < backup.sql`

5. **Update Frontend**:
   - Update `REACT_APP_API_URL` to your Render backend URL
   - Example: `https://era-bot-backend.onrender.com/api`

## 📋 Manual Setup (Alternative)

If you prefer manual setup or need customization:

### 1. PostgreSQL Database
- **New +** → **PostgreSQL**
- Name: `era-bot-postgres`
- Database: `electricity_logger`
- Plan: Free (or upgrade)

### 2. Backend Web Service
- **New +** → **Web Service**
- Connect GitHub repo
- **Settings**:
  - Root Directory: `backend`
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`
- **Environment Variables**:
  - `DATABASE_URL`: (Auto-linked from PostgreSQL)
  - `SECRET_KEY`: Generate random string
  - `FRONTEND_URL`: Your frontend URL
  - `RESEND_API_KEY`: (Optional)

### 3. Cron Job
- **New +** → **Cron Job**
- Connect GitHub repo
- **Settings**:
  - Root Directory: `backend`
  - Schedule: `0 * * * *` (every hour)
  - Build Command: `pip install -r requirements.txt`
  - Start Command: `python generate_random_data.py` (optional, for generating test data)
- **Environment Variables**:
  - `DATABASE_URL`: (Auto-linked from PostgreSQL)
  - `SECRET_KEY`: (Same as backend)

## ✅ Verify Deployment

1. **Health Check**:
   ```bash
   curl https://your-backend.onrender.com/
   ```
   Should return: `{"status": "ok", "database": "connected"}`

2. **Test Registration/Login**
3. **Test Power Logging**
4. **Check Cron Job Logs** (wait for next scheduled run)

## 🔗 Important URLs

- **Render Dashboard**: [dashboard.render.com](https://dashboard.render.com)
- **Documentation**: [render.com/docs](https://render.com/docs)
- **PostgreSQL Guide**: [render.com/docs/databases](https://render.com/docs/databases)
- **Cron Jobs**: [render.com/docs/cron-jobs](https://render.com/docs/cron-jobs)

## 💡 Tips

- **Free Tier**: Services spin down after 15 min inactivity (first request may be slow)
- **Database Backups**: Export regularly on free tier
- **Environment Variables**: Use `fromService` in `render.yaml` to sync between services
- **Custom Domain**: Add in Render dashboard → Settings → Custom Domain

## 🆘 Common Issues

**Service won't start**: Check logs, verify build/start commands
**Database connection fails**: Verify `DATABASE_URL` is set correctly
**Cron job not running**: Check schedule format and logs
**CORS errors**: Set `FRONTEND_URL` environment variable

For detailed troubleshooting, see [RENDER_MIGRATION.md](./RENDER_MIGRATION.md).

