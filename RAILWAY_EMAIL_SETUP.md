# Railway Email Setup Guide

## Quick Setup for Railway

### Step 1: Choose Your Email Provider

**For Development/Testing:**
- **Gmail** (easiest, 500 emails/day free)
- **Outlook** (300 emails/day free)

**For Production:**
- **SendGrid** (100 emails/day free, recommended)
- **Mailgun** (5,000 emails/month free)

### Step 2: Get Your Email Credentials

#### Option A: Gmail (Easiest for Testing)

1. **Enable 2-Factor Authentication:**
   - Go to [Google Account Security](https://myaccount.google.com/security)
   - Enable "2-Step Verification"

2. **Create App Password:**
   - Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
   - Select "Mail" → "Other (Custom name)"
   - Name it "Railway App"
   - Copy the 16-character password (looks like: `abcd efgh ijkl mnop`)

3. **Add to Railway:**
   - Go to your Railway backend service
   - Go to **"Variables"** tab
   - Add these variables:

```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=abcdefghijklmnop  (your 16-character app password, no spaces)
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

#### Option B: SendGrid (Recommended for Production)

1. **Create SendGrid Account:**
   - Go to [SendGrid](https://sendgrid.com/)
   - Sign up for free account
   - Verify your email

2. **Create API Key:**
   - Go to Settings → API Keys
   - Click "Create API Key"
   - Name: "Railway App"
   - Permissions: "Full Access" or "Restricted Access" with Mail Send
   - Copy the API key (you'll only see it once!)

3. **Verify Sender:**
   - Go to Settings → Sender Authentication
   - Verify a Single Sender (for testing)
   - Use the verified email as MAIL_DEFAULT_SENDER

4. **Add to Railway:**
   - Go to your Railway backend service
   - Go to **"Variables"** tab
   - Add these variables:

```
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=apikey
MAIL_PASSWORD=your-sendgrid-api-key-here
MAIL_DEFAULT_SENDER=your-verified-email@example.com
```

**Important:** For SendGrid, `MAIL_USERNAME` must be exactly `apikey` (not your email!)

### Step 3: Add Variables to Railway

1. Go to your Railway project dashboard
2. Click on your **backend service**
3. Go to **"Variables"** tab
4. Click **"New Variable"** for each variable
5. Add all 6 variables:
   - `MAIL_SERVER`
   - `MAIL_PORT`
   - `MAIL_USE_TLS`
   - `MAIL_USERNAME`
   - `MAIL_PASSWORD`
   - `MAIL_DEFAULT_SENDER`

### Step 4: Redeploy

- Railway will automatically redeploy when you add variables
- Or manually trigger a redeploy

### Step 5: Test

1. Try registering a new user
2. Check the Railway logs for email sending status
3. Check your email inbox (and spam folder)

## Troubleshooting

### Check Railway Logs

1. Go to your Railway backend service
2. Click on **"Deployments"** tab
3. Click on the latest deployment
4. Check the logs for email-related messages

### Common Issues

#### "Email not configured"
- **Solution:** Make sure all 6 email variables are set in Railway
- Check that `MAIL_USERNAME` and `MAIL_PASSWORD` are not empty

#### "Authentication failed" (Error 535/534)
- **Gmail/Outlook:** Make sure you're using an **App Password**, not your regular password
- **SendGrid:** Make sure `MAIL_USERNAME=apikey` (exactly) and `MAIL_PASSWORD` is your API key

#### "Connection timeout" or "Connection refused"
- Check `MAIL_SERVER` and `MAIL_PORT` are correct
- For Gmail: `smtp.gmail.com:587`
- For SendGrid: `smtp.sendgrid.net:587`

#### Emails not arriving
- Check spam/junk folder
- Verify `MAIL_DEFAULT_SENDER` is correct
- For SendGrid: Make sure sender email is verified

### Verify Configuration

After adding variables, check the Railway logs. You should see:
- `✅ Verification email sent successfully to [email]`

If you see errors, the logs will show detailed information about what's wrong.

## Quick Reference

### Gmail Settings
```
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-char-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

### SendGrid Settings
```
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=apikey
MAIL_PASSWORD=your-api-key
MAIL_DEFAULT_SENDER=verified-email@example.com
```

### Outlook Settings
```
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@outlook.com
```

## Need More Help?

See `backend/EMAIL_SETUP.md` for detailed instructions for all email providers.

