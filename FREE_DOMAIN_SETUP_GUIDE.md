# Complete Guide: Get Free Domain & Set Up Email with Resend

## 🎯 Goal
Get a free domain, verify it with Resend, and enable email delivery for your app.

## Step 1: Get a Free Domain

### Option A: Dot TK (Recommended - Most Reliable) ⭐

1. **Go to Dot TK:**
   - Visit: https://www.dot.tk
   - This is the official Tokelau registry (more reliable than Freenom)

2. **Search for a Domain:**
   - Enter a name you want (e.g., `electricitylogger`)
   - Click **"Search"** or **"Check Availability"**

3. **Register Domain:**
   - If available, click **"Get it now"** or **"Register"**
   - Create free account
   - Complete registration

4. **Access Domain Management:**
   - Log in to your account
   - Go to **"My Domains"** or domain management
   - Full DNS control available

**Why Dot TK?**
- ✅ More reliable than Freenom
- ✅ Direct from registry
- ✅ Full DNS control
- ✅ Free forever
- ✅ Better for production

### Option B: Freenom (Alternative)

1. **Go to Freenom:**
   - Visit: https://www.freenom.com
   - Click **"Register a New Domain"** or **"Get a Free Domain"**

2. **Search for a Domain:**
   - Enter a name you want (e.g., `electricitylogger`)
   - Select a free TLD: `.tk`, `.ml`, `.ga`, `.cf`, or `.gq`
   - Click **"Check Availability"**

3. **Select Duration:**
   - Choose **12 months FREE** (maximum free period)
   - Click **"Get it now!"**

4. **Create Account:**
   - Sign up with your email
   - Verify your email address
   - Complete registration

5. **Complete Domain Registration:**
   - Fill in domain details
   - Select **12 months FREE**
   - Complete checkout (it's free!)

6. **Access Domain Management:**
   - Go to **"My Domains"** in your account
   - Find your domain
   - Click **"Manage Domain"** or **"Manage Freenom DNS"**

### Option C: InfinityFree (Free Subdomain + Hosting)

1. **Go to No-IP:**
   - Visit: https://www.noip.com
   - Sign up for free account

2. **Create Hostname:**
   - Go to **"Dynamic DNS"** → **"Hostnames"**
   - Click **"Create Hostname"**
   - Choose a subdomain (e.g., `electricitylogger.ddns.net`)
   - It's free!

### Option C: DuckDNS (Free Subdomain)

1. **Go to DuckDNS:**
   - Visit: https://www.duckdns.org
   - Sign in with Google/GitHub

2. **Create Subdomain:**
   - Enter a subdomain name
   - Click **"Add domain"**
   - Free subdomain like `electricitylogger.duckdns.org`

**Recommendation:** Use **Dot TK** (Option A) for the most reliable free domain, or **Freenom** (Option B) as an alternative

---

## Step 2: Verify Domain with Resend

### 2.1 Add Domain to Resend

1. **Go to Resend Dashboard:**
   - Visit: https://resend.com/domains
   - Click **"Add Domain"**

2. **Enter Your Domain:**
   - Enter your domain (e.g., `electricitylogger.tk`)
   - Click **"Add"**

3. **Resend Will Show DNS Records:**
   - You'll see records you need to add:
     - **SPF Record** (TXT)
     - **DKIM Record** (TXT)
     - **DMARC Record** (TXT - optional but recommended)

### 2.2 Add DNS Records to Your Domain

#### For Freenom:

1. **Go to Freenom Domain Management:**
   - Log in to Freenom
   - Go to **"My Domains"**
   - Click on your domain
   - Click **"Manage Freenom DNS"**

2. **Add SPF Record:**
   - **Type:** TXT
   - **Name:** Leave blank or `@` (root domain)
   - **TTL:** 3600 (or default)
   - **Target/Value:** Copy from Resend (looks like: `v=spf1 include:_spf.resend.com ~all`)

3. **Add DKIM Record:**
   - **Type:** TXT
   - **Name:** `resend._domainkey` (or what Resend shows)
   - **TTL:** 3600
   - **Target/Value:** Copy from Resend (long string starting with `v=DKIM1...`)

4. **Add DMARC Record (Optional but Recommended):**
   - **Type:** TXT
   - **Name:** `_dmarc`
   - **TTL:** 3600
   - **Target/Value:** `v=DMARC1; p=none; rua=mailto:your-email@example.com`

5. **Save All Records:**
   - Click **"Save"** or **"Update"** for each record
   - Wait a few minutes for DNS propagation

#### For No-IP or DuckDNS:

These services may have limited DNS control. Check their documentation for adding TXT records.

### 2.3 Verify Domain in Resend

1. **Go Back to Resend:**
   - Visit: https://resend.com/domains
   - Find your domain
   - Click **"Verify"** or **"Check Status"**

2. **Wait for Verification:**
   - DNS propagation can take 5 minutes to 48 hours
   - Usually takes 10-30 minutes
   - Resend will check automatically

3. **Verification Complete:**
   - You'll see a green checkmark ✅
   - Status will show **"Verified"**

---

## Step 3: Update Railway Configuration

### 3.1 Update RESEND_FROM_EMAIL

1. **Set the From Email:**
   ```bash
   railway variables --set "RESEND_FROM_EMAIL=noreply@yourdomain.tk"
   ```
   Replace `yourdomain.tk` with your actual domain.

2. **Verify Variables:**
   ```bash
   railway variables
   ```
   Make sure `RESEND_FROM_EMAIL` shows your domain email.

### 3.2 Redeploy Backend

Railway will automatically redeploy when you update variables. Or manually trigger:
- Go to Railway Dashboard
- Click **"Redeploy"** on your backend service

---

## Step 4: Test Email Delivery

1. **Register a New User:**
   - Use any email address (not just your verified one)
   - Complete registration

2. **Check Email:**
   - User should receive email at their address
   - Check spam folder if not in inbox

3. **Check Railway Logs:**
   - Should see: `✅ Verification email sent successfully`
   - No more 403 errors!

4. **Check Resend Dashboard:**
   - Go to https://resend.com/emails
   - See sent emails with **"Delivered"** status

---

## 🎯 Quick Checklist

- [ ] Get free domain from Freenom
- [ ] Add domain to Resend
- [ ] Add SPF record to domain DNS
- [ ] Add DKIM record to domain DNS
- [ ] Add DMARC record (optional)
- [ ] Verify domain in Resend (wait for green checkmark)
- [ ] Update `RESEND_FROM_EMAIL` in Railway
- [ ] Redeploy backend
- [ ] Test registration with any email
- [ ] Confirm email delivery works!

---

## 🆘 Troubleshooting

### DNS Records Not Working?

1. **Check Record Format:**
   - Make sure you copied the entire value from Resend
   - No extra spaces or characters
   - TXT records can be long - include everything

2. **Wait for Propagation:**
   - DNS changes take time to propagate
   - Can take up to 48 hours (usually 10-30 minutes)
   - Use https://dnschecker.org to check propagation

3. **Verify in Freenom:**
   - Go back to Freenom DNS management
   - Make sure records are saved correctly
   - Check for typos

### Domain Not Verifying in Resend?

1. **Check DNS Propagation:**
   - Use: https://dnschecker.org
   - Search for your domain
   - Check TXT records are visible globally

2. **Double-Check Records:**
   - Make sure SPF and DKIM records match Resend exactly
   - No extra characters or spaces

3. **Contact Resend Support:**
   - If still not working after 24 hours
   - They can help troubleshoot

### Still Getting 403 Errors?

1. **Verify Domain Status:**
   - Check Resend dashboard shows domain as "Verified"
   - Green checkmark ✅

2. **Check RESEND_FROM_EMAIL:**
   - Must use your verified domain
   - Format: `noreply@yourdomain.tk`
   - Not `onboarding@resend.dev`

3. **Redeploy Backend:**
   - Make sure Railway picked up the new variable
   - Check logs for the new from email

---

## 📊 Example: Complete Setup

**Domain:** `electricitylogger.tk` (from Freenom)

**Resend From Email:** `noreply@electricitylogger.tk`

**DNS Records Added:**
- SPF: `v=spf1 include:_spf.resend.com ~all`
- DKIM: `v=DKIM1; k=rsa; p=...` (long string from Resend)
- DMARC: `v=DMARC1; p=none; rua=mailto:electricitylogger@gmail.com`

**Railway Variable:**
```
RESEND_FROM_EMAIL=noreply@electricitylogger.tk
```

**Result:** ✅ Emails sent to any address!

---

## ⏱️ Time Estimate

- **Getting domain:** 5-10 minutes
- **Adding DNS records:** 5 minutes
- **DNS propagation:** 10-30 minutes (sometimes up to 48 hours)
- **Resend verification:** Automatic after DNS propagates
- **Total:** ~30-60 minutes (mostly waiting for DNS)

---

**You'll have email delivery working in about an hour!** 🚀

