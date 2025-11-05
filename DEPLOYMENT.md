# 🚀 Deployment Guide

This guide will help you deploy your Electricity Supply Logger Bot to **Vercel** (frontend) and **Railway** (backend), and push your code to **GitHub**.

## 📋 Prerequisites

- A GitHub account (you mentioned you already created a repository)
- A Vercel account (free at [vercel.com](https://vercel.com))
- A Railway account (free at [railway.app](https://railway.app))
- Git installed on your computer

---

## Step 1: Push Code to GitHub

### 1.1 Initialize Git (if not already done)

Open your terminal in the project root directory and run:

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit your changes
git commit -m "Initial commit: Electricity Supply Logger Bot"

# Add your GitHub repository as remote (replace YOUR_USERNAME and YOUR_REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**Note:** Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub username and repository name.

---

## Step 2: Deploy Backend to Railway

### 2.1 Create Railway Account

1. Go to [railway.app](https://railway.app)
2. Sign up with your GitHub account (recommended for easier integration)

### 2.2 Create New Project

1. Click **"New Project"**
2. Select **"Deploy from GitHub repo"**
3. Choose your repository
4. Railway will automatically detect it's a Python project

### 2.3 Configure Backend Deployment

1. **Set Root Directory:**
   - In Railway dashboard, go to your service
   - Click on **"Settings"**
   - Under **"Root Directory"**, set it to: `backend`

2. **Set Build Command:**
   - Railway should auto-detect, but if needed:
   - Build Command: `pip install -r requirements.txt`

3. **Set Start Command:**
   - Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT`

4. **Add Environment Variables:**
   - Go to **"Variables"** tab
   - Add the following:
     - `SECRET_KEY`: Generate a random secret key (you can use: `python -c "import secrets; print(secrets.token_hex(32))"`)
     - `PORT`: Railway sets this automatically, but you can add it if needed

5. **Deploy:**
   - Railway will automatically deploy when you push to GitHub
   - Or click **"Deploy"** button manually

### 2.4 Get Your Backend URL

1. After deployment, Railway will provide a URL like: `https://your-app-name.railway.app`
2. **Copy this URL** - you'll need it for the frontend configuration
3. Your API will be available at: `https://your-app-name.railway.app/api`

---

## Step 3: Deploy Frontend to Vercel

### 3.1 Create Vercel Account

1. Go to [vercel.com](https://vercel.com)
2. Sign up with your GitHub account

### 3.2 Import Project

1. Click **"Add New..."** → **"Project"**
2. Import your GitHub repository
3. Vercel will detect it's a React project

### 3.3 Configure Frontend Deployment

1. **Framework Preset:** React (should be auto-detected)

2. **Root Directory:** 
   - Click **"Edit"** next to Root Directory
   - Set it to: `frontend`

3. **Build Command:**
   - Should be: `npm run build` (auto-detected)

4. **Output Directory:**
   - Should be: `build` (auto-detected)

5. **Environment Variables:**
   - Click **"Environment Variables"**
   - Add:
     - Key: `REACT_APP_API_URL`
     - Value: `https://your-railway-backend-url.railway.app/api`
     - **Important:** Replace `your-railway-backend-url` with your actual Railway URL from Step 2.4

6. **Deploy:**
   - Click **"Deploy"**
   - Vercel will build and deploy your frontend

### 3.4 Get Your Frontend URL

1. After deployment, Vercel will provide a URL like: `https://your-app-name.vercel.app`
2. This is your live frontend URL!

---

## Step 4: Update CORS Settings (If Needed)

If you encounter CORS errors, you may need to update the backend CORS settings to allow your Vercel domain:

1. Go to Railway dashboard → Your backend service
2. Go to **"Variables"** tab
3. Add a new variable:
   - Key: `FRONTEND_URL`
   - Value: `https://your-vercel-app.vercel.app`

Then update `backend/app.py` to use this:

```python
frontend_url = os.environ.get('FRONTEND_URL', '*')
CORS(app, resources={r"/api/*": {"origins": frontend_url}}, supports_credentials=True)
```

---

## Step 5: Test Your Deployment

1. **Test Backend:**
   - Visit: `https://your-railway-url.railway.app`
   - You should see a JSON response with API status

2. **Test Frontend:**
   - Visit: `https://your-vercel-url.vercel.app`
   - Try registering a new user
   - Test logging power events

---

## 🔄 Updating Your Deployment

Whenever you make changes to your code:

1. **Commit and push to GitHub:**
   ```bash
   git add .
   git commit -m "Your commit message"
   git push origin main
   ```

2. **Railway and Vercel will automatically redeploy** your changes (if auto-deploy is enabled)

---

## 📝 Important Notes

### For Your Teacher Demo:

1. **Show the live URLs:**
   - Frontend: `https://your-vercel-url.vercel.app`
   - Backend API: `https://your-railway-url.railway.app/api`

2. **Demonstrate features:**
   - User registration/login
   - Logging power events
   - Viewing statistics and charts

3. **Show the codebase:**
   - Your GitHub repository shows the full source code
   - Both frontend (React) and backend (Flask) are visible

### Security Notes:

- The `SECRET_KEY` in production should be a strong random string
- Consider using environment variables for all sensitive data
- For production, consider using a proper database instead of CSV files

### Troubleshooting:

**Backend not connecting:**
- Check that Railway deployment is successful
- Verify the `REACT_APP_API_URL` in Vercel matches your Railway URL
- Check Railway logs for errors

**Frontend build failing:**
- Check Vercel build logs
- Ensure all dependencies are in `package.json`
- Verify environment variables are set correctly

**CORS errors:**
- Update CORS settings as described in Step 4
- Make sure your Vercel URL is allowed in backend CORS

---

## 🎉 You're Done!

Your application is now live and ready to showcase to your teacher!

**Live URLs:**
- Frontend: [Your Vercel URL]
- Backend: [Your Railway URL]
- GitHub: [Your GitHub Repository URL]

Good luck with your presentation! 🚀

