# 🚀 RAILWAY DEPLOYMENT - STEP BY STEP GUIDE

## Complete 10-Step Deployment Process

---

## **STEP 1: Create Railway Account**

1. Go to: https://railway.app
2. Click **"Start Free"** or **"Sign Up"**
3. Choose **"Continue with GitHub"**
4. Authorize Railway to access your GitHub
5. Confirm email
6. ✓ Account created!

**Time: 2 minutes**

---

## **STEP 2: Create New Railway Project**

1. Go to Railway Dashboard
2. Click **"+ New Project"**
3. Select **"Deploy from GitHub repo"**
4. Look for: **`Adanhassan790/Elleden-Hotel`**
5. Click **"Select Repository"**
6. Railway starts deploying automatically!

**Time: 1 minute**

---

## **STEP 3: Wait for Initial Deployment**

You'll see a **"Building"** status:
```
📦 Building...
⏳ This takes 2-5 minutes
```

What's happening:
- ✓ Downloading code from GitHub
- ✓ Installing Python packages
- ✓ Building the application
- ✓ Starting the server

**Time: 5 minutes**

---

## **STEP 4: Add Environment Variables**

⚠️ **CRITICAL STEP** - App won't work without these!

### **Action:**
1. In Railway Dashboard, click on your **main service** (the blue circle with name)
2. Go to **"Variables"** tab (top menu)
3. Click **"RAW Editor"** (top right)
4. Copy-paste this entire block:

```
SECRET_KEY=django-superhz#aqk!qmj3-a)svo)$&6r2=f5hs7b5je=w#3^2&z=nqr7%p0&v9
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,.railway.app
EMAIL_HOST_USER=elledenhotelltd@gmail.com
EMAIL_HOST_PASSWORD=bcanouvfydpjokpy
MPESA_ENVIRONMENT=sandbox
MPESA_CONSUMER_KEY=uLdcxbFm1VC4yNGUO2zZiXJneeksC7I93XOdeZQc7gCG3R9N
MPESA_CONSUMER_SECRET=HpAdvzwtdCaO8N7mGKOt5sLMRXgHpGmzzFZ3AIg0vAQ8V6BnbpJdlI5WIJlajZli
MPESA_SHORTCODE=174379
MPESA_PASSKEY=bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919
MPESA_CALLBACK_URL=https://your-app-domain.railway.app/bookings/mpesa/callback/
AFRICASTALKING_USERNAME=elledenhotel
AFRICASTALKING_API_KEY=atsk_36edf8ab6f1b702ed43fd4727fac4abad432827e87b97df0d04f263063a1026bfb2bdbd4
AFRICASTALKING_SENDER_ID=ELLEDENHOTEL
```

5. Click **"Update Variables"** (bottom right)
6. Railway automatically **redeploys** ⏳ (2-3 minutes)

**Time: 2 minutes**

---

## **STEP 5: Add PostgreSQL Database**

1. Back in Railway Dashboard, click **"+ Add Service"**
2. Select **"Database"** 
3. Choose **"PostgreSQL"**
4. Wait for database to initialize (~30 seconds)
5. Railway automatically creates `DATABASE_URL` variable ✓

**What happens:**
- ✓ PostgreSQL database created
- ✓ `DATABASE_URL` automatically added to variables
- ✓ Migrations run automatically via Procfile

**Time: 1 minute**

---

## **STEP 6: Check Deployment Status**

### **Look for Green Checkmark:**

In Railway Dashboard:
```
✓ Main Service: Healthy (green)
✓ PostgreSQL: Healthy (green)
```

### **If RED (Error):**
1. Click on service
2. Go to **"Logs"** tab
3. Look for error message
4. Common errors:
   - Missing environment variables → Go back to Step 4
   - Database not connected → Restart service
   - Port conflict → Change PORT variable

**Time: 1 minute (or troubleshoot)**

---

## **STEP 7: Get Your App URL**

1. In Railway Dashboard, click your **main service**
2. Look for **"Domains"** section (right side)
3. You'll see something like:
   ```
   https://elleden-hotel-prod-abc123.railway.app
   ```
4. **Copy this URL** - this is your live site!

**Time: 30 seconds**

---

## **STEP 8: Test Your Site (Basic Checks)**

Open your app URL in browser and test:

- [ ] **Homepage loads** → Click link in Railway Domains
- [ ] **Can access /admin/** → Go to: `your-url.railway.app/admin/`
- [ ] **Create superuser** (if needed):
  ```
  In Railway: Click service → Logs → Look for superuser creation prompt
  Or use Railway shell to create manually
  ```
- [ ] **Login works** → Try admin login
- [ ] **Booking page loads** → Go to `/bookings/book/`

**Time: 3 minutes**

---

## **STEP 9: Optional - Add Custom Domain**

### **Only if you have a domain registered:**

1. **Get your domain's nameservers** (from Namecheap/GoDaddy)
   - Usually like: `ns1.namecheap.com`, `ns2.namecheap.com`

2. **In Railway:**
   - Go to Service → Domains
   - Click **"Add Domain"**
   - Enter your domain: `elledenhotel.com`
   - Railway gives you CNAME record

3. **Update at Domain Registrar:**
   - Login to Namecheap/GoDaddy
   - Go to DNS Settings
   - Add Railway's CNAME record
   - Wait 24-48 hours

4. **Verify:**
   - Your site is now: `https://elledenhotel.com` ✓

**Time: 5 minutes (plus 24-48 hours DNS)**

---

## **STEP 10: Monitor & Maintain**

### **Daily Checks:**
1. Go to Railway Dashboard
2. Check if services are **green** (healthy)
3. Click **"Logs"** to see errors
4. Monitor app performance

### **Weekly Tasks:**
- [ ] Test booking flow
- [ ] Test email (password reset)
- [ ] Check M-Pesa payments
- [ ] Review error logs

### **Monthly Tasks:**
- [ ] Check costs on Railway billing
- [ ] Update API keys if needed
- [ ] Backup database (if critical)
- [ ] Review user feedback

**Time: 5-10 minutes/week**

---

## 🎯 **QUICK REFERENCE - What You Just Did**

| Component | Status | Details |
|-----------|--------|---------|
| **Web Server** | ✓ Live | Running on Railway |
| **Database** | ✓ Live | PostgreSQL in Railway |
| **Environment** | ✓ Set | All variables configured |
| **Domain** | ⏳ Optional | Use Railway domain for now |
| **SSL/HTTPS** | ✓ Auto | Railway handles it |
| **Static Files** | ✓ Served | WhiteNoise configured |
| **Email** | ✓ Configured | Gmail SMTP ready |
| **M-Pesa** | ✓ Sandbox | Sandbox mode active |
| **SMS** | ⚠️ Old Key | Will update later |

---

## 📊 **DEPLOYMENT SUMMARY**

```
GitHub Repo:        ✓ Pushed
Environment Setup:  ✓ Complete
Railway Project:    ✓ Created
Services:           ✓ Web + Database
Variables:          ✓ Added
Live URL:           ✓ yourapp.railway.app
Custom Domain:      ⏳ Optional
```

---

## 🐛 **Common Issues & Fixes**

### **Issue: App shows BUILD FAILED**
```
Fix: 
1. Go to Logs tab
2. Look for error message
3. Common: Missing packages → Update requirements.txt
4. Push fix to GitHub → Auto-redeploys
```

### **Issue: DATABASE_URL not found**
```
Fix:
1. Go to PostgreSQL service in Railway
2. Copy the DATABASE_URL from its variables
3. Add to main app service variables
4. Redeploy
```

### **Issue: Page shows 404 or doesn't load**
```
Fix:
1. Check if ALLOWED_HOSTS includes your domain
2. Check DEBUG=False is correct
3. View Logs for Django errors
4. Restart service
```

### **Issue: Emails not sending**
```
Fix:
1. Check EMAIL_HOST_USER and PASSWORD are correct
2. Gmail app password must be 16 chars (no spaces)
3. Check 2-Step Verification is ON in Gmail
4. Test with password reset
```

### **Issue: M-Pesa callback not working**
```
Fix:
1. Go to Step 4 in this guide
2. Update MPESA_CALLBACK_URL with CORRECT domain
3. Make sure it matches Railway domain exactly
4. Test with M-Pesa sandbox
```

---

## ✅ **DEPLOYMENT CHECKLIST - FINAL**

**Before Going Public:**
- [ ] Homepage is loading
- [ ] Admin panel works (/admin/)
- [ ] Can create account
- [ ] Can book a room
- [ ] Payment form shows
- [ ] Email works (test password reset)
- [ ] No error logs showing

**You're Done! 🎉**

Your site is **LIVE** at: `https://your-railway-domain.railway.app`

---

## 📞 **SUPPORT LINKS**

- Railway Docs: https://docs.railway.app
- Railway Status: https://status.railway.app
- Django Deployment: https://docs.djangoproject.com/en/5.0/howto/deployment/
- M-Pesa Sandbox: https://developer.safaricom.co.ke/

---

## 🔄 **NEXT STEPS (AFTER DEPLOYMENT)**

1. **Get new Africa's Talking API key**
   - Go to https://account.africastalking.com
   - Regenerate key
   - Update in Railway Variables

2. **Register custom domain** (optional)
   - Buy from Namecheap/GoDaddy (~$8-15/year)
   - Connect via Railway domains

3. **Monitor the site**
   - Check logs daily
   - Test features weekly
   - Monitor costs monthly

4. **Keep code updated**
   - Make changes locally
   - Push to GitHub
   - Railway auto-deploys

---

**Questions? Check the Logs in Railway Dashboard! 🔍**
