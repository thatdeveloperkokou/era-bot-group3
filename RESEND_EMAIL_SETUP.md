# Resend Email Setup Guide

Resend is a modern email API service that works perfectly with Railway and other cloud platforms. It's much more reliable than SMTP for cloud deployments.

## ✅ Quick Setup

### Step 1: Get Your Resend API Key

1. Go to [Resend Dashboard](https://resend.com)
2. Sign up or log in
3. Go to **API Keys** section
4. Click **Create API Key**
5. Copy your API key (starts with `re_`)

**Your API Key:** `re_ZxeVdayV_LVMMnbD6VXC3CQHjNr9ccQYN` ✅

### Step 2: Set Up in Railway

1. **Go to Railway Dashboard:**
   - Navigate to your backend service
   - Go to **Variables** tab

2. **Add Environment Variables:**
   - **Key:** `RESEND_API_KEY`
   - **Value:** `re_ZxeVdayV_LVMMnbD6VXC3CQHjNr9ccQYN`
   
   - **Key:** `RESEND_FROM_EMAIL`
   - **Value:** `onboarding@resend.dev` (default) or your verified domain email

3. **Remove Old SMTP Variables (if any):**
   - You can remove: `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD`
   - These are no longer needed with Resend

4. **Save and Redeploy:**
   - Railway will automatically redeploy
   - Check logs to verify email sending works

### Step 3: Verify Domain (Optional but Recommended)

For production, you should verify your own domain:

1. **In Resend Dashboard:**
   - Go to **Domains**
   - Click **Add Domain**
   - Follow verification steps

2. **Update RESEND_FROM_EMAIL:**
   - Use your verified domain email
   - Example: `noreply@yourdomain.com`

## 🧪 Testing

After setup, test email verification:

1. **Register a new user** with your email
2. **Check your inbox** for verification code
3. **Check Railway logs** for email sending status

## 📊 Resend Features

- ✅ **100 emails/day free** (perfect for development)
- ✅ **No SMTP blocking** (works with Railway)
- ✅ **Fast delivery** (API-based, not SMTP)
- ✅ **Better reliability** (no connection timeouts)
- ✅ **Easy setup** (just API key)

## 🔧 Environment Variables

**Required:**
```
RESEND_API_KEY=re_your_api_key_here
```

**Optional:**
```
RESEND_FROM_EMAIL=onboarding@resend.dev  # Default Resend email
# Or use your verified domain:
RESEND_FROM_EMAIL=noreply@yourdomain.com
```

## 🆘 Troubleshooting

### Emails Not Sending

1. **Check API Key:**
   - Verify `RESEND_API_KEY` is set correctly
   - Make sure it starts with `re_`
   - Check it's not expired in Resend dashboard

2. **Check Logs:**
   - Railway logs should show: `✅ Verification email sent successfully`
   - If you see errors, check the error message

3. **Check Resend Dashboard:**
   - Go to Resend → **Logs**
   - See if emails are being sent
   - Check for any errors or bounces

### API Key Invalid

- Verify the key in Resend dashboard
- Make sure it's the full key (starts with `re_`)
- Check if key has been revoked

### Domain Not Verified

- If using custom domain, verify it in Resend
- Or use `onboarding@resend.dev` for testing

## 📝 Migration from SMTP

If you were using SMTP before:

1. **Add Resend variables** (as shown above)
2. **Remove SMTP variables:**
   - `MAIL_SERVER`
   - `MAIL_PORT`
   - `MAIL_USERNAME`
   - `MAIL_PASSWORD`
   - `MAIL_DEFAULT_SENDER`
3. **Redeploy backend**
4. **Test email verification**

## ✅ Benefits Over SMTP

- **No port blocking** - Railway doesn't block API calls
- **Faster** - API is faster than SMTP
- **More reliable** - No connection timeouts
- **Better tracking** - See email status in Resend dashboard
- **Easier setup** - Just one API key

---

**Your Resend API Key is already configured in the code!** Just add it to Railway environment variables and you're good to go! 🚀

