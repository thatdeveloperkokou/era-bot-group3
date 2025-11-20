# Freenom Free Domain - Step by Step (With Screenshots Guide)

## 🎯 Getting Your Free Domain from Freenom

### Step 1: Visit Freenom Website

1. Go to: **https://www.freenom.com**
2. You'll see the homepage with domain search

### Step 2: Search for Your Domain

1. In the search box, type your desired name:
   - Example: `electricitylogger`
   - Or: `myelectricitybot`
   - Or: `powerlogger`

2. Select a **FREE TLD** from the dropdown:
   - `.tk` (Tokelau) - Most popular
   - `.ml` (Mali)
   - `.ga` (Gabon)
   - `.cf` (Central African Republic)
   - `.gq` (Equatorial Guinea)

3. Click **"Check Availability"** or press Enter

### Step 3: Select Your Domain

1. If available, you'll see:
   - Your domain name
   - Price: **FREE** (for 12 months)
   - Duration options

2. **Important:** Select **12 months FREE** (maximum free period)

3. Click **"Get it now!"** or **"Add to Cart"**

### Step 4: Create Freenom Account

1. If you don't have an account:
   - Click **"Create Account"** or **"Sign Up"**
   - Fill in:
     - Email address
     - Password
     - First Name
     - Last Name
   - Click **"Create Account"**

2. **Verify Your Email:**
   - Check your email inbox
   - Click verification link
   - Return to Freenom

### Step 5: Complete Domain Registration

1. **Review Your Cart:**
   - Should show your domain
   - Duration: 12 months
   - Price: FREE

2. **Fill in Domain Details:**
   - **Registrant Type:** Individual (usually)
   - **First Name:** Your first name
   - **Last Name:** Your last name
   - **Email:** Your email
   - **Address:** Your address
   - **City:** Your city
   - **State/Province:** Your state
   - **Postal Code:** Your zip code
   - **Country:** Your country
   - **Phone:** Your phone number

3. **Complete Checkout:**
   - Review all information
   - Accept terms and conditions
   - Click **"Complete Order"** or **"Checkout"**

4. **Confirmation:**
   - You'll see "Order Complete" or similar
   - Domain is now yours!

### Step 6: Access Domain Management

1. **Go to "My Domains":**
   - Log in to Freenom
   - Click **"My Domains"** in the menu
   - Or go to: https://my.freenom.com/clientarea.php?action=domains

2. **Find Your Domain:**
   - You'll see a list of your domains
   - Find the one you just registered

3. **Manage DNS:**
   - Click on your domain name
   - Or click **"Manage Domain"**
   - Look for **"Manage Freenom DNS"** or **"DNS"** tab
   - Click it

---

## 🔧 Managing DNS Records in Freenom

### Accessing DNS Management

1. **From "My Domains" page:**
   - Click on your domain name
   - This opens domain details

2. **Find DNS Settings:**
   - Look for tabs: **"Management Tools"**, **"DNS"**, or **"Nameservers"**
   - Click **"Manage Freenom DNS"** or **"Use Freenom Nameservers"**

3. **You'll See DNS Records:**
   - A records (for website)
   - CNAME records
   - **TXT records** (what we need!)

### Adding TXT Records

1. **Find "Add Record" or "+" button:**
   - Usually at the bottom of DNS records list
   - Or in a "Records" section

2. **Add SPF Record:**
   - **Type:** Select **"TXT"**
   - **Name:** Leave blank or enter `@` (represents root domain)
   - **TTL:** 3600 (or leave default)
   - **Target/Value:** Paste from Resend (looks like: `v=spf1 include:_spf.resend.com ~all`)
   - Click **"Save"** or **"Add"**

3. **Add DKIM Record:**
   - **Type:** Select **"TXT"**
   - **Name:** Enter `resend._domainkey` (or what Resend shows)
   - **TTL:** 3600
   - **Target/Value:** Paste from Resend (long string starting with `v=DKIM1...`)
   - Click **"Save"** or **"Add"**

4. **Add DMARC Record (Optional):**
   - **Type:** Select **"TXT"**
   - **Name:** Enter `_dmarc`
   - **TTL:** 3600
   - **Target/Value:** `v=DMARC1; p=none; rua=mailto:your-email@gmail.com`
   - Click **"Save"** or **"Add"**

### Saving Changes

1. **Verify Records:**
   - Make sure all records are listed
   - Check for typos
   - Values should match Resend exactly

2. **Save:**
   - Click **"Save Changes"** or **"Update"**
   - Wait for confirmation message

3. **Wait for Propagation:**
   - DNS changes take 10-30 minutes to propagate
   - Can take up to 48 hours (rare)

---

## 📋 Freenom DNS Record Example

Here's what your DNS records should look like:

```
Type    Name              TTL     Target/Value
----    ----              ---     -----------
TXT     @                 3600    v=spf1 include:_spf.resend.com ~all
TXT     resend._domainkey 3600    v=DKIM1; k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQC...
TXT     _dmarc            3600    v=DMARC1; p=none; rua=mailto:electricitylogger@gmail.com
```

---

## 🆘 Common Freenom Issues

### Can't Find DNS Management?

1. **Try Different Paths:**
   - My Domains → Click Domain → Management Tools → DNS
   - Or: Services → My Domains → Manage Domain → DNS

2. **Check Domain Status:**
   - Domain must be active
   - Not expired or pending

### TXT Records Not Saving?

1. **Check Format:**
   - No extra spaces
   - Copy entire value from Resend
   - TXT records can be very long - that's normal

2. **Try Different Browser:**
   - Sometimes Freenom interface has issues
   - Try Chrome, Firefox, or Edge

### Domain Not Showing Up?

1. **Check Email:**
   - Registration might need email verification
   - Check spam folder

2. **Wait a Few Minutes:**
   - Domain registration can take a few minutes
   - Refresh "My Domains" page

---

## ✅ Verification Checklist

After adding DNS records:

- [ ] SPF record added (Type: TXT, Name: @ or blank)
- [ ] DKIM record added (Type: TXT, Name: resend._domainkey)
- [ ] DMARC record added (Type: TXT, Name: _dmarc) - Optional
- [ ] All records saved in Freenom
- [ ] Waited 10-30 minutes for DNS propagation
- [ ] Verified domain in Resend dashboard
- [ ] Green checkmark ✅ in Resend

---

**Once verified in Resend, you're ready to send emails to any address!** 🎉

