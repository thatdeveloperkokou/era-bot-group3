# Namecheap Domain Setup - Quick Guide

## 🎯 Buy Domain from Namecheap ($0.99/year)

### Step 1: Create Account (2 minutes)

1. **Go to Namecheap:**
   - Visit: https://www.namecheap.com
   - Click "Sign Up" (top right corner)

2. **Fill in Form:**
   - Email address
   - Password
   - First Name
   - Last Name
   - Click "Create Account"

3. **Verify Email:**
   - Check your email
   - Click verification link
   - Return to Namecheap

### Step 2: Search for Domain (1 minute)

1. **In the search box** (top of page):
   - Type: `electricitylogger`
   - Click search icon or press Enter

2. **Look for Results:**
   - Find `.xyz` domain
   - Should show price: **$0.99/year** (or similar)
   - Other TLDs might be more expensive

### Step 3: Buy Domain (2 minutes)

1. **Add to Cart:**
   - Click "Add to Cart" next to `.xyz` domain
   - Click "View Cart" (top right)

2. **Review Cart:**
   - Should show: `electricitylogger.xyz` - $0.99/year
   - Click "Confirm Order"

3. **Checkout:**
   - Enter payment method (credit card, PayPal, etc.)
   - Complete purchase
   - Domain is now yours! ✅

### Step 4: Access DNS Management (1 minute)

1. **Go to Domain List:**
   - After purchase, you'll see your domain
   - Or go to: https://ap.www.namecheap.com/Domains/DomainControlPanel

2. **Click on Your Domain:**
   - Click `electricitylogger.xyz` (or your domain name)

3. **Go to Advanced DNS:**
   - Click "Advanced DNS" tab
   - You'll see DNS records section
   - This is where you'll add Resend records!

### Step 5: Add Resend DNS Records (5 minutes)

1. **Add Domain to Resend:**
   - Go to: https://resend.com/domains
   - Click "Add Domain"
   - Enter: `electricitylogger.xyz`
   - Click "Add"

2. **Copy DNS Records from Resend:**
   - Resend will show you records to add:
     - DKIM (TXT)
     - SPF (TXT)
     - DMARC (TXT) - Optional
     - MX (Sending)
     - MX (Receiving)
   - Copy each record

3. **Add Records in Namecheap:**
   - In Namecheap Advanced DNS, click "Add New Record"
   - For each record:
     - **Type:** Select type (TXT, MX, etc.)
     - **Host:** Enter name (from Resend)
     - **Value:** Enter value (from Resend)
     - **TTL:** Leave as default or set to 3600
     - Click "Save" (green checkmark)
   - Repeat for all records

4. **Verify Records Added:**
   - You should see all records listed
   - Check they match Resend requirements

### Step 6: Verify in Resend (Wait 10-30 minutes)

1. **Wait for DNS Propagation:**
   - DNS changes take 10-30 minutes
   - Can take up to 48 hours (rare)

2. **Verify in Resend:**
   - Go to: https://resend.com/domains
   - Find your domain
   - Click "Verify" or "Check Status"
   - Wait for verification
   - You'll see green checkmarks when verified ✅

### Step 7: Update Railway (1 minute)

1. **Set From Email:**
   ```bash
   railway variables --set "RESEND_FROM_EMAIL=noreply@electricitylogger.xyz"
   ```

2. **Verify Variable:**
   ```bash
   railway variables | findstr RESEND
   ```
   Should show: `RESEND_FROM_EMAIL=noreply@electricitylogger.xyz`

3. **Railway will auto-redeploy**

### Step 8: Test! (1 minute)

1. **Register a new user** with any email
2. **Check their inbox** - they should receive verification email!
3. **Check Railway logs** - should see success messages
4. **Check Resend dashboard** - should show sent emails

---

## ✅ Complete Checklist

- [ ] Created Namecheap account
- [ ] Bought `.xyz` domain ($0.99/year)
- [ ] Accessed Advanced DNS
- [ ] Added domain to Resend
- [ ] Added DKIM record (TXT)
- [ ] Added SPF record (TXT)
- [ ] Added DMARC record (TXT) - Optional
- [ ] Added MX record (Sending)
- [ ] Added MX record (Receiving)
- [ ] Waited 10-30 minutes for DNS propagation
- [ ] Verified domain in Resend (green checkmark ✅)
- [ ] Updated Railway: `RESEND_FROM_EMAIL`
- [ ] Tested email delivery - works! ✅

---

## 🆘 Troubleshooting

### Can't Find Advanced DNS?

1. **Go to Domain List:**
   - https://ap.www.namecheap.com/Domains/DomainControlPanel
   - Click on your domain

2. **Look for Tabs:**
   - "Advanced DNS" tab should be visible
   - If not, look for "DNS" or "DNS Management"

### DNS Records Not Saving?

1. **Check Format:**
   - Make sure values match Resend exactly
   - No extra spaces
   - Copy complete values

2. **Check Record Type:**
   - TXT records for DKIM, SPF, DMARC
   - MX records for sending/receiving

### Domain Not Verifying in Resend?

1. **Wait Longer:**
   - DNS can take 30 minutes to 48 hours
   - Usually 10-30 minutes

2. **Check DNS Propagation:**
   - Visit: https://dnschecker.org
   - Search for your domain
   - Check if TXT records are visible globally

3. **Verify Records:**
   - Double-check all records in Namecheap
   - Make sure they match Resend exactly

---

## 💰 Cost Breakdown

- **Domain:** $0.99/year
- **That's:** $0.08/month
- **That's:** Less than 3 cents per day!

**Very affordable and most reliable option!**

---

## 🎉 You're Done!

Once verified:
- ✅ Email delivery works
- ✅ Users can register and verify
- ✅ Professional domain
- ✅ Reliable setup

**Total time:** ~20 minutes  
**Total cost:** $0.99/year  
**Result:** Fully working email system! 🚀

---

**Start at https://www.namecheap.com - it's the easiest solution!** 🎯

