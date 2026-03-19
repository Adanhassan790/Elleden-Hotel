# ⚡ RAILWAY DEPLOYMENT - QUICK CHECKLIST

## 🚀 DEPLOY IN 10 MINUTES

Copy-paste this checklist and follow step by step:

```
═══════════════════════════════════════════════════════════════
RAILWAY DEPLOYMENT - 10 MINUTE CHECKLIST
═══════════════════════════════════════════════════════════════

⏱️ TOTAL TIME: ~10 minutes

STEP 1: Create Railway Account
[ ] Go to https://railway.app
[ ] Click "Sign Up"
[ ] Choose "Continue with GitHub"
[ ] Authorize Railway
[ ] Email confirmed
⏱️ TIME: 2 minutes

STEP 2: Create New Project & Deploy
[ ] Go to Railway Dashboard
[ ] Click "+ New Project"
[ ] Select "Deploy from GitHub repo"
[ ] Find & select: Adanhassan790/Elleden-Hotel
[ ] Wait for deployment to start
⏱️ TIME: 1 minute

STEP 3: Wait for Build
[ ] Watch "Building..." status
[ ] Wait 5 minutes for build to complete
⏱️ TIME: 5 minutes

STEP 4: Add Environment Variables ⚠️ CRITICAL
[ ] Click on main service (in Railway)
[ ] Go to "Variables" tab
[ ] Click "RAW Editor"
[ ] Copy-paste this ENTIRE block:

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

[ ] Click "Update Variables"
[ ] Wait for auto-redeploy (2-3 minutes)
⏱️ TIME: 2 minutes

STEP 5: Add PostgreSQL Database
[ ] Click "+ Add Service"
[ ] Select "Database"
[ ] Choose "PostgreSQL"
[ ] Wait 30 seconds for creation
[ ] Verify DATABASE_URL is auto-created
⏱️ TIME: 1 minute

STEP 6: Verify Everything is Green
[ ] Check main service: GREEN ✓
[ ] Check PostgreSQL: GREEN ✓
[ ] If RED: Go to Logs tab and check error
⏱️ TIME: 1 minute

STEP 7: Get Your Live URL
[ ] Click main service
[ ] Look at "Domains" section
[ ] Copy your Railway domain
[ ] Example: https://elleden-hotel-prod-abc123.railway.app
[ ] SAVE THIS URL!
⏱️ TIME: 30 seconds

STEP 8: Test Your Site
[ ] Open your Railway URL in browser
[ ] Check homepage loads
[ ] Check /admin/ page
[ ] Try /bookings/book/ page
[ ] Everything working? ✓ YOU'RE DONE!
⏱️ TIME: 2 minutes

═══════════════════════════════════════════════════════════════
✅ DEPLOYMENT COMPLETE!
Your site is LIVE at: https://your-railway-domain.railway.app
═══════════════════════════════════════════════════════════════
```

---

## 📱 **EASY COPY-PASTE ENVIRONMENT VARIABLES**

When you paste variables, copy this entire block (Step 4 above):

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
AFRICESSTALKING_SENDER_ID=ELLEDENHOTEL
```

---

## 🎯 **YOUR LIVE SITE URL**

After Step 7, you'll have something like:
```
https://elleden-hotel-prod-abc123.railway.app
```

**TEST THESE LINKS:**
- Homepage: `https://your-url.railway.app`
- Admin: `https://your-url.railway.app/admin/`
- Booking: `https://your-url.railway.app/bookings/book/`

---

## ⚠️ **IMPORTANT NOTES**

1. **MPESA_CALLBACK_URL:** Replace `your-app-domain` with your actual Railway domain after Step 7

2. **Environment Variables:** Once added, Railway auto-redeploys (wait 2-3 minutes)

3. **Database:** PostgreSQL takes 30 seconds to create, then auto-connects

4. **Go Live:** Your site is public immediately! Anyone can access it!

5. **Errors:** If something fails, check Railway Logs (click service → Logs)

---

## 🚨 **IF SOMETHING GOES WRONG**

1. **Build Failed:** Check Logs → likely missing package
2. **Database error:** Add PostgreSQL again (Step 5)
3. **Page not found:** Check ALLOWED_HOSTS variable
4. **Email not working:** Check EMAIL variables are correct
5. **M-Pesa broken:** Update MPESA_CALLBACK_URL with correct domain

---

## ✅ **YOU ARE DONE WHEN:**

- [ ] Deployed on Railway ✓
- [ ] Environment variables set ✓
- [ ] Database created ✓
- [ ] Site loads at your URL ✓
- [ ] Admin page works ✓
- [ ] Booking page works ✓

**Congratulations! Your site is LIVE! 🎉**

---

## 📚 **REFERENCE DOCUMENTS**

In your project folder:
- `RAILWAY_DEPLOY_STEPS.md` - Full detailed guide
- `RAILWAY_ENV_VARIABLES.txt` - All variables reference
- `RAILWAY_DEPLOYMENT.md` - Original deployment guide

---

**Questions? Check Railway Dashboard → Logs tab for error messages!**
