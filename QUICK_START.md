# 🚀 Quick Start Guide - Push to GitHub

Follow these steps to push your project to GitHub and prepare for deployment.

## Step 1: Open Terminal in Project Folder

Navigate to your project folder:
```bash
cd "C:\Users\salom\group 3 bot project"
```

## Step 2: Initialize Git (if needed)

```bash
git init
```

## Step 3: Add All Files

```bash
git add .
```

## Step 4: Commit Your Changes

```bash
git commit -m "Initial commit: Electricity Supply Logger Bot with deployment configuration"
```

## Step 5: Connect to Your GitHub Repository

Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub username and repository name:

```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
```

## Step 6: Push to GitHub

```bash
git branch -M main
git push -u origin main
```

If this is your first time, GitHub might ask for authentication. You can:
- Use a Personal Access Token (recommended)
- Or use GitHub Desktop application

## Step 7: Verify on GitHub

1. Go to your GitHub repository
2. You should see all your files there
3. You're ready to deploy!

## Next Steps

After pushing to GitHub, follow the [DEPLOYMENT.md](./DEPLOYMENT.md) guide to:
1. Deploy backend to Railway
2. Deploy frontend to Vercel
3. Connect everything together

---

**Need Help?**

If you get authentication errors:
1. Go to GitHub.com → Settings → Developer settings → Personal access tokens
2. Generate a new token with `repo` permissions
3. Use the token as your password when pushing

