# Adding Resend DNS Records in InfinityFree

## 🎯 You're in the Right Place!

I can see you're in InfinityFree's DNS Records section with the "Add Record" dropdown. Here's how to add each record:

---

## Step-by-Step: Adding Each Record

### Record 1: Domain Verification - DKIM (TXT)

**For DKIM, you need a TXT record:**

1. **Look for a generic "Add Record" or "TXT Record" option:**
   - The dropdown shows "Create SPF Record" (which is a TXT record)
   - Look for a generic "Create TXT Record" or "Add Record" option
   - If you don't see it, try clicking "Create SPF Record" - it might allow you to change the type to TXT

2. **If you see "Create TXT Record" or generic "Add Record":**
   - Click it
   - **Type:** `TXT`
   - **Name/Host:** Copy the FULL name from Resend (e.g., `resend._domainkey.electricitylogger.wuaze.com`)
   - **Value/Target:** Copy the FULL DKIM key from Resend (the complete long string)
   - **TTL:** `3600` (or default)
   - Click **"Save"** or **"Add"**

3. **If only "Create SPF Record" is available:**
   - Click "Create SPF Record"
   - In the form, you might be able to change the record type to TXT
   - Or use the SPF form but change the Name to your DKIM name

---

### Record 2: Enable Sending - MX Record

**This one is easy - use the dropdown option:**

1. **Click "Create MX Record"** from the dropdown
2. **Fill in the form:**
   - **Name/Host:** Copy the FULL name from Resend (e.g., `send.electricitylogger.wuaze.com`)
   - **Mail Server:** Copy the FULL mail server from Resend (e.g., `feedback-smtp.us-east-1.resend.com`)
   - **Priority:** `10`
   - **TTL:** `3600` (or default)
3. **Click "Save" or "Add"**

---

### Record 3: Enable Sending - SPF (TXT)

**Use the SPF option from the dropdown:**

1. **Click "Create SPF Record"** from the dropdown
2. **Fill in the form:**
   - **Name/Host:** Copy the FULL name from Resend (e.g., `send.electricitylogger.wuaze.com`)
   - **Value/Target:** Copy the FULL SPF record from Resend (e.g., `v=spf1 include:amazonses.com ~all`)
   - **TTL:** `3600` (or default)
3. **Click "Save" or "Add"**

---

### Record 4: Enable Sending - DMARC (TXT) - Optional

**For DMARC, you need another TXT record:**

1. **Look for "Create TXT Record" or generic "Add Record":**
   - Same as DKIM - look for a TXT option
   - Or try "Create SPF Record" and see if you can change the type

2. **Fill in:**
   - **Type:** `TXT`
   - **Name/Host:** `_dmarc` (or `_dmarc.electricitylogger.wuaze.com` if Resend shows it)
   - **Value/Target:** Copy the FULL DMARC record from Resend (e.g., `v=DMARC1; p=none;`)
   - **TTL:** `3600` (or default)
3. **Click "Save" or "Add"**

---

### Record 5: Enable Receiving - MX Record

**Another MX record:**

1. **Click "Create MX Record"** from the dropdown
2. **Fill in the form:**
   - **Name/Host:** Copy the FULL name from Resend (e.g., `electricitylogger.wuaze.com` or `@`)
   - **Mail Server:** Copy the FULL mail server from Resend (e.g., `inbound-smtp.us-east-1.resend.com`)
   - **Priority:** `10`
   - **TTL:** `3600` (or default)
3. **Click "Save" or "Add"**

---

## 🔍 Finding TXT Record Option

If you don't see a "Create TXT Record" option in the dropdown:

### Option 1: Check for More Options
- The dropdown might scroll - try scrolling down
- Look for "Add Record" or "Create Record" (generic option)

### Option 2: Use SPF Form
- Click "Create SPF Record"
- In the form, you might be able to:
  - Change the record type dropdown to "TXT"
  - Or just use the SPF form but change the Name field

### Option 3: Look for Advanced Options
- Check if there's an "Advanced" or "More" button
- Look for a "+" or "Add" button that might show more record types

### Option 4: Check InfinityFree Documentation
- Visit: https://forum.infinityfree.com
- Search for "add TXT record" or "DNS Zone Editor"

---

## 📋 Quick Checklist

After adding all records, you should have:

- [ ] DKIM (TXT) - Domain Verification
- [ ] MX Record - Sending (send.electricitylogger.wuaze.com)
- [ ] SPF (TXT) - Sending
- [ ] DMARC (TXT) - Sending (Optional)
- [ ] MX Record - Receiving (electricitylogger.wuaze.com)

---

## ⚠️ Important Notes

1. **Copy FULL Values:**
   - Don't use truncated values from screenshots
   - Get complete values from your Resend dashboard
   - DKIM keys are very long - copy the entire key

2. **Name Format:**
   - Use exactly what Resend shows
   - Some might be full domain: `resend._domainkey.electricitylogger.wuaze.com`
   - Others might be shorter: `resend._domainkey`
   - Follow Resend's format exactly

3. **MX Priority:**
   - Both MX records should have Priority: `10`
   - This is important for email routing

---

## 🚀 After Adding All Records

1. **Wait 10-30 minutes** for DNS propagation
2. **Go to Resend:** https://resend.com/domains
3. **Click "Verify"** on your domain
4. **Check all sections:**
   - Domain Verification: ✅
   - Enable Sending: ✅
   - Enable Receiving: ✅

---

## 🆘 Troubleshooting

### Can't Find TXT Record Option?

1. **Try "Create SPF Record":**
   - SPF is a TXT record type
   - The form might allow you to change the type
   - Or use it and modify the Name field

2. **Check InfinityFree Help:**
   - Look for a "?" or "Help" icon
   - Check InfinityFree documentation

3. **Contact InfinityFree Support:**
   - They can guide you to the TXT record option
   - Forum: https://forum.infinityfree.com

---

**Start with the MX records (easiest), then add the TXT records!** 🎉

