# Render Deployment Checklist ✅

Use this checklist to ensure your CodeVenture deployment is properly configured.

## Pre-Deployment Checklist

### Local Development

- [ ] All code changes committed to Git
- [ ] Tests pass locally (`pytest`)
- [ ] No errors in console when running locally
- [ ] `.env.example` file is up to date
- [ ] `requirements.txt` includes all dependencies
- [ ] `runtime.txt` specifies Python 3.11.7
- [ ] `render.yaml` is properly configured

### Git Repository

- [ ] Latest changes pushed to GitHub
- [ ] Repository is public or Render has access
- [ ] `main` branch is the default branch
- [ ] No sensitive data in Git (secrets, .env files)

## Render Configuration Checklist

### Blueprint Setup

- [ ] Render.yaml includes database configuration
- [ ] Render.yaml includes web service configuration
- [ ] Database and web service in same region (Ohio)
- [ ] Build command includes migrations and collectstatic
- [ ] Start command uses Gunicorn

### Database (codeventure-db)

- [ ] PostgreSQL database created
- [ ] Free tier selected (or appropriate plan)
- [ ] Database name: `codeventure`
- [ ] Region: Ohio (or same as web service)
- [ ] Database accessible from web service

### Web Service (codeventure)

- [ ] Connected to GitHub repository
- [ ] Branch: `main`
- [ ] Environment: Python 3
- [ ] Region: Ohio (same as database)
- [ ] Plan: Free (or appropriate)

## Environment Variables Checklist

### Auto-Configured (via render.yaml)

- [ ] `PYTHON_VERSION` = 3.11.7
- [ ] `DJANGO_SETTINGS_MODULE` = CodeVenture.settings
- [ ] `DJANGO_DEBUG` = false
- [ ] `WEB_CONCURRENCY` = 2
- [ ] `DATABASE_URL` = (auto-generated from database)
- [ ] `DJANGO_SECRET_KEY` = (auto-generated)

### Manual Configuration Required

- [ ] `DJANGO_ALLOWED_HOSTS` = your-app-name.onrender.com
- [ ] `DJANGO_CSRF_TRUSTED_ORIGINS` = https://your-app-name.onrender.com

### Optional (Google OAuth)

- [ ] Google OAuth credentials created
- [ ] Redirect URI configured in Google Cloud Console
- [ ] Social application added in Django admin

## Post-Deployment Checklist

### Immediate Checks (0-5 minutes after deploy)

- [ ] Build completed successfully (check logs)
- [ ] No errors in build logs
- [ ] Migrations ran successfully
- [ ] Static files collected
- [ ] Service status shows "Live"

### Functional Checks (5-15 minutes after deploy)

- [ ] Homepage loads (`https://your-app.onrender.com`)
- [ ] CSS and images load correctly (no 404s)
- [ ] JavaScript works properly
- [ ] Login page accessible
- [ ] Signup page accessible
- [ ] No 500 Internal Server Errors

### Database Checks

- [ ] Admin page accessible (`/admin/`)
- [ ] Can create superuser via Render Shell
- [ ] Database migrations are up to date
- [ ] No database connection errors in logs

### Security Checks

- [ ] HTTP redirects to HTTPS
- [ ] Security headers present (HSTS, X-Frame-Options)
- [ ] Admin panel requires authentication
- [ ] CSRF protection working (forms submit correctly)
- [ ] `DEBUG=False` (check in logs)

### Performance Checks

- [ ] Page load time < 5 seconds
- [ ] Static files load quickly
- [ ] No timeout errors
- [ ] Gunicorn workers running (check logs: "Booting worker")

## Ongoing Maintenance Checklist

### Daily

- [ ] Check service status (green in dashboard)
- [ ] Review error logs for issues
- [ ] Verify site is accessible

### Weekly

- [ ] Check deploy history for failures
- [ ] Review application logs for warnings
- [ ] Test critical user flows (login, signup, etc.)
- [ ] Monitor database size/usage

### Monthly

- [ ] Update Python dependencies
- [ ] Review Django security advisories
- [ ] Check for available database backups
- [ ] Test restore procedure (if applicable)
- [ ] Review and optimize slow queries

### Quarterly

- [ ] Review overall application performance
- [ ] Consider upgrading to paid plan if needed
- [ ] Update Django to latest LTS version
- [ ] Security audit

## Troubleshooting Checklist

### Build Fails

- [ ] Check build logs for specific error
- [ ] Verify all dependencies in requirements.txt
- [ ] Check Python version compatibility
- [ ] Ensure runtime.txt exists and is correct

### 500 Internal Server Error

- [ ] Check application logs in Render dashboard
- [ ] Verify `DJANGO_SECRET_KEY` is set
- [ ] Check `DJANGO_ALLOWED_HOSTS` includes domain
- [ ] Verify `DJANGO_CSRF_TRUSTED_ORIGINS` has https://
- [ ] Ensure database is connected
- [ ] Run `python manage.py check --deploy` in shell

### Static Files Not Loading

- [ ] Check build logs for collectstatic output
- [ ] Verify WhiteNoise in MIDDLEWARE
- [ ] Check `DJANGO_ALLOWED_HOSTS` setting
- [ ] Ensure STATICFILES_STORAGE is set correctly

### Database Connection Issues

- [ ] Verify DATABASE_URL environment variable
- [ ] Check database is in same region
- [ ] Ensure migrations completed successfully
- [ ] Check database isn't full (free tier: 256MB)

### Slow Performance

- [ ] Check if on free tier (sleeps after inactivity)
- [ ] Review database query efficiency
- [ ] Consider increasing worker count
- [ ] Enable database connection pooling
- [ ] Consider upgrading plan

## Quick Commands Reference

### Render Shell Commands

```bash
# Create superuser
python manage.py createsuperuser

# Run migrations
python manage.py migrate

# Check deployment configuration
python manage.py check --deploy

# Open Django shell
python manage.py shell

# Show database tables
python manage.py dbshell
\dt

# Collect static files manually
python manage.py collectstatic --noinput
```

### Local Verification Commands

```bash
# Run deployment verification script
python verify_deployment.py

# Test with production settings locally
DJANGO_DEBUG=False python manage.py runserver

# Check for security issues
python manage.py check --deploy

# Run tests
pytest

# Update a dependency
pip install --upgrade package-name
pip freeze > requirements.txt
```

## Emergency Procedures

### Rollback to Previous Deploy

1. [ ] Go to Render Dashboard → Service
2. [ ] Click "Deploys" tab
3. [ ] Find working deploy
4. [ ] Click "..." menu → "Redeploy"

### Database Issues

1. [ ] Check Render Dashboard → Database → Metrics
2. [ ] Review database logs
3. [ ] If data loss, restore from backup
4. [ ] Contact Render support if persistent

### Complete Service Reset

1. [ ] Export database backup first!
2. [ ] Delete current services in Render
3. [ ] Redeploy using Blueprint
4. [ ] Restore database from backup
5. [ ] Reconfigure environment variables

## Success Criteria

Your deployment is successful when:

✅ Site loads without errors  
✅ All pages accessible  
✅ Login/signup works  
✅ Database connections work  
✅ Static files load  
✅ No errors in logs  
✅ HTTPS working  
✅ Forms submit successfully  

---

**Last Updated**: February 2026  
**Version**: 1.0  
**For**: CodeVenture Render Deployment
