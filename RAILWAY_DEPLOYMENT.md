# Railway Deployment Guide - Elleden Hotel

## Overview
This guide walks you through deploying the Elleden Hotel application to Railway.

---

## 📋 Prerequisites

- Railway account (https://railway.app)
- GitHub account with your code pushed
- All environment variables documented below

---

## 🚀 Step-by-Step Deployment

### Step 1: Connect GitHub to Railway

1. Go to [Railway.app](https://railway.app)
2. Click **"Start a New Project"**
3. Select **"Deploy from GitHub"**
4. Authorize Railway to access your GitHub account
5. Select your `Elleden-Hotel` repository
6. Click **"Deploy"**

Railway will automatically detect the `Procfile` and deploy your app.

---

### Step 2: Set Environment Variables in Railway

After the initial deployment attempt, go to your project settings and add these variables:

#### **Django Settings**
```
SECRET_KEY=django-superhz#aqk!qmj3-a)svo)$&6r2=f5hs7b5je=w#3^2&z=nqr7%p0&v9
DEBUG=False
ALLOWED_HOSTS=your-app-name.railway.app,www.your-app-name.railway.app
```

#### **Database** (Railway Postgres Plugin)
- Railway will auto-create `DATABASE_URL` when you add PostgreSQL
- You don't need to set this manually

#### **Email Settings**
```
EMAIL_HOST_USER=elledenhotelltd@gmail.com
EMAIL_HOST_PASSWORD=bcanouvfydpjokpy
```

#### **M-Pesa Settings** (Sandbox)
```
MPESA_ENVIRONMENT=sandbox
MPESA_CONSUMER_KEY=uLdcxbFm1VC4yNGUO2zZiXJneeksC7I93XOdeZQc7gCG3R9N
MPESA_CONSUMER_SECRET=HpAdvzwtdCaO8N7mGKOt5sLMRXgHpGmzzFZ3AIg0vAQ8V6BnbpJdlI5WIJlajZli
MPESA_SHORTCODE=174379
MPESA_PASSKEY=bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919
MPESA_CALLBACK_URL=https://your-app-name.railway.app/bookings/mpesa/callback/
```

#### **Africa's Talking SMS Settings**
```
AFRICASTALKING_USERNAME=elledenhotel
AFRICASTALKING_API_KEY=atsk_36edf8ab6f1b702ed43fd4727fac4abad432827e87b97df0d04f263063a1026bfb2bdbd4
AFRICASTALKING_SENDER_ID=ELLEDENHOTEL
```

---

### Step 3: Add PostgreSQL Database

1. In your Railway project, click **"+ New Service"**
2. Select **"Add Database"** → **"PostgreSQL"**
3. Railway automatically sets `DATABASE_URL` environment variable
4. The database will migrate automatically via the `release` command in Procfile

---

### Step 4: How to Set Variables in Railway Dashboard

1. Go to your Railway project
2. Click on your service (the app name)
3. Click on the **"Variables"** tab
4. Click **"+ New Variable"** for each environment variable
5. Enter the **Key** and **Value**
6. Example:
   ```
   Key: ALLOWED_HOSTS
   Value: elleden-hotel.railway.app
   ```
7. Click **"Save & Redeploy"** after adding variables

---

### Step 5: Verify Deployment

1. Once deployment is complete, visit your app URL: `https://your-app-name.railway.app`
2. Test the booking flow
3. Check email sending works
4. Verify M-Pesa integration (sandbox mode)

---

## 🔧 Finding Your App Domain

After deployment, your app URL will be:
- Format: `https://yourapp-prod.railway.app` (Railway format)
- Check the **"Domain"** section in Railway Dashboard

Replace `your-app-name.railway.app` with your actual domain in:
- `ALLOWED_HOSTS`
- `MPESA_CALLBACK_URL`

---

## 📝 Production Checklist

Before going live:

- [ ] `DEBUG=False` in production variables
- [ ] All API keys set correctly
- [ ] Email provider working (test password reset)
- [ ] M-Pesa callback URL updated
- [ ] Database migrations ran successfully
- [ ] Static files collected
- [ ] Superuser created on production
- [ ] HTTPS enabled (Railway handles this automatically)

---

## 🆘 Troubleshooting

### Build Fails
- Check `Procfile` syntax
- Ensure `requirements.txt` is current: `pip freeze > requirements.txt`
- Check deployment logs in Railway Dashboard

### Database Connection Error
- Verify `DATABASE_URL` is set
- Check PostgreSQL service is running

### Static Files Not Loading
- Run `python manage.py collectstatic --noinput` locally
- Verify `STATIC_ROOT` in settings.py

### Email Not Sending
- Test locally with `DEBUG=False`
- Verify Gmail app password (16 characters, no spaces)
- Check email configuration in settings

---

## 📞 Support

For issues with Railway, visit: https://railway.app/support

---

## Summary

| Variable | Purpose | Value |
|----------|---------|-------|
| `SECRET_KEY` | Django encryption | Generate & keep secret |
| `DEBUG` | Debug mode | `False` (production) |
| `ALLOWED_HOSTS` | Allowed domains | Your Railway domain |
| `DATABASE_URL` | PostgreSQL connection | Auto-set by Railway |
| `EMAIL_HOST_PASSWORD` | Gmail app password | 16-char app password |
| `MPESA_*` | M-Pesa credentials | From Safaricom Dashboard |
| `AFRICASTALKING_*` | SMS credentials | From AT Dashboard |

---

**You're ready to deploy!** 🎉
