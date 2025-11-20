# Google OAuth Setup Guide

## ✅ What's Been Added

I've added Google OAuth login to your application! Users can now login with their Google account - no email verification needed!

## 🎯 Features

- ✅ Google Sign-In button on login/register page
- ✅ Automatic account creation for new users
- ✅ Automatic login for existing users
- ✅ No email verification needed
- ✅ Seamless user experience

---

## 🔧 Setup Required

### Step 1: Get Google OAuth Credentials

1. **Go to Google Cloud Console:**
   - Visit: https://console.cloud.google.com
   - Sign in with your Google account

2. **Create a New Project (or select existing):**
   - Click "Select a project" → "New Project"
   - Enter project name: "Electricity Logger"
   - Click "Create"

3. **Enable Google+ API:**
   - Go to "APIs & Services" → "Library"
   - Search for "Google+ API"
   - Click "Enable"

4. **Create OAuth 2.0 Credentials:**
   - Go to "APIs & Services" → "Credentials"
   - Click "Create Credentials" → "OAuth client ID"
   - If prompted, configure OAuth consent screen first:
     - User Type: External
     - App name: "Electricity Logger"
     - User support email: Your email
     - Developer contact: Your email
     - Click "Save and Continue"
     - Scopes: Click "Save and Continue"
     - Test users: Add your email, click "Save and Continue"
     - Click "Back to Dashboard"

5. **Create OAuth Client ID:**
   - Application type: **Web application**
   - Name: "Electricity Logger Web"
   - **Authorized JavaScript origins:**
     - Add: `http://localhost:3000` (for local development)
     - Add: `https://your-frontend-domain.vercel.app` (your Vercel URL)
   - **Authorized redirect URIs:**
     - Add: `http://localhost:3000` (for local development)
     - Add: `https://your-frontend-domain.vercel.app` (your Vercel URL)
   - Click "Create"

6. **Copy Client ID:**
   - You'll see your Client ID
   - Copy it (looks like: `123456789-abcdefghijklmnop.apps.googleusercontent.com`)

---

### Step 2: Add to Frontend (Vercel)

1. **Go to Vercel Dashboard:**
   - Your frontend project → Settings → Environment Variables

2. **Add Environment Variable:**
   - **Key:** `REACT_APP_GOOGLE_CLIENT_ID`
   - **Value:** Your Google Client ID (from Step 1)
   - **Environment:** Production, Preview, Development
   - Click "Save"

3. **Redeploy Frontend:**
   - Vercel will auto-redeploy
   - Or manually trigger redeploy

---

### Step 3: Add to Backend (Railway)

1. **Go to Railway Dashboard:**
   - Your backend service → Variables

2. **Add Environment Variable:**
   - **Key:** `GOOGLE_CLIENT_ID`
   - **Value:** Your Google Client ID (same as frontend)
   - Click "Save"

3. **Railway will auto-redeploy**

---

## ✅ Testing

1. **Go to your login page**
2. **You should see:** "Sign in with Google" button
3. **Click it:**
   - Google sign-in popup appears
   - Select your Google account
   - Grant permissions
4. **Result:**
   - New users: Account created automatically, logged in
   - Existing users: Logged in immediately
   - Redirected to dashboard

---

## 🎨 UI Features

- **Google Sign-In Button:**
  - Appears above email/password form
  - Styled to match your app
  - "or" divider between Google and email login

- **User Experience:**
  - One-click login
  - No email verification needed
  - Seamless account creation

---

## 📋 Environment Variables Checklist

### Frontend (Vercel):
- [ ] `REACT_APP_GOOGLE_CLIENT_ID` = Your Google Client ID

### Backend (Railway):
- [ ] `GOOGLE_CLIENT_ID` = Your Google Client ID (same as frontend)

---

## 🆘 Troubleshooting

### Google Button Not Showing?

1. **Check Environment Variable:**
   - Make sure `REACT_APP_GOOGLE_CLIENT_ID` is set in Vercel
   - Redeploy frontend

2. **Check Browser Console:**
   - Look for errors
   - Make sure Google script loaded

### "Invalid Client ID" Error?

1. **Check Client ID:**
   - Make sure it matches in both frontend and backend
   - No extra spaces or characters

2. **Check Authorized Origins:**
   - Make sure your frontend URL is in authorized origins
   - Check both `http://localhost:3000` and production URL

### "OAuth is not configured" Error?

1. **Check Backend Variable:**
   - Make sure `GOOGLE_CLIENT_ID` is set in Railway
   - Redeploy backend

### Button Shows But Click Does Nothing?

1. **Check Google Script:**
   - Make sure script loaded in `index.html`
   - Check browser console for errors

2. **Check Client ID:**
   - Verify it's correct
   - Make sure it's for "Web application" type

---

## 🎉 Benefits

- ✅ **No email verification** - Google emails are pre-verified
- ✅ **Better UX** - One-click login
- ✅ **More secure** - Google handles authentication
- ✅ **Faster registration** - No code entry needed
- ✅ **Professional** - Industry standard

---

## 📝 Code Changes Made

### Backend:
- Added `/api/auth/google` endpoint
- Google token verification
- Automatic user creation/login
- Added `google-auth` library

### Frontend:
- Added Google Sign-In script to `index.html`
- Added Google login button
- Added login handler
- Added styling

---

**Once you add the Google Client ID to Vercel and Railway, Google OAuth will work!** 🚀

