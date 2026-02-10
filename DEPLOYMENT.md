# CodeVenture Deployment Guide

## Pre-Deployment Checklist ✅

### Fixed Issues
- ✅ Updated all dependencies to Python 3.11 compatible versions
- ✅ Fixed Pillow compatibility (10.1.0 → 11.1.0)
- ✅ Updated Django to latest 4.2.x LTS (4.2.17)
- ✅ Upgraded all security packages (cryptography, urllib3, certifi)
- ✅ Added `runtime.txt` to specify Python 3.11.7
- ✅ Enhanced `render.yaml` with production-ready gunicorn configuration
- ✅ Removed legacy documentation files from root
- ✅ Kept main features documentation in `Documents/` folder

### Current Project Structure
```
CodeVenture/
├── Documents/                    # Project documentation
│   └── Main features implemented for Code Venture.pdf
├── CodeVenture/                  # Django project settings
├── WelcomePage/                  # Landing page & auth
├── UserManagement/               # User profiles & roles
├── LearningResource/             # Learning modules
├── QuizChallengeSystem/          # Quizzes & coding challenges
├── PythonPlayground/             # Integrated Python IDE
├── ProgressTracker/              # Student progress tracking
├── requirements.txt              # Python dependencies
├── runtime.txt                   # Python version specification
├── render.yaml                   # Render deployment config
├── .env.example                  # Environment variable template
└── README.md                     # Project documentation
```

## Render Deployment Steps 🚀

### 1. Push Changes to GitHub
```bash
git add .
git commit -m "fix: update dependencies for Python 3.11 and production deployment"
git push origin main
```

### 2. Create PostgreSQL Database on Render
1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **New** → **PostgreSQL**
3. Configure:
   - **Name**: `codeventure-db`
   - **Database**: `codeventure`
   - **User**: (auto-generated)
   - **Region**: Same as your web service
   - **Plan**: Free
4. Click **Create Database**
5. Copy the **Internal Database URL** (starts with `postgresql://`)

### 3. Deploy Web Service on Render
1. In Render Dashboard, click **New** → **Web Service**
2. Connect your GitHub repository: `matthewcks-prog/CodeVenture`
3. Configure the service:
   - **Name**: `codeventure`
   - **Environment**: Python 3
   - **Region**: Same as database
   - **Branch**: main
   - **Build Command**: (auto-detected from render.yaml)
   - **Start Command**: (auto-detected from render.yaml)
   - **Plan**: Free

### 4. Configure Environment Variables
In the Render Web Service settings, add these environment variables:

#### Required Variables
```bash
# Django Secret Key (generate a strong random string)
DJANGO_SECRET_KEY=your-super-secret-key-here-min-50-chars

# Database URL (from step 2)
DATABASE_URL=postgresql://user:password@host/codeventure

# Django Settings
DJANGO_DEBUG=False
DJANGO_SETTINGS_MODULE=CodeVenture.settings

# Allowed Hosts (your Render URL)
DJANGO_ALLOWED_HOSTS=codeventure.onrender.com

# CSRF Trusted Origins (with https://)
DJANGO_CSRF_TRUSTED_ORIGINS=https://codeventure.onrender.com

# Gunicorn Workers
WEB_CONCURRENCY=2
```

#### Generate Secret Key
You can generate a secure secret key using:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 5. Deploy
1. Click **Create Web Service**
2. Render will automatically:
   - Install Python 3.11.7
   - Install all dependencies from `requirements.txt`
   - Run `collectstatic` to gather static files
   - Run migrations to set up the database
   - Start gunicorn with 2 workers

### 6. Verify Deployment
After deployment completes (5-10 minutes):

1. Visit your app URL: `https://codeventure.onrender.com`
2. Check that:
   - ✅ Homepage loads correctly
   - ✅ Static files (CSS, images) are served
   - ✅ Login/signup works
   - ✅ Google OAuth works (if configured)
   - ✅ Database connections work

### 7. Monitor Logs
View logs in Render Dashboard → Your Service → Logs to check for any issues.

## Post-Deployment Configuration

### Enable Google OAuth (Optional)
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create OAuth 2.0 credentials
3. Add authorized redirect URI: `https://codeventure.onrender.com/accounts/google/login/callback/`
4. In Django admin, add Social Application with Client ID and Secret

### Create Superuser
In Render Shell (Dashboard → Your Service → Shell):
```bash
python manage.py createsuperuser
```

### Run Django Deployment Checklist
```bash
python manage.py check --deploy
```

## Troubleshooting 🔧

### Build Fails with Dependency Errors
- Check that `runtime.txt` specifies Python 3.11.7
- Verify all packages in `requirements.txt` support Python 3.11
- Check build logs for specific error messages

### Static Files Not Loading
- Ensure `DJANGO_ALLOWED_HOSTS` includes your Render domain
- Verify `python manage.py collectstatic` ran successfully in build logs
- Check WhiteNoise is in `MIDDLEWARE` (already configured)

### Database Connection Issues
- Verify `DATABASE_URL` environment variable is set correctly
- Check database is in the same region as web service
- Ensure migrations ran successfully: `python manage.py migrate`

### 500 Internal Server Error
- Check Render logs for detailed error messages
- Verify `DJANGO_SECRET_KEY` is set
- Ensure `DJANGO_DEBUG=False` in production
- Check `DJANGO_CSRF_TRUSTED_ORIGINS` includes your domain with `https://`

## Production Best Practices ✨

### Security
- ✅ `DEBUG=False` in production
- ✅ Strong `SECRET_KEY` (50+ characters)
- ✅ HTTPS enforced (configured in settings.py)
- ✅ Secure cookies enabled
- ✅ HSTS headers configured
- ✅ CSRF protection enabled

### Performance
- ✅ WhiteNoise for static file serving
- ✅ Gunicorn with 2 workers
- ✅ 120-second timeout for long requests
- ✅ Static file compression enabled
- ✅ Database connection pooling (PostgreSQL)

### Scalability
- Database migrations automated in build
- Static files collected automatically
- Environment-based configuration
- Modular Django app architecture
- Separation of concerns (apps by feature)

### Maintainability
- Clean project structure
- Comprehensive test coverage
- Clear documentation
- Version-pinned dependencies
- Git-based deployments

## Monitoring & Maintenance

### Regular Tasks
- Monitor Render logs for errors
- Check application performance metrics
- Update dependencies regularly for security patches
- Backup PostgreSQL database periodically
- Review Django security advisories

### Updating Dependencies
```bash
# Update specific package
pip install --upgrade package-name
pip freeze > requirements.txt

# Or update all packages (test thoroughly!)
pip list --outdated
```

## Support & Resources

- [Render Documentation](https://render.com/docs)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [WhiteNoise Documentation](http://whitenoise.evans.io/)
- [Gunicorn Configuration](https://docs.gunicorn.org/en/stable/configure.html)

---

**Your CodeVenture app is now production-ready! 🎉**
