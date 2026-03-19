# Railway Deployment - Build Fixes Complete ✅

## Changes Made to Your Project

### ✅ 1. Fixed psycopg2 Issue
- Changed: `psycopg[binary]>=3.1.0` 
- To: `psycopg2-binary>=2.9.0` (more compatible with Railway)
- **File:** `backend/requirements.txt`

### ✅ 2. Updated Production Settings
- Made SECRET_KEY flexible during build phase
- **File:** `backend/elleden/settings.py`

### ✅ 3. Generated Production SECRET_KEY
```
+rqxtotr@0$%p0u*v!z+xm2^c&a5#-37*h23vkn)k$waexm-v-
```

---

## 🚀 Now Deploy to Railway - Step by Step

### **Step 1: Connect Railway to GitHub**
1. Go to https://railway.app
2. Sign in with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your repo: `Elleden-Hotel`
5. Railway auto-detects Django app

### **Step 2: Add PostgreSQL Database**
1. In Railway project, click **"+ Add"** 
2. Search for **PostgreSQL**
3. Click **"Add PostgreSQL"** (Railway auto-creates `DATABASE_URL`)

### **Step 3: Add Environment Variables**

In Railway dashboard:
1. Click **"Variables"** tab for your Web service
2. **Copy-paste EACH variable below:**

```
SECRET_KEY=+rqxtotr@0$%p0u*v!z+xm2^c&a5#-37*h23vkn)k$waexm-v-
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,.railway.app
DEFAULT_FROM_EMAIL=your-email@gmail.com
EMAIL_HOST=smtp.gmail.com
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-gmail-app-password
EMAIL_PORT=587
EMAIL_USE_TLS=True
MPESA_ENVIRONMENT=sandbox
MPESA_CONSUMER_KEY=your-mpesa-key
MPESA_CONSUMER_SECRET=your-mpesa-secret
MPESA_CALLBACK_URL=https://your-railway-domain/bookings/payment/mpesa-callback/
AFRICASTALKING_USERNAME=your-username
AFRICASTALKING_API_KEY=your-new-api-key
```

**Note:** The DATABASE_URL will be auto-created by PostgreSQL plugin - DON'T add it manually.

### **Step 4: Set Procfile Path (if needed)**
If Railway doesn't auto-detect, add this variable to Web service:
```
RAILWAY_DOCKERFILE_PATH=backend/Dockerfile
```

Or set the working directory to `backend/` in Railway settings.

### **Step 5: Deploy**
1. Click **"Deploy"** button
2. Wait for build to complete (2-3 minutes)
3. Watch logs for any errors

### **Expected Build Output:**
```
Installing dependencies...
✓ Installing Python 3.11.7
✓ Installing pip packages (psycopg2-binary, etc.)
Running release command...
✓ python manage.py migrate
✓ python manage.py collectstatic
Starting web service...
✓ Gunicorn server running
```

---

## ⚠️ If Build Still Fails

**Check Railway logs for specific error:**
1. Railway Dashboard → Your Project
2. Click **"Deployments"** tab
3. Click latest failed deployment
4. Click **"Logs"** - scroll to bottom for red error

**Common errors:**
- `ModuleNotFoundError` → Missing package in requirements.txt
- `ProgrammingError` → Database migration failed
- `FileNotFoundError` → Wrong STATIC_ROOT path

---

## 📝 Production Checklist Before Deploying

- [ ] All environment variables above added to Railway
- [ ] SECRET_KEY is the one generated above
- [ ] DEBUG=False (not True)
- [ ] DATABASE_URL auto-created by PostgreSQL plugin  
- [ ] EMAIL credentials correct (Gmail app password, no spaces)
- [ ] M-Pesa keys updated (optional, can set after)
- [ ] Africa's Talking API key rotated (old key was exposed)

---

## 🎯 After Successful Deployment

1. **Test the site:** Click Railway domain link
2. **Check admin panel:** `/admin/` with your superuser
3. **Rotate Africa's Talking key** (old one is exposed in git history)
4. **Monitor logs** for any 500 errors
5. **(Optional) Register custom domain** via Railway settings

---

## Support

If build fails with different error, share the **full error log** and I'll help fix it.
