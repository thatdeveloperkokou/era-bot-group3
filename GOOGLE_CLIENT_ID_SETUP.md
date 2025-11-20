# Google OAuth Client ID Setup

## ✅ Your Google OAuth Credentials

**Client ID:** `YOUR_CLIENT_ID_HERE` (Get this from Google Cloud Console)

**Client Secret:** `YOUR_CLIENT_SECRET_HERE` (not needed for our implementation, but keep it secure)

---

## 🔧 Setup Steps

### Step 1: Add to Railway (Backend) ✅

I've already set this for you! The Client ID has been added to Railway.

**Verify:**
```bash
railway variables | findstr GOOGLE
```

Should show: `GOOGLE_CLIENT_ID=YOUR_CLIENT_ID_HERE`

---

### Step 2: Add to Vercel (Frontend)

1. **Go to Vercel Dashboard:**
   - Your frontend project → **Settings** → **Environment Variables**

2. **Add Environment Variable:**
   - **Key:** `REACT_APP_GOOGLE_CLIENT_ID`
   - **Value:** `YOUR_CLIENT_ID_HERE` (Your actual Client ID from Google Cloud Console)
   - **Environment:** Select all (Production, Preview, Development)
   - Click **"Save"**

3. **Redeploy Frontend:**
   - Vercel will auto-redeploy
   - Or manually trigger redeploy from Deployments tab

---

### Step 3: Verify Authorized Origins

Make sure your frontend URLs are in Google OAuth settings:

1. **Go to Google Cloud Console:**
   - https://console.cloud.google.com
   - APIs & Services → Credentials
   - Click on your OAuth 2.0 Client ID

2. **Check Authorized JavaScript origins:**
   - Should include:
     - `http://localhost:3000` (for local development)
     - `https://your-frontend-domain.vercel.app` (your Vercel URL)

3. **Check Authorized redirect URIs:**
   - Should include:
     - `http://localhost:3000`
     - `https://your-frontend-domain.vercel.app`

---

## 📋 Quick Checklist

- [x] Client ID added to Railway (Backend) ✅
- [ ] Client ID added to Vercel (Frontend) - **DO THIS NOW**
- [ ] Authorized origins configured in Google Console
- [ ] Frontend redeployed
- [ ] Test Google Sign-In button

---

## 🎯 What You Need

**For our implementation, you only need:**
- ✅ **Client ID** (for both frontend and backend)
- ❌ **Client Secret** (not needed - we use client-side flow)

---

## 🧪 Testing

After adding to Vercel and redeploying:

1. **Go to your login page**
2. **You should see:** "Sign in with Google" button
3. **Click it:**
   - Google popup appears
   - Select your account
   - For new users: Location form appears
   - For existing users: Immediate login

---

## 🆘 Troubleshooting

### Button Not Showing?

1. **Check Vercel Environment Variable:**
   - Make sure `REACT_APP_GOOGLE_CLIENT_ID` is set
   - Redeploy frontend

2. **Check Browser Console:**
   - Look for errors
   - Check if Google script loaded

### "Invalid Client ID" Error?

1. **Check Authorized Origins:**
   - Make sure your frontend URL is in authorized origins
   - Check both localhost and production URL

2. **Check Environment Variable:**
   - Make sure Client ID matches exactly
   - No extra spaces or characters

---

## ✅ Next Steps

1. **Add Client ID to Vercel** (see Step 2 above)
2. **Redeploy frontend**
3. **Test Google Sign-In**
4. **Done!** 🎉

---

**Your Google OAuth is almost ready! Just add the Client ID to Vercel and you're done!** 🚀

