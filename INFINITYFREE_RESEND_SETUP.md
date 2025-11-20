# Setting Up electricitylogger.wuaze.com with Resend

## ✅ You Have: electricitylogger.wuaze.com

Now let's verify it with Resend and enable email delivery!

---

## Step 1: Add Domain to Resend

1. **Go to Resend Dashboard:**
   - Visit: https://resend.com/domains
   - Click **"Add Domain"**

2. **Enter Your Domain:**
   - Domain: `electricitylogger.wuaze.com`
   - Click **"Add"**

3. **Resend Will Show DNS Records:**
   - You'll see records you need to add:
     - **SPF Record** (TXT)
     - **DKIM Record** (TXT)
     - **DMARC Record** (TXT - optional but recommended)
   - **Copy these records** - you'll need them!

---

## Step 2: Add DNS Records in InfinityFree

### 2.1 Access InfinityFree DNS Management

1. **Log in to InfinityFree:**
   - Go to: https://www.infinityfree.net
   - Log in to your account

2. **Go to Domain Management:**
   - Click on **"Domains"** or **"My Domains"**
   - Find `electricitylogger.wuaze.com`
   - Click on it or click **"Manage"**

3. **Access DNS Settings:**
   - Look for **"DNS Zone Editor"** or **"DNS Management"**
   - Or go to: **"Advanced"** → **"DNS Zone Editor"**
   - Click to open DNS management

### 2.2 Add DNS Records from Resend

**Important:** Resend will show you multiple records. You need to add ALL of them. Copy the **FULL, untruncated values** from your Resend dashboard!

#### Records You Need to Add:

1. **Domain Verification - DKIM (TXT)**
2. **Enable Sending - MX Record**
3. **Enable Sending - SPF (TXT)**
4. **Enable Sending - DMARC (TXT)** - Optional
5. **Enable Receiving - MX Record**

#### Record 1: Domain Verification - DKIM (TXT)

1. **Click "Add Record" or "+"**
2. **Fill in:**
   - **Type:** `TXT`
   - **Name/Host:** Copy the FULL name from Resend (looks like: `resend._domainkey.electricitylogger.wuaze.com`)
   - **TTL:** `3600` (or default)
   - **Value/Target:** Copy the FULL content from Resend (starts with `p=MIGfMA0GCSqGSIb3DQEB...` - get the complete key!)
3. **Click "Add" or "Save"**

#### Record 2: Enable Sending - MX Record

1. **Click "Add Record" or "+"**
2. **Fill in:**
   - **Type:** `MX`
   - **Name/Host:** Copy the FULL name from Resend (looks like: `send.electricitylogger.wuaze.com`)
   - **TTL:** `3600` (or default)
   - **Value/Target:** Copy the FULL mail server from Resend (looks like: `feedback-smtp.us-east-1.resend.com`)
   - **Priority:** `10`
3. **Click "Add" or "Save"**

#### Record 3: Enable Sending - SPF (TXT)

1. **Click "Add Record" or "+"**
2. **Fill in:**
   - **Type:** `TXT`
   - **Name/Host:** Copy the FULL name from Resend (looks like: `send.electricitylogger.wuaze.com`)
   - **TTL:** `3600` (or default)
   - **Value/Target:** Copy the FULL SPF record from Resend (looks like: `v=spf1 include:amazonses.com ~all`)
3. **Click "Add" or "Save"**

#### Record 4: Enable Sending - DMARC (TXT) - Optional

1. **Click "Add Record" or "+"**
2. **Fill in:**
   - **Type:** `TXT`
   - **Name/Host:** `_dmarc` (or what Resend shows)
   - **TTL:** `3600`
   - **Value/Target:** Copy the FULL DMARC record from Resend (looks like: `v=DMARC1; p=none;`)
3. **Click "Add" or "Save"**

#### Record 5: Enable Receiving - MX Record

1. **Click "Add Record" or "+"**
2. **Fill in:**
   - **Type:** `MX`
   - **Name/Host:** Copy the FULL name from Resend (looks like: `electricitylogger.wuaze.com` or `@`)
   - **TTL:** `3600` (or default)
   - **Value/Target:** Copy the FULL mail server from Resend (looks like: `inbound-smtp.us-east-1.resend.com`)
   - **Priority:** `10`
3. **Click "Add" or "Save"**

### 2.3 Verify Records Added

Your DNS records should look like this:

```
Type    Name              TTL     Value
----    ----              ---     -----
TXT     @                 3600    v=spf1 include:_spf.resend.com ~all
TXT     resend._domainkey 3600    v=DKIM1; k=rsa; p=... (long string)
TXT     _dmarc            3600    v=DMARC1; p=none; rua=mailto:electricitylogger@gmail.com
```

---

## Step 3: Verify Domain in Resend

1. **Go Back to Resend:**
   - Visit: https://resend.com/domains
   - Find `electricitylogger.wuaze.com`
   - Click **"Verify"** or **"Check Status"**

2. **Wait for DNS Propagation:**
   - DNS changes take 10-30 minutes to propagate
   - Can take up to 48 hours (rare)
   - Resend will check automatically

3. **Check Verification Status:**
   - You'll see status updates
   - When verified, you'll see a green checkmark ✅
   - Status will show **"Verified"**

**Tip:** You can check DNS propagation at: https://dnschecker.org
- Search for your domain
- Check TXT records are visible globally

---

## Step 4: Update Railway Configuration

### 4.1 Update RESEND_FROM_EMAIL

1. **Set the From Email:**
   ```bash
   railway variables --set "RESEND_FROM_EMAIL=noreply@electricitylogger.wuaze.com"
   ```

2. **Verify Variables:**
   ```bash
   railway variables
   ```
   Make sure `RESEND_FROM_EMAIL` shows: `noreply@electricitylogger.wuaze.com`

### 4.2 Redeploy Backend

Railway will automatically redeploy when you update variables. Or manually:
- Go to Railway Dashboard
- Click **"Redeploy"** on your backend service

---

## Step 5: Test Email Delivery

1. **Register a New User:**
   - Go to your app
   - Register with any email address
   - Complete registration

2. **Check Email:**
   - User should receive email at their address
   - Check spam folder if not in inbox
   - Email should be from: `noreply@electricitylogger.wuaze.com`

3. **Check Railway Logs:**
   - Go to Railway → Backend → Logs
   - Should see: `✅ Verification email sent successfully`
   - No more 403 errors!

4. **Check Resend Dashboard:**
   - Go to https://resend.com/emails
   - See sent emails with **"Delivered"** status

---

## 🎯 Quick Checklist

- [ ] Domain added to Resend (`electricitylogger.wuaze.com`)
- [ ] SPF record added in InfinityFree DNS
- [ ] DKIM record added in InfinityFree DNS
- [ ] DMARC record added (optional)
- [ ] All DNS records saved
- [ ] Waited 10-30 minutes for DNS propagation
- [ ] Domain verified in Resend (green checkmark ✅)
- [ ] Updated `RESEND_FROM_EMAIL` in Railway
- [ ] Backend redeployed
- [ ] Tested registration with any email
- [ ] Email delivery confirmed!

---

## 🆘 Troubleshooting

### DNS Records Not Showing in Resend?

1. **Check DNS Propagation:**
   - Visit: https://dnschecker.org
   - Search for `electricitylogger.wuaze.com`
   - Check TXT records are visible globally
   - Wait if not yet propagated (can take 30 minutes)

2. **Verify Records in InfinityFree:**
   - Go back to InfinityFree DNS Zone Editor
   - Make sure all records are saved correctly
   - Check for typos
   - Make sure values match Resend exactly

3. **Check Record Format:**
   - SPF: Name should be `@` or blank
   - DKIM: Name should be `resend._domainkey`
   - DMARC: Name should be `_dmarc`
   - Values should match Resend exactly (no extra spaces)

### Still Getting 403 Errors?

1. **Verify Domain Status:**
   - Check Resend dashboard shows domain as "Verified"
   - Green checkmark ✅

2. **Check RESEND_FROM_EMAIL:**
   - Must use your verified domain
   - Format: `noreply@electricitylogger.wuaze.com`
   - Not `onboarding@resend.dev`

3. **Redeploy Backend:**
   - Make sure Railway picked up the new variable
   - Check logs for the new from email

### Can't Find DNS Management in InfinityFree?

1. **Try Different Paths:**
   - Domains → Your Domain → DNS Zone Editor
   - Or: Advanced → DNS Zone Editor
   - Or: Domain Settings → DNS

2. **Check InfinityFree Documentation:**
   - Visit: https://forum.infinityfree.com
   - Search for "DNS Zone Editor"

---

## 📊 Expected Result

After setup:

✅ **Domain:** `electricitylogger.wuaze.com` verified in Resend  
✅ **From Email:** `noreply@electricitylogger.wuaze.com`  
✅ **Emails:** Delivered to any address  
✅ **Status:** No more 403 errors!  
✅ **Logs:** `✅ Verification email sent successfully`

---

## 🚀 Next Steps

Once verified:

1. **Test Registration:**
   - Register with any email
   - Check email inbox
   - Verify code works

2. **Monitor:**
   - Check Resend dashboard for email status
   - Check Railway logs for success messages

3. **Production Ready:**
   - Your email system is now fully functional!
   - Users can register and receive verification emails

---

**You're almost there! Add the DNS records and verify in Resend!** 🎉

