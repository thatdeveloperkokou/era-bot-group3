# Fix "Invalid Google token" Error

## 🚨 The Error

**Error:** "Invalid Google token"  
**When:** Trying to sign in with Gmail/Google OAuth

This error occurs when the backend cannot verify the Google ID token sent from the frontend.

---

## ✅ Quick Fix Checklist

### 1. Check Client ID Match (MOST COMMON ISSUE)

The **GOOGLE_CLIENT_ID** in your backend must **exactly match** the **REACT_APP_GOOGLE_CLIENT_ID** in your frontend.

**Backend (Railway):**
1. Go to Railway Dashboard → Your Backend Service → Variables
2. Check `GOOGLE_CLIENT_ID` value
3. Copy the full Client ID (looks like: `123456789-abcdefghijklmnop.apps.googleusercontent.com`)

**Frontend (Vercel):**
1. Go to Vercel Dashboard → Your Frontend Project → Settings → Environment Variables
2. Check `REACT_APP_GOOGLE_CLIENT_ID` value
3. **Must be EXACTLY the same** as backend Client ID

**Fix:**
- If they don't match, update one to match the other
- Redeploy both frontend and backend
- Wait 2-3 minutes for changes to propagate

---

### 2. Check Backend Logs

The improved error logging will now show more details:

1. **Go to Railway Dashboard** → Your Backend Service → Deployments → View Logs
2. **Look for these messages:**
   - `🔍 Verifying Google token with Client ID: ...`
   - `❌ Google token verification failed: ...`
3. **Check the error message** - it will tell you:
   - If token expired: "Google token has expired. Please try signing in again."
   - If Client ID mismatch: "Client ID mismatch. The Google Client ID in the backend does not match..."
   - The actual error from Google

---

### 3. Verify Google Cloud Console Configuration

1. **Go to Google Cloud Console:**
   - https://console.cloud.google.com
   - APIs & Services → Credentials
   - Click on your OAuth 2.0 Client ID

2. **Check Authorized JavaScript origins:**
   - Must include your frontend URL (e.g., `https://your-app.vercel.app`)
   - Must include `http://localhost:3000` for local development
   - **No trailing slashes**

3. **Check Authorized redirect URIs:**
   - Same URLs as above
   - Must match exactly (case-sensitive)

---

### 4. Token Expiration

Google ID tokens expire quickly (usually within 1 hour, but can be shorter).

**If you see "Token expired" error:**
- This is normal - just try signing in again
- The token will be refreshed automatically

---

## 🔍 Detailed Troubleshooting Steps

### Step 1: Verify Environment Variables

**Backend (Railway):**
```bash
# Check if GOOGLE_CLIENT_ID is set
railway variables | findstr GOOGLE
```

Should show: `GOOGLE_CLIENT_ID=your-client-id-here`

**Frontend (Vercel):**
- Go to Vercel Dashboard → Settings → Environment Variables
- Check `REACT_APP_GOOGLE_CLIENT_ID` is set
- Value should match backend exactly

---

### Step 2: Check Backend Logs

After trying to sign in, check Railway logs for:

```
🔍 Verifying Google token with Client ID: 123456789-abc...
❌ Google token verification failed: [error message]
```

The error message will tell you exactly what's wrong:
- **"Token expired"** → Just try again
- **"audience mismatch"** or **"client_id mismatch"** → Client IDs don't match
- **"Invalid token"** → Token format issue or Client ID wrong

---

### Step 3: Verify Client IDs Match

**Critical:** Both must be the **exact same value**:

1. **Backend:** Railway → Variables → `GOOGLE_CLIENT_ID`
2. **Frontend:** Vercel → Environment Variables → `REACT_APP_GOOGLE_CLIENT_ID`

**They must match character-for-character!**

---

### Step 4: Check Google Cloud Console

1. **Go to:** https://console.cloud.google.com
2. **Navigate to:** APIs & Services → Credentials
3. **Click your OAuth 2.0 Client ID**
4. **Verify:**
   - Authorized JavaScript origins includes your frontend URL
   - Authorized redirect URIs includes your frontend URL
   - Client ID matches what you have in Railway/Vercel

---

### Step 5: Redeploy Everything

After making changes:

1. **Redeploy Backend (Railway):**
   - Changes to environment variables trigger auto-redeploy
   - Or manually redeploy from Deployments tab

2. **Redeploy Frontend (Vercel):**
   - Changes to environment variables trigger auto-redeploy
   - Or manually redeploy from Deployments tab

3. **Wait 2-3 minutes** for changes to propagate

4. **Clear browser cache** and try again

---

## 🎯 Common Error Messages & Solutions

### "Google token has expired"
**Solution:** Just try signing in again. Tokens expire quickly.

### "Client ID mismatch"
**Solution:** 
1. Check Railway `GOOGLE_CLIENT_ID` matches Vercel `REACT_APP_GOOGLE_CLIENT_ID`
2. Update one to match the other
3. Redeploy both services

### "Invalid Google token"
**Solution:**
1. Check backend logs for detailed error
2. Verify Client IDs match exactly
3. Check Google Cloud Console authorized origins
4. Make sure frontend URL is in authorized origins

### "Google OAuth is not configured"
**Solution:**
1. Check `GOOGLE_CLIENT_ID` is set in Railway
2. Redeploy backend

---

## ✅ Verification Steps

After fixing, verify:

1. **Backend logs show:**
   ```
   🔍 Verifying Google token with Client ID: ...
   ✅ Token verified successfully. Email: ...
   ```

2. **Frontend:**
   - Click "Sign in with Google"
   - Google popup appears
   - Select account
   - Either logs in or shows location form (for new users)

3. **No error messages** in browser console or backend logs

---

## 🆘 Still Not Working?

1. **Check backend logs** - The improved logging will show the exact error
2. **Verify Client IDs match** - This is the #1 cause
3. **Check Google Cloud Console** - Authorized origins must include your frontend URL
4. **Redeploy both services** - After any environment variable changes
5. **Wait 2-3 minutes** - For changes to propagate
6. **Clear browser cache** - Old tokens might be cached

---

## 📝 Quick Reference

**Backend Environment Variable:**
- Key: `GOOGLE_CLIENT_ID`
- Location: Railway → Variables

**Frontend Environment Variable:**
- Key: `REACT_APP_GOOGLE_CLIENT_ID`
- Location: Vercel → Settings → Environment Variables

**Both must be the exact same value!**

---

**The most common fix is ensuring the Client IDs match exactly between frontend and backend!** 🚀

