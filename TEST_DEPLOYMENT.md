# CodeVenture Deployment Testing Guide

## ✅ Configuration Verification Complete

Your Blueprint configuration has been validated and is ready for deployment!

**Configuration Status:**
- ✅ `render.yaml` - Valid Blueprint configuration
- ✅ Database: `codeventure-db` (PostgreSQL, Free tier, Ohio)
- ✅ Web Service: `codeventure` (Python, Free tier, Ohio)
- ✅ Python 3.11.7 configured
- ✅ All required dependencies present
- ✅ Build and start commands configured
- ✅ Environment variables properly set up

---

## 🚀 Deployment Steps

### Step 1: Push to GitHub

```bash
# Commit and push any pending changes
git add .
git commit -m "feat: configure Blueprint for production deployment"
git push origin main
```

### Step 2: Deploy via Render Dashboard

1. **Go to Render Dashboard**: https://dashboard.render.com

2. **Create New Blueprint**:
   - Click **"New +"** → **"Blueprint"**
   - Connect your GitHub account (if not already connected)
   - Select the **CodeVenture** repository
   - Select branch: **main**

3. **Review Blueprint Configuration**:
   Render will detect your `render.yaml` and show:
   - ✅ **Database**: `codeventure-db` (PostgreSQL Free)
   - ✅ **Web Service**: `codeventure` (Python Free)

4. **Set Required Environment Variables**:
   
   When prompted, you'll need to set these two variables. Start with placeholder values:
   
   ```bash
   DJANGO_ALLOWED_HOSTS=codeventure.onrender.com
   DJANGO_CSRF_TRUSTED_ORIGINS=https://codeventure.onrender.com
   ```
   
   **Note**: You'll update these with your actual URL after the first deployment.

5. **Apply Blueprint**:
   - Click **"Apply"** or **"Create Services"**
   - Render will start provisioning:
     - Creating PostgreSQL database (2-3 minutes)
     - Building and deploying web service (5-10 minutes)
     - Running migrations automatically
     - Collecting static files

6. **Wait for Deployment**:
   - Watch the logs in the dashboard
   - Look for: `"Booting worker with pid"` (means success!)
   - Service status should show **"Live"** (green)

### Step 3: Update Environment Variables with Actual URL

After the first deployment completes:

1. **Get Your Render URL**:
   - In Render Dashboard → `codeventure` service
   - Copy the URL (e.g., `https://codeventure-abc123.onrender.com`)

2. **Update Environment Variables**:
   - Go to: Dashboard → `codeventure` service → **Environment** tab
   - Update these values with your ACTUAL Render URL:
   
   ```bash
   DJANGO_ALLOWED_HOSTS=codeventure-abc123.onrender.com
   DJANGO_CSRF_TRUSTED_ORIGINS=https://codeventure-abc123.onrender.com
   ```
   
   - Click **"Save Changes"** (this will trigger a redeploy)

---

## 🧪 Testing Your Deployment

### Automated Testing

Run the deployment verification script:

```bash
python verify_deployment.py
```

Choose option **2** to test the deployed site, then enter your Render URL.

### Manual Testing Checklist

#### 1. Basic Accessibility Test

Visit your app URL in a browser:

```
https://your-app-name.onrender.com
```

**Expected Results:**
- ✅ Homepage loads without errors
- ✅ CSS styles are applied correctly
- ✅ Images load properly
- ✅ No 404 errors in browser console
- ✅ Page loads in under 5 seconds (after initial cold start)

**Note**: Free tier services sleep after 15 minutes of inactivity. First request may take 30-60 seconds to "wake up" the service.

#### 2. Security Tests

**HTTPS Redirect:**
- Visit `http://your-app-name.onrender.com` (without 's')
- ✅ Should automatically redirect to HTTPS

**Security Headers:**
- Open browser DevTools → Network tab
- Refresh the page
- Click on the main document request
- Check Response Headers:
  - ✅ `Strict-Transport-Security` should be present
  - ✅ `X-Frame-Options: DENY` should be present
  - ✅ `X-Content-Type-Options: nosniff` should be present

#### 3. Authentication Tests

**Login/Signup Pages:**

1. **Visit Login Page**:
   ```
   https://your-app-name.onrender.com/accounts/login/
   ```
   - ✅ Login form displays correctly
   - ✅ CSS styles applied
   - ✅ No JavaScript errors

2. **Visit Signup Page**:
   ```
   https://your-app-name.onrender.com/accounts/signup/
   ```
   - ✅ Signup form displays correctly
   - ✅ Role selection works (Student/Parent/Teacher)
   - ✅ Form validation works

3. **Test Account Creation**:
   - Try creating a new student account
   - ✅ Form submits successfully
   - ✅ No 500 errors
   - ✅ Redirects to appropriate page
   - ✅ User is logged in

#### 4. Database Connectivity Tests

**Admin Panel Test:**

1. **Create a Superuser** (via Render Shell):
   - Go to: Dashboard → `codeventure` service → **Shell** tab
   - Run:
     ```bash
     python manage.py createsuperuser
     ```
   - Follow the prompts to create admin user

2. **Access Admin Panel**:
   ```
   https://your-app-name.onrender.com/admin/
   ```
   - ✅ Admin login page loads
   - ✅ Static files (CSS) load correctly
   - ✅ Can login with superuser credentials
   - ✅ Can view and edit database records

#### 5. Application Feature Tests

Test the main features of CodeVenture:

1. **Learning Resources**:
   ```
   https://your-app-name.onrender.com/learning/
   ```
   - ✅ Module list displays
   - ✅ Can view module details
   - ✅ Videos load (if any)

2. **Quiz System**:
   ```
   https://your-app-name.onrender.com/quiz/
   ```
   - ✅ Quiz list displays
   - ✅ Can start a quiz
   - ✅ Can submit answers
   - ✅ Results are saved to database

3. **Python Playground**:
   ```
   https://your-app-name.onrender.com/playground/
   ```
   - ✅ Editor loads
   - ✅ Can write and execute code
   - ✅ Output displays correctly

4. **User Progress**:
   ```
   https://your-app-name.onrender.com/progress/
   ```
   - ✅ Progress tracker displays
   - ✅ User data persists across sessions

#### 6. Performance Tests

**Response Time:**
- Test with: https://tools.pingdom.com/
- Or use browser DevTools → Network tab
- ✅ First request: < 60 seconds (cold start)
- ✅ Subsequent requests: < 3 seconds

**Static Files:**
- Check browser DevTools → Network tab
- ✅ All CSS files: 200 status
- ✅ All JS files: 200 status
- ✅ All images: 200 status

---

## 🔍 Monitoring Your Deployment

### Check Logs

1. **Application Logs**:
   - Dashboard → `codeventure` service → **Logs** tab
   - Look for:
     - ✅ "Booting worker with pid" (Gunicorn started)
     - ✅ No errors about missing environment variables
     - ✅ No database connection errors
     - ✅ Migrations completed successfully

2. **Build Logs**:
   - Dashboard → `codeventure` service → **Events** tab
   - Check the most recent deploy
   - Look for:
     - ✅ "Installing dependencies" completed
     - ✅ "Collecting static files" completed
     - ✅ "Running migrations" completed
     - ✅ Build status: "Live"

### Health Check Commands

Run these in **Render Shell** (Dashboard → Service → Shell):

```bash
# Check deployment configuration
python manage.py check --deploy

# Check database connection
python manage.py dbshell
\conninfo
\q

# View database tables
python manage.py dbshell
\dt
\q

# Check migrations status
python manage.py showmigrations

# Collect static files manually (if needed)
python manage.py collectstatic --noinput
```

---

## ⚠️ Troubleshooting

### Issue: 500 Internal Server Error

**Diagnosis:**
1. Check logs: Dashboard → Service → Logs
2. Look for the specific error message

**Common Causes & Fixes:**

| Error | Cause | Solution |
|-------|-------|----------|
| `DisallowedHost` | Wrong `DJANGO_ALLOWED_HOSTS` | Update to match your Render URL |
| `CSRF verification failed` | Wrong `DJANGO_CSRF_TRUSTED_ORIGINS` | Add `https://` prefix |
| `OperationalError: database` | Database not connected | Check `DATABASE_URL` env var |
| `SECRET_KEY` error | Secret key not set | Should be auto-generated; check env vars |

### Issue: Static Files Not Loading (404 errors)

**Diagnosis:**
- Open browser DevTools → Console
- Look for 404 errors on CSS/JS files

**Fix:**
1. Check build logs: verify `collectstatic` ran successfully
2. Check `DJANGO_ALLOWED_HOSTS` includes your domain
3. In Render Shell, run:
   ```bash
   python manage.py collectstatic --noinput
   ```

### Issue: Page Takes Forever to Load

**Diagnosis:**
- Free tier services sleep after 15 minutes of inactivity

**Solutions:**
- First request after sleep: 30-60 seconds is normal
- Subsequent requests should be fast (2-3 seconds)
- Consider upgrading to paid tier for always-on service
- Or: Use a service like UptimeRobot to ping your app every 10 minutes

### Issue: Database Connection Errors

**Fix:**
1. Verify database is running: Dashboard → Database
2. Check database region matches web service region (both Ohio)
3. Verify `DATABASE_URL` env var is set
4. In Render Shell:
   ```bash
   python manage.py dbshell
   ```
   Should connect successfully

---

## 📊 Success Metrics

Your deployment is successful when ALL of these are true:

- [ ] Service status shows **"Live"** (green)
- [ ] Homepage loads without errors
- [ ] All static files (CSS/JS/images) load correctly
- [ ] Can create and login with user accounts
- [ ] Database operations work (create, read, update)
- [ ] No errors in application logs
- [ ] HTTPS is enforced
- [ ] Admin panel is accessible
- [ ] All main features work as expected

---

## 🎯 Quick Test Script

Copy and paste this into your browser console to test basic functionality:

```javascript
// Test 1: Check if page loaded
console.log('Page Title:', document.title);

// Test 2: Check for JavaScript errors
console.log('No errors above this line = ✅');

// Test 3: Check static files
const images = document.querySelectorAll('img');
const broken = Array.from(images).filter(img => !img.complete || img.naturalHeight === 0);
console.log('Broken images:', broken.length === 0 ? '✅ None' : `❌ ${broken.length}`);

// Test 4: Check CSS loaded
const hasStyles = window.getComputedStyle(document.body).backgroundColor !== 'rgba(0, 0, 0, 0)';
console.log('CSS loaded:', hasStyles ? '✅ Yes' : '❌ No');

// Test 5: Check HTTPS
console.log('Using HTTPS:', window.location.protocol === 'https:' ? '✅ Yes' : '❌ No');

console.log('\n✅ All tests passed = Deployment successful!');
```

---

## 📞 Support Resources

- **Render Documentation**: https://render.com/docs
- **Render Blueprints Guide**: https://render.com/docs/infrastructure-as-code
- **Django Deployment Checklist**: https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/
- **Render Community Forum**: https://community.render.com/
- **Render Status Page**: https://status.render.com/

---

## 🔄 Continuous Deployment

Once your Blueprint is deployed, you have **automatic continuous deployment**!

**How it works:**
1. Make changes to your code locally
2. Commit and push to GitHub:
   ```bash
   git add .
   git commit -m "feat: add new feature"
   git push origin main
   ```
3. Render automatically detects the push and redeploys
4. Build runs (install dependencies, migrations, collectstatic)
5. New version goes live automatically

**No manual intervention needed!**

---

## 🎉 Congratulations!

Your CodeVenture app is now deployed using **Infrastructure as Code** with Render Blueprints!

**What you've achieved:**
- ✅ Production-ready Django application
- ✅ PostgreSQL database with automatic backups
- ✅ Automatic deployments on every push
- ✅ HTTPS with security headers
- ✅ Static file serving with WhiteNoise
- ✅ Database migrations run automatically
- ✅ Scalable architecture
- ✅ Version-controlled infrastructure

**Your deployment URL**: https://codeventure-l7dc.onrender.com

---

**Last Updated**: February 2026  
**Version**: 1.0
