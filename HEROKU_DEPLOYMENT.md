# Heroku Deployment Guide for SB Volunteer Workflow System

## Prerequisites

1. **Heroku Account**: Sign up at [heroku.com](https://heroku.com)
2. **Heroku CLI**: Install from [devcenter.heroku.com/articles/heroku-cli](https://devcenter.heroku.com/articles/heroku-cli)
3. **Git**: Ensure your code is committed to Git (already done ✅)

## Step 1: Login to Heroku

```bash
heroku login
```

## Step 2: Create Heroku Application

```bash
# Create a new Heroku app (replace 'your-app-name' with your desired name)
heroku create sb-volunteer-workflow-system

# Or if you want a specific name:
heroku create your-preferred-name
```

## Step 3: Add PostgreSQL Database

```bash
# Add PostgreSQL database addon (free tier)
heroku addons:create heroku-postgresql:essential-0

# Check database URL
heroku config:get DATABASE_URL
```

## Step 4: Configure Environment Variables

```bash
# Generate a new secret key
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Set environment variables
heroku config:set SECRET_KEY="your-generated-secret-key-here"
heroku config:set DEBUG=False
heroku config:set DJANGO_SETTINGS_MODULE=workflow_system.settings

# Email configuration (for task notifications)
heroku config:set EMAIL_HOST_USER="sbvwsdmn@gmail.com"
heroku config:set EMAIL_HOST_PASSWORD="ssko xlye iukl bmrz"

# Google OAuth configuration (if using social auth)
heroku config:set GOOGLE_OAUTH2_CLIENT_ID="your-google-client-id"
heroku config:set GOOGLE_OAUTH2_CLIENT_SECRET="your-google-client-secret"

# Additional security settings
heroku config:set ALLOWED_HOSTS=".herokuapp.com"
```

## Step 5: Deploy to Heroku

```bash
# Add Heroku remote (if not done automatically)
heroku git:remote -a your-app-name

# Deploy to Heroku
git push heroku main
```

## Step 6: Run Database Migrations

```bash
# Run migrations (this happens automatically via Procfile, but you can run manually)
heroku run python manage.py migrate

# Create superuser for admin access
heroku run python manage.py createsuperuser

# Populate sample data (optional)
heroku run python manage.py populate_sample_tasks
```

## Step 7: Configure Django Sites Framework

```bash
# Update site domain for Heroku
heroku run python manage.py shell
```

In the shell, run:
```python
from django.contrib.sites.models import Site
site = Site.objects.get(pk=1)
site.domain = 'your-app-name.herokuapp.com'
site.name = 'SB Volunteer Workflow System'
site.save()
exit()
```

## Step 8: Configure Social Authentication (If Using Google OAuth)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Update OAuth redirect URIs to include:
   - `https://your-app-name.herokuapp.com/accounts/google/login/callback/`
3. Update the SocialApplication in Django admin:
   ```bash
   heroku open /admin/
   ```

## Step 9: Test Deployment

```bash
# Open your application
heroku open

# Check logs if there are issues
heroku logs --tail
```

## Useful Heroku Commands

```bash
# View application logs
heroku logs --tail

# Restart application
heroku restart

# Open application in browser
heroku open

# Access Django shell
heroku run python manage.py shell

# Run custom management commands
heroku run python manage.py <command>

# Scale dynos
heroku ps:scale web=1

# Check dyno status
heroku ps

# View configuration variables
heroku config
```

## Environment Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `generated-secret-key` |
| `DEBUG` | Debug mode | `False` |
| `DATABASE_URL` | PostgreSQL URL | `postgres://...` (auto-set) |
| `EMAIL_HOST_USER` | Gmail username | `sbvwsdmn@gmail.com` |
| `EMAIL_HOST_PASSWORD` | Gmail app password | `ssko xlye iukl bmrz` |
| `GOOGLE_OAUTH2_CLIENT_ID` | Google OAuth client ID | `your-client-id.googleusercontent.com` |
| `GOOGLE_OAUTH2_CLIENT_SECRET` | Google OAuth secret | `your-client-secret` |

## File Structure Added for Heroku

```
sb_vws/
├── Procfile                    # Heroku process configuration
├── runtime.txt                 # Python version specification
├── requirements.txt            # Updated with production dependencies
├── HEROKU_DEPLOYMENT.md        # This deployment guide
└── workflow_system/
    └── settings.py             # Updated for production
```

## Production Features Enabled

✅ **PostgreSQL Database**: Automatic database switching
✅ **Static Files**: WhiteNoise for efficient static file serving
✅ **Security**: HTTPS redirects, secure cookies, HSTS headers
✅ **Logging**: Comprehensive logging configuration
✅ **CORS**: Cross-origin request handling
✅ **Automatic Migrations**: Via Procfile release phase

## Troubleshooting

### Common Issues:

1. **Static Files Not Loading**:
   ```bash
   heroku run python manage.py collectstatic --noinput
   ```

2. **Database Connection Errors**:
   ```bash
   heroku config:get DATABASE_URL
   heroku run python manage.py migrate
   ```

3. **Application Crashes**:
   ```bash
   heroku logs --tail
   ```

4. **Google OAuth Errors**:
   - Update redirect URIs in Google Cloud Console
   - Update SocialApplication domain in Django admin

### Support Resources:

- [Heroku Django Documentation](https://devcenter.heroku.com/articles/django-app-configuration)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [Heroku Support](https://help.heroku.com/)

## Post-Deployment Checklist

- [ ] Application loads successfully
- [ ] Database migrations completed
- [ ] Superuser account created
- [ ] Static files loading properly
- [ ] Email notifications working
- [ ] Google OAuth configured (if using)
- [ ] Admin panel accessible
- [ ] SSL certificate active
- [ ] Domain configured correctly

Your SB Volunteer Workflow System is now live on Heroku! 🚀
