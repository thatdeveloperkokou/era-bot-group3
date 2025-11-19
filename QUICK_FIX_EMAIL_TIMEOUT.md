# Quick Fix: Email Timeout Issue

## The Problem
Registration is hanging at "📧 Attempting to send verification email" because the email sending is timing out.

## ✅ Quick Fix (30 seconds)

### Option 1: Disable Email Sending Temporarily (Recommended)

1. Go to Railway Dashboard → Your Backend Service
2. Go to **Variables** tab
3. Add or update:
   - **Key:** `MAIL_SUPPRESS_SEND`
   - **Value:** `true`
4. Railway will auto-redeploy

**Result:** Registration will work immediately, but emails won't be sent. Verification codes will be printed in Railway logs instead.

### Option 2: Configure Email Properly

If you want emails to work, you need to configure email settings in Railway:

1. Go to Railway Dashboard → Your Backend Service → **Variables**
2. Add these variables:
   - `MAIL_SERVER=smtp.gmail.com` (or your email provider)
   - `MAIL_PORT=587`
   - `MAIL_USE_TLS=true`
   - `MAIL_USERNAME=your-email@gmail.com`
   - `MAIL_PASSWORD=your-app-password` (use App Password for Gmail)
   - `MAIL_DEFAULT_SENDER=your-email@gmail.com`

**Note:** For Gmail, you need to use an App Password, not your regular password.

## What Happens Now

After setting `MAIL_SUPPRESS_SEND=true`:
- Registration will complete successfully ✅
- Verification codes will be printed in Railway logs
- Users can check the logs to get their verification code
- You can configure email later when ready

## Check Railway Logs

After registration, check Railway logs. You should see:
```
📧 MAIL_SUPPRESS_SEND enabled. Skipping actual email send for user@email.com. Verification code: 123456
```

The user can use this code to verify their email.

## Configure Email Later

When you're ready to enable email:
1. Set up email credentials (see EMAIL_SETUP.md)
2. Set `MAIL_SUPPRESS_SEND=false` or remove it
3. Redeploy

