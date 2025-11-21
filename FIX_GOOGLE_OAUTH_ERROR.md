# Fix Google OAuth "no registered origin" Error

## 🚨 The Error

**Error:** "Access blocked: Authorization Error - no registered origin"  
**Error 401:** invalid_client

This means your frontend URL is not in Google's authorized origins list.

---

## ✅ Solution: Add Authorized Origins in Google Cloud Console

### Step 1: Go to Google Cloud Console

1. **Visit:** https://console.cloud.google.com
2. **Select your project** (the one where you created the OAuth client)
3. **Go to:** APIs & Services → **Credentials**
4. **Click on your OAuth 2.0 Client ID:**
   - Client ID: `847715031800-ngeofddh32pq0i2n78v85pfsp613tniv.apps.googleusercontent.com`

### Step 2: Add Authorized JavaScript Origins

1. **Find "Authorized JavaScript origins"** section
2. **Click "Add URI"** or the **+** button
3. **Add these URLs:**

   **For Production:**
   - `https://era-bot-group3-nx3x.vercel.app` (or your actual Vercel URL)
   - Check your Vercel dashboard for the exact URL

   **For Development:**
   - `http://localhost:3000`

4. **Click "Save"**

### Step 3: Add Authorized Redirect URIs (if needed)

1. **Find "Authorized redirect URIs"** section
2. **Click "Add URI"**
3. **Add the same URLs:**
   - `https://era-bot-group3-nx3x.vercel.app` (your Vercel URL)
   - `http://localhost:3000`

4. **Click "Save"**

---

## 🔍 How to Find Your Vercel URL

1. **Go to Vercel Dashboard:**
   - https://vercel.com/dashboard
   - Select your frontend project

2. **Check the URL:**
   - Look at the project overview
   - The URL will be something like: `https://your-project-name.vercel.app`
   - Or check the "Domains" section

3. **Copy the exact URL** (including `https://`)

---

## 📋 Quick Checklist

- [ ] Go to Google Cloud Console
- [ ] Open your OAuth 2.0 Client ID
- [ ] Add Vercel URL to "Authorized JavaScript origins"
- [ ] Add `http://localhost:3000` to "Authorized JavaScript origins"
- [ ] Add same URLs to "Authorized redirect URIs"
- [ ] Click "Save"
- [ ] Wait 1-2 minutes for changes to propagate
- [ ] Try Google Sign-In again

---

## 🎯 Example Configuration

**Authorized JavaScript origins:**
```
http://localhost:3000
https://era-bot-group3-nx3x.vercel.app
```

**Authorized redirect URIs:**
```
http://localhost:3000
https://era-bot-group3-nx3x.vercel.app
```

**Important:**
- ✅ Must include `http://` or `https://`
- ✅ No trailing slash
- ✅ Exact match with your frontend URL

---

## ⏱️ After Saving

1. **Wait 1-2 minutes** for changes to propagate
2. **Refresh your frontend page**
3. **Try Google Sign-In again**

---

## 🆘 Still Not Working?

### Check Your Vercel URL:

1. **Go to Vercel Dashboard**
2. **Check the exact URL** of your deployment
3. **Make sure it matches** what you added in Google Console
4. **Case-sensitive:** URLs must match exactly

### Check Browser Console:

1. **Open browser DevTools** (F12)
2. **Go to Console tab**
3. **Look for errors:**
   - Should see Google script loading
   - Check for any error messages

### Verify Client ID:

1. **Check Vercel Environment Variable:**
   - Make sure `REACT_APP_GOOGLE_CLIENT_ID` is set
   - Value should be: `847715031800-ngeofddh32pq0i2n78v85pfsp613tniv.apps.googleusercontent.com`

2. **Check Railway Environment Variable:**
   - Make sure `GOOGLE_CLIENT_ID` is set
   - Same value as above

---

## ✅ Expected Result

After adding the authorized origins:

1. **Click "Sign in with Google"**
2. **Google popup appears** (no error)
3. **Select your account**
4. **For new users:** Location form appears
5. **For existing users:** Immediate login
6. **Redirected to dashboard** ✅

---

**Add your Vercel URL to Google's authorized origins and the error will be fixed!** 🚀

