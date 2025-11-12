# Email Configuration Guide

This guide explains how to configure email for sending verification codes in the Electricity Logger application.

## ⚠️ About ProtonMail

**ProtonMail does NOT support SMTP access** for regular accounts. ProtonMail Bridge is available but requires:
- Running a local application on your server
- Complex setup and maintenance
- Not suitable for cloud/deployed applications

**Recommendation:** Use a standard email provider with SMTP support instead.

---

## 📧 Recommended Email Providers

### 1. **Gmail** (Recommended for Development)
- ✅ Free
- ✅ Easy to set up
- ✅ Reliable
- ⚠️ Daily sending limits (500 emails/day for free accounts)

### 2. **Outlook/Hotmail** (Good Alternative)
- ✅ Free
- ✅ Easy to set up
- ✅ Good reliability
- ⚠️ Daily sending limits (300 emails/day)

### 3. **Yahoo Mail** (Alternative)
- ✅ Free
- ✅ SMTP support
- ⚠️ Lower daily limits

### 4. **SendGrid** (Recommended for Production)
- ✅ Free tier: 100 emails/day
- ✅ Excellent for production
- ✅ High deliverability
- ✅ Detailed analytics

### 5. **Mailgun** (Good for Production)
- ✅ Free tier: 5,000 emails/month
- ✅ Excellent API
- ✅ Good for production

---

## 🔧 Setup Instructions

### Option 1: Gmail Setup (Recommended for Development)

#### Step 1: Enable 2-Factor Authentication
1. Go to [Google Account Security](https://myaccount.google.com/security)
2. Enable "2-Step Verification"
3. Complete the setup process

#### Step 2: Create an App Password
1. Go to [Google App Passwords](https://myaccount.google.com/apppasswords)
2. Select "Mail" as the app
3. Select "Other (Custom name)" as the device
4. Enter "Electricity Logger" as the name
5. Click "Generate"
6. **Copy the 16-character password** (you'll need this)

#### Step 3: Configure Backend
Create or update `backend/.env` file:

```env
# Email Configuration (Gmail)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-16-character-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

**Important:** Use the **App Password**, NOT your regular Gmail password!

---

### Option 2: Outlook/Hotmail Setup

#### Step 1: Enable App Password
1. Go to [Microsoft Account Security](https://account.microsoft.com/security)
2. Enable "Two-step verification"
3. Go to "App passwords"
4. Create a new app password for "Mail"
5. Copy the password

#### Step 2: Configure Backend
Update `backend/.env`:

```env
# Email Configuration (Outlook)
MAIL_SERVER=smtp-mail.outlook.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@outlook.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@outlook.com
```

---

### Option 3: Yahoo Mail Setup

#### Step 1: Generate App Password
1. Go to [Yahoo Account Security](https://login.yahoo.com/account/security)
2. Enable "Two-step verification"
3. Generate an app password
4. Copy the password

#### Step 2: Configure Backend
Update `backend/.env`:

```env
# Email Configuration (Yahoo)
MAIL_SERVER=smtp.mail.yahoo.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@yahoo.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@yahoo.com
```

---

### Option 4: SendGrid Setup (Recommended for Production)

#### Step 1: Create SendGrid Account
1. Go to [SendGrid](https://sendgrid.com/)
2. Sign up for a free account
3. Verify your email address

#### Step 2: Create API Key
1. Go to Settings → API Keys
2. Click "Create API Key"
3. Name it "Electricity Logger"
4. Select "Full Access" or "Restricted Access" with Mail Send permissions
5. Copy the API key

#### Step 3: Verify Sender Identity
1. Go to Settings → Sender Authentication
2. Verify a Single Sender (for development) or Domain (for production)
3. Follow the verification steps

#### Step 4: Configure Backend
Update `backend/.env`:

```env
# Email Configuration (SendGrid)
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=apikey
MAIL_PASSWORD=your-sendgrid-api-key
MAIL_DEFAULT_SENDER=your-verified-email@yourdomain.com
```

**Note:** For SendGrid, `MAIL_USERNAME` is always `apikey` and `MAIL_PASSWORD` is your API key.

---

### Option 5: Mailgun Setup (Good for Production)

#### Step 1: Create Mailgun Account
1. Go to [Mailgun](https://www.mailgun.com/)
2. Sign up for a free account
3. Verify your email

#### Step 2: Get SMTP Credentials
1. Go to Sending → Domain Settings
2. Use the sandbox domain for testing, or add your own domain
3. Go to SMTP credentials
4. Create SMTP credentials or use the default ones
5. Copy the username and password

#### Step 3: Configure Backend
Update `backend/.env`:

```env
# Email Configuration (Mailgun)
MAIL_SERVER=smtp.mailgun.org
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=postmaster@your-domain.mailgun.org
MAIL_PASSWORD=your-mailgun-password
MAIL_DEFAULT_SENDER=noreply@your-domain.com
```

---

## 🔒 Security Best Practices

1. **Never commit `.env` file to Git**
   - The `.env` file is already in `.gitignore`
   - Always use environment variables in production

2. **Use App Passwords, not regular passwords**
   - Gmail, Outlook, and Yahoo require app passwords
   - Regular passwords won't work with 2FA enabled

3. **Rotate passwords regularly**
   - Change app passwords every 90 days
   - Update them in your `.env` file

4. **Use environment variables in production**
   - Set environment variables in your hosting platform
   - Never hardcode credentials

---

## 🧪 Testing Email Configuration

### Test Locally

1. Start your backend server:
   ```bash
   cd backend
   python app.py
   ```

2. Try to register a new user with a valid email address

3. Check your email inbox for the verification code

4. Check the backend console for any error messages

### Troubleshooting

#### Error: "Authentication failed"
- **Gmail/Outlook/Yahoo:** Make sure you're using an App Password, not your regular password
- **SendGrid/Mailgun:** Verify your API key/credentials are correct

#### Error: "Connection timeout"
- Check your firewall settings
- Verify the SMTP server and port are correct
- Try port 465 with SSL instead of 587 with TLS

#### Emails not arriving
- Check spam/junk folder
- Verify the email address is correct
- Check email provider's sending limits
- Verify sender email is authenticated (for SendGrid/Mailgun)

#### Error: "SMTP server not responding"
- Check internet connection
- Verify SMTP server address is correct
- Try different ports (587 for TLS, 465 for SSL)

---

## 📝 Environment Variables Reference

```env
# Required Email Configuration
MAIL_SERVER=smtp.gmail.com          # SMTP server address
MAIL_PORT=587                       # SMTP port (587 for TLS, 465 for SSL)
MAIL_USE_TLS=true                   # Use TLS (true for port 587, false for port 465)
MAIL_USERNAME=your-email@gmail.com  # Your email or API username
MAIL_PASSWORD=your-password         # App password or API key
MAIL_DEFAULT_SENDER=your-email@gmail.com  # Default sender email
```

---

## 🚀 Production Deployment

### Heroku
```bash
heroku config:set MAIL_SERVER=smtp.sendgrid.net
heroku config:set MAIL_PORT=587
heroku config:set MAIL_USE_TLS=true
heroku config:set MAIL_USERNAME=apikey
heroku config:set MAIL_PASSWORD=your-sendgrid-api-key
heroku config:set MAIL_DEFAULT_SENDER=noreply@yourdomain.com
```

### Vercel/Railway/Render
Set environment variables in your platform's dashboard using the same variable names.

---

## 📊 Email Provider Comparison

| Provider | Free Tier | Setup Difficulty | Best For |
|----------|-----------|------------------|----------|
| Gmail | 500/day | Easy | Development |
| Outlook | 300/day | Easy | Development |
| Yahoo | 500/day | Easy | Development |
| SendGrid | 100/day | Medium | Production |
| Mailgun | 5,000/month | Medium | Production |

---

## ❓ FAQ

### Q: Can I use ProtonMail?
**A:** No, ProtonMail doesn't support SMTP for regular accounts. Use Gmail, Outlook, or a transactional email service instead.

### Q: Why do I need an App Password?
**A:** Modern email providers require 2FA for security. App Passwords allow applications to send emails without compromising your main account password.

### Q: What if I don't want to set up email?
**A:** The app will still work, but verification codes will be printed to the console instead of sent via email. This is fine for development but not recommended for production.

### Q: Can I use multiple email providers?
**A:** The current setup supports one email provider at a time. You can switch providers by updating the `.env` file.

### Q: How do I test without sending real emails?
**A:** For development, you can use a service like [Mailtrap](https://mailtrap.io/) which captures emails without sending them.

---

## 🔗 Useful Links

- [Gmail App Passwords](https://myaccount.google.com/apppasswords)
- [Outlook App Passwords](https://account.microsoft.com/security)
- [SendGrid Documentation](https://docs.sendgrid.com/)
- [Mailgun Documentation](https://documentation.mailgun.com/)
- [Flask-Mail Documentation](https://pythonhosted.org/Flask-Mail/)

---

## 💡 Quick Start (Gmail)

1. Enable 2FA on your Google account
2. Create an App Password: https://myaccount.google.com/apppasswords
3. Update `backend/.env`:
   ```env
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=true
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=xxxx xxxx xxxx xxxx
   MAIL_DEFAULT_SENDER=your-email@gmail.com
   ```
4. Restart your backend server
5. Test by registering a new user

That's it! Your email should now work. 🎉

