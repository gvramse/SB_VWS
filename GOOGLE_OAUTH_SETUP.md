# Google OAuth 2.0 Setup Guide

## 🔑 How to Get Google Client ID and Secret

### Step 1: Access Google Cloud Console
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account
3. Accept terms if prompted

### Step 2: Create or Select a Project
1. **Create New Project** (recommended):
   - Click the project dropdown at the top
   - Click "NEW PROJECT"
   - Enter project name: `Workflow System`
   - Click "CREATE"

2. **Or Select Existing Project**:
   - Choose from the dropdown if you have one

### Step 3: Enable Google+ API (Required)
1. In the left sidebar, go to **APIs & Services** → **Library**
2. Search for "Google+ API" 
3. Click on it and click **ENABLE**
4. *(Note: Even though Google+ is deprecated, this API is still required for basic profile access)*

### Step 4: Configure OAuth Consent Screen
1. Go to **APIs & Services** → **OAuth consent screen**
2. Choose **External** (unless you have Google Workspace)
3. Fill in required fields:
   - **App name**: `Workflow System`
   - **User support email**: Your email
   - **Developer contact information**: Your email
4. Click **SAVE AND CONTINUE**
5. **Scopes**: Click **SAVE AND CONTINUE** (default scopes are fine)
6. **Test users**: Add your email for testing
7. Click **SAVE AND CONTINUE**

### Step 5: Create OAuth 2.0 Credentials
1. Go to **APIs & Services** → **Credentials**
2. Click **+ CREATE CREDENTIALS** → **OAuth client ID**
3. Select **Web application**
4. Configure:
   - **Name**: `Workflow System OAuth`
   - **Authorized JavaScript origins**: 
     ```
     http://localhost:8000
     https://yourdomain.com
     ```
   - **Authorized redirect URIs**:
     ```
     http://localhost:8000/accounts/google/login/callback/
     https://yourdomain.com/accounts/google/login/callback/
     ```
5. Click **CREATE**

### Step 6: Get Your Credentials
After creating, you'll see a popup with:
- **Client ID**: `something.apps.googleusercontent.com`
- **Client Secret**: `GOCSPX-something`

**Copy both values!**

### Step 7: Add to Your .env File
Create/update `sb_vws/.env`:
```bash
# Google OAuth Configuration
GOOGLE_CLIENT_ID=1234567890-abcdefghijklmnopqrstuvwxyz.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-abcdefghijklmnopqrstuvwxyz
```

### Step 8: Test the Integration
1. Restart your Django server:
   ```bash
   python manage.py runserver
   ```
2. Go to: http://localhost:8000/auth/login/
3. Click "Sign in with Google"
4. You should see Google's OAuth consent screen

## 📋 Complete Setup Checklist

### ✅ Google Cloud Console
- [ ] Project created/selected
- [ ] Google+ API enabled
- [ ] OAuth consent screen configured
- [ ] OAuth 2.0 credentials created

### ✅ Django Configuration
- [ ] Client ID added to .env
- [ ] Client secret added to .env
- [ ] Server restarted
- [ ] Social login tested

## 🔧 Common Issues & Solutions

### Issue: "redirect_uri_mismatch"
**Solution**: Check your redirect URIs in Google Console match exactly:
```
http://localhost:8000/accounts/google/login/callback/
```

### Issue: "access_blocked"
**Solution**: Add your email to test users in OAuth consent screen

### Issue: "invalid_client"
**Solution**: Check your Client ID and Secret are correctly copied

### Issue: App not verified
**Solution**: For development, this is normal. Click "Advanced" → "Go to Workflow System (unsafe)"

## 🏢 Production Setup

### For Production Domain
1. Add your production domain to:
   - **Authorized JavaScript origins**: `https://yourdomain.com`
   - **Authorized redirect URIs**: `https://yourdomain.com/accounts/google/login/callback/`

2. Update your production .env:
   ```bash
   GOOGLE_CLIENT_ID=your_production_client_id
   GOOGLE_CLIENT_SECRET=your_production_client_secret
   ```

### App Verification (Optional)
For public apps, you may need Google verification:
1. Go to OAuth consent screen
2. Click "PUBLISH APP"
3. Submit for verification if required

## 🧪 Testing Your Setup

### Test the OAuth Flow
1. **Start server**: `python manage.py runserver`
2. **Visit**: http://localhost:8000/auth/login/
3. **Click**: "Sign in with Google"
4. **Expected flow**:
   - Redirects to Google
   - Shows consent screen
   - Redirects back to your app
   - Creates user account automatically
   - Logs user in

### Verify User Creation
1. Go to Django admin: http://localhost:8000/admin/
2. Check **Users** section
3. You should see a new user with Google email

## 📊 OAuth Scopes Explained

### Default Scopes (configured in settings.py)
```python
'SCOPE': [
    'profile',  # Basic profile info (name, picture)
    'email',    # Email address
]
```

### Additional Scopes (if needed)
```python
'SCOPE': [
    'profile',
    'email',
    'openid',              # OpenID Connect
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email',
]
```

## 🔐 Security Best Practices

### Protect Your Credentials
- ✅ **Never commit** Client Secret to version control
- ✅ **Use environment variables** (.env file)
- ✅ **Different credentials** for development/production
- ✅ **Regular rotation** of secrets

### OAuth Security
- ✅ **HTTPS in production** (required by Google)
- ✅ **Validate redirect URIs** carefully
- ✅ **Monitor OAuth usage** in Google Console
- ✅ **Revoke unused credentials**

## 📞 Support Resources

### Google Documentation
- [OAuth 2.0 Setup](https://developers.google.com/identity/protocols/oauth2)
- [Google Console Help](https://support.google.com/cloud/answer/6158849)

### Django-allauth Documentation
- [Google Provider](https://django-allauth.readthedocs.io/en/latest/providers.html#google)
- [Configuration Options](https://django-allauth.readthedocs.io/en/latest/configuration.html)

---

**🎉 That's it! Your Google OAuth integration should now be working!**

After following these steps, users can sign in to your Django Workflow System using their Google accounts.
