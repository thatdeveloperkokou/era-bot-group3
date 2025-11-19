# Deployment Quick Reference

## 🚀 Critical Items (5-Minute Checklist)

### Railway Backend
```
✅ DATABASE_URL (auto-set by Railway)
✅ SECRET_KEY (generate new: python -c "import secrets; print(secrets.token_hex(32))")
✅ FRONTEND_URL=https://your-frontend.vercel.app
```

### Vercel Frontend
```
✅ REACT_APP_API_URL=https://your-backend-url/api  (MUST include /api!)
✅ REACT_APP_MAPBOX_ACCESS_TOKEN=pk.your-token
```

### Scheduler Setup
```
Option 1: New Railway service
  Start Command: python backend/scheduler_runner.py

Option 2: Railway Cron
  Schedule: 0 * * * *
  Command: python backend/auto_logger.py
```

## ⚠️ Most Common Mistakes

1. **REACT_APP_API_URL missing `/api`** → Frontend can't connect
2. **SECRET_KEY still default** → Security risk
3. **Scheduler not running** → No auto-logging
4. **FRONTEND_URL wrong** → CORS errors
5. **Region profiles not seeded** → Auto-logger fails

## 🧪 Quick Test Commands

```bash
# Test backend
curl https://your-backend-url/api

# Test region profiles
curl https://your-backend-url/api/region-profiles

# Test scheduler (dry-run)
python backend/auto_logger.py --dry-run
```

## 📋 Deployment Order

1. Backend → Set vars → Deploy → Test
2. Database → Verify connection → Seed regions
3. Frontend → Set vars → Deploy → Test
4. Scheduler → Set up → Verify running

---

**Full checklist:** See `PRE_DEPLOYMENT_CHECKLIST.md`

