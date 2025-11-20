# Adding Resend DNS Records to InfinityFree

## 🎯 You Have the DNS Records from Resend!

Now let's add them to InfinityFree. I can see you have:
- Domain Verification (DKIM)
- Enable Sending (MX, SPF, DMARC)
- Enable Receiving (MX)

---

## Step 1: Access DNS Zone Editor in InfinityFree

1. **From the InfinityFree control panel:**
   - Click on **"DNS Records"** in the left sidebar (I can see it in your screenshot)
   - Or go to: Domains → `electricitylogger.wuaze.com` → DNS Zone Editor

2. **You should see a page to add DNS records**

---

## Step 2: Add the DNS Records

**Important:** Copy the **FULL, untruncated values** from your Resend dashboard. The image shows truncated values - make sure to copy the complete values!

### Record 1: Domain Verification - DKIM (TXT)

1. **Click "Add Record" or "+"**
2. **Fill in:**
   - **Type:** `TXT`
   - **Name/Host:** Copy the FULL name from Resend (looks like: `resend._domainkey.electricitylogger.wuaze.com`)
   - **TTL:** `3600` (or leave default)
   - **Value/Target:** Copy the FULL content from Resend (starts with `p=MIGfMA0GCSqGSIb3DQEB...` - make sure to get the complete key!)
3. **Click "Add" or "Save"**

### Record 2: Enable Sending - MX Record

1. **Click "Add Record" or "+"**
2. **Fill in:**
   - **Type:** `MX`
   - **Name/Host:** Copy the FULL name from Resend (looks like: `send.electricitylogger.wuaze.com`)
   - **TTL:** `3600` (or leave default)
   - **Value/Target:** Copy the FULL mail server from Resend (looks like: `feedback-smtp.us-east-1.resend.com`)
   - **Priority:** `10`
3. **Click "Add" or "Save"**

### Record 3: Enable Sending - SPF (TXT)

1. **Click "Add Record" or "+"**
2. **Fill in:**
   - **Type:** `TXT`
   - **Name/Host:** Copy the FULL name from Resend (looks like: `send.electricitylogger.wuaze.com`)
   - **TTL:** `3600` (or leave default)
   - **Value/Target:** Copy the FULL SPF record from Resend (looks like: `v=spf1 include:amazonses.com ~all` - make sure to get the complete value!)
3. **Click "Add" or "Save"**

### Record 4: Enable Sending - DMARC (TXT) - Optional

1. **Click "Add Record" or "+"**
2. **Fill in:**
   - **Type:** `TXT`
   - **Name/Host:** `_dmarc` (or `_dmarc.electricitylogger.wuaze.com` if Resend shows it)
   - **TTL:** `3600` (or leave default)
   - **Value/Target:** Copy the FULL DMARC record from Resend (looks like: `v=DMARC1; p=none;` - make sure to get the complete value!)
3. **Click "Add" or "Save"**

### Record 5: Enable Receiving - MX Record

1. **Click "Add Record" or "+"**
2. **Fill in:**
   - **Type:** `MX`
   - **Name/Host:** Copy the FULL name from Resend (looks like: `electricitylogger.wuaze.com` or just `@`)
   - **TTL:** `3600` (or leave default)
   - **Value/Target:** Copy the FULL mail server from Resend (looks like: `inbound-smtp.us-east-1.resend.com`)
   - **Priority:** `10`
3. **Click "Add" or "Save"**

---

## Step 3: Verify All Records Added

Your DNS records should look something like this:

```
Type    Name                                    TTL     Value
----    ----                                    ---     -----
TXT     resend._domainkey.electricitylogger...  3600    p=MIGfMA0GCSqGSIb3DQEB... (full key)
MX      send.electricitylogger.wuaze.com        3600    feedback-smtp.us-east-1.resend.com (Priority: 10)
TXT     send.electricitylogger.wuaze.com      3600    v=spf1 include:amazonses.com ~all
TXT     _dmarc                                 3600    v=DMARC1; p=none; (full value)
MX      electricitylogger.wuaze.com            3600    inbound-smtp.us-east-1.resend.com (Priority: 10)
```

---

## Step 4: Wait for DNS Propagation

1. **DNS changes take time to propagate:**
   - Usually 10-30 minutes
   - Can take up to 48 hours (rare)

2. **Check DNS Propagation:**
   - Visit: https://dnschecker.org
   - Search for your domain
   - Check if TXT and MX records are visible globally

---

## Step 5: Verify in Resend

1. **Go back to Resend:**
   - Visit: https://resend.com/domains
   - Find `electricitylogger.wuaze.com`

2. **Click "Verify" or "Check Status"**

3. **Wait for verification:**
   - Resend will check automatically
   - You'll see status updates
   - When verified, you'll see green checkmarks ✅

4. **Check all sections:**
   - Domain Verification: ✅ Verified
   - Enable Sending: ✅ Enabled
   - Enable Receiving: ✅ Enabled

---

## ⚠️ Important Notes

### Copy FULL Values!

The image shows truncated values. Make sure to:
- Copy the **complete** Name/Host values
- Copy the **complete** Content/Value values
- Don't use truncated values from the image
- Get the full values directly from your Resend dashboard

### Common Issues:

1. **DKIM Key Too Long:**
   - DKIM keys are very long (multiple lines)
   - Make sure to copy the ENTIRE key
   - Some DNS systems allow multi-line values

2. **Name Format:**
   - Some DNS systems need full domain: `resend._domainkey.electricitylogger.wuaze.com`
   - Others need just: `resend._domainkey`
   - Check what Resend shows and use that format

3. **MX Records:**
   - Make sure Priority is set to `10`
   - Value should be the mail server hostname (not an IP)

---

## ✅ Verification Checklist

After adding all records:

- [ ] DKIM record added (TXT)
- [ ] Sending MX record added
- [ ] SPF record added (TXT)
- [ ] DMARC record added (TXT) - Optional
- [ ] Receiving MX record added
- [ ] All records saved in InfinityFree
- [ ] Waited 10-30 minutes for DNS propagation
- [ ] Checked DNS propagation at dnschecker.org
- [ ] Domain verified in Resend (green checkmark ✅)
- [ ] Sending enabled in Resend (green toggle ✅)
- [ ] Receiving enabled in Resend (green toggle ✅)

---

## 🚀 After Verification

Once all records are verified:

1. **Railway is already configured:**
   - `RESEND_FROM_EMAIL=noreply@electricitylogger.wuaze.com` ✅

2. **Test email delivery:**
   - Register a new user with any email
   - They should receive verification email!
   - Check Railway logs for success messages

3. **Check Resend dashboard:**
   - Go to https://resend.com/emails
   - See sent emails with "Delivered" status

---

**Start adding the DNS records in InfinityFree! Make sure to copy the FULL values from Resend!** 🎉

