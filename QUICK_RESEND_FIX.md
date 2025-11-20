# Quick Fix: Resend Email Not Sending

## The Issue

You're seeing "Email sending failed. Use the code shown below" even though API requests return 200. This means:
- ✅ Registration is working
- ✅ Verification code is being created
- ❌ Resend API is not sending emails

## ✅ Quick Fix

### Step 1: Add RESEND_API_KEY to Railway

1. **Go to Railway Dashboard:**
   - Navigate to your backend service
   - Click **Variables** tab

2. **Add RESEND_API_KEY:**
   - Click **New Variable**
   - **Key:** `RESEND_API_KEY`
   - **Value:** `re_ZxeVdayV_LVMMnbD6VXC3CQHjNr9ccQYN`
   - Click **Save**

3. **Add RESEND_FROM_EMAIL (Optional):**
   - **Key:** `RESEND_FROM_EMAIL`
   - **Value:** `onboarding@resend.dev` (default)
   - Or use your verified domain email
   - Click **Save**

4. **Redeploy:**
   - Railway will auto-redeploy
   - Or manually trigger redeploy

### Step 2: Verify in Logs

After redeploying, check Railway logs:

1. **Go to Railway → Backend Service → Deployments → Latest → Logs**

2. **Look for:**
   - `📧 Resend config check: RESEND_API_KEY=SET`
   - `✅ Verification email sent successfully`

3. **If you see errors:**
   - Check the error message
   - Verify API key is correct
   - Check Resend dashboard for API key status

### Step 3: Test Again

1. **Register a new user**
2. **Check your email** - should receive verification code
3. **Check Railway logs** - should show success message

## 🔍 Troubleshooting

### Still Showing Fallback Code?

**Check Railway Logs:**
- Look for: `⚠️ RESEND_API_KEY not configured`
- If you see this → API key is not set correctly

**Verify API Key:**
- Go to Resend Dashboard → API Keys
- Make sure the key is active
- Copy the full key (starts with `re_`)

**Check Variable Name:**
- Must be exactly: `RESEND_API_KEY` (case-sensitive)
- No spaces or extra characters

### Resend API Error?

**Common Errors:**
- `401 Unauthorized` → API key is invalid
- `403 Forbidden` → API key doesn't have email send permission
- `422 Validation Error` → Email address or from address is invalid

**Solutions:**
1. Verify API key in Resend dashboard
2. Check `RESEND_FROM_EMAIL` is valid
3. Make sure recipient email is valid

### Check Resend Dashboard

1. **Go to:** https://resend.com/emails
2. **Check Logs:**
   - See if emails are being sent
   - Check delivery status
   - See any error messages

## ✅ Expected Behavior After Fix

**In Railway Logs:**
```
📧 Resend config check: RESEND_API_KEY=SET, RESEND_FROM_EMAIL=onboarding@resend.dev
📧 Sending email via Resend API to user@email.com...
✅ Verification email sent successfully to user@email.com
   Resend email ID: abc123...
```

**In Frontend:**
- No "Email sending failed" message
- User receives email with verification code
- No fallback code shown

## 🎯 Quick Checklist

- [ ] `RESEND_API_KEY` is set in Railway
- [ ] API key value is correct (starts with `re_`)
- [ ] Backend has been redeployed after adding variable
- [ ] Check Railway logs for success messages
- [ ] Test registration and check email inbox

---

**Your API Key:** `re_ZxeVdayV_LVMMnbD6VXC3CQHjNr9ccQYN`

Just add it to Railway and you're done! 🚀

