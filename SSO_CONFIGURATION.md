# Enterprise SSO Configuration Guide

This guide covers the complete setup of enterprise-wide Single Sign-On (SSO) authentication for the Django Workflow System.

## 🏢 Available SSO Methods

### ✅ 1. Social Authentication (django-allauth)
- **Google** - OAuth 2.0
- **GitHub** - OAuth 2.0  
- **Microsoft** - OAuth 2.0/OpenID Connect
- **LinkedIn** - OAuth 2.0

### ✅ 2. SAML SSO (djangosaml2)
- **Enterprise Identity Providers**
- **Active Directory Federation Services (ADFS)**
- **Azure AD SAML**
- **Okta SAML**
- **Auth0 SAML**

### ✅ 3. OAuth2 Provider (django-oauth-toolkit)
- **Custom OAuth2 applications**
- **API access tokens**
- **Third-party integrations**

### 🔧 4. LDAP/Active Directory (django-auth-ldap)
- **Windows Active Directory**
- **OpenLDAP**
- **Azure AD Connect**
- *(Requires Visual C++ build tools on Windows)*

## 🚀 Quick Setup

### 1. Install Dependencies (Already Done)
```bash
pip install django-allauth djangosaml2 django-oauth-toolkit
# Note: django-auth-ldap requires Visual C++ build tools on Windows
```

### 2. Update Environment Variables
Create/update your `.env` file:
```bash
# Social Authentication Keys
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret

MICROSOFT_CLIENT_ID=your_microsoft_client_id
MICROSOFT_CLIENT_SECRET=your_microsoft_client_secret

LINKEDIN_CLIENT_ID=your_linkedin_client_id
LINKEDIN_CLIENT_SECRET=your_linkedin_client_secret

# SAML Configuration
SAML_ENTITY_ID=http://your-domain.com/saml2/metadata/
SAML_IDP_METADATA_PATH=/path/to/idp-metadata.xml
SAML_KEY_FILE=/path/to/private.key
SAML_CERT_FILE=/path/to/certificate.crt

# LDAP Configuration (when enabled)
LDAP_SERVER_URI=ldap://your-domain-controller:389
LDAP_BIND_DN=CN=django-agent,CN=Users,DC=company,DC=com
LDAP_BIND_PASSWORD=secure_password
LDAP_USER_SEARCH_BASE=CN=Users,DC=company,DC=com
LDAP_GROUP_SEARCH_BASE=CN=Groups,DC=company,DC=com
LDAP_ACTIVE_GROUP=CN=Active Users,CN=Groups,DC=company,DC=com
LDAP_STAFF_GROUP=CN=Staff,CN=Groups,DC=company,DC=com
LDAP_ADMIN_GROUP=CN=Admins,CN=Groups,DC=company,DC=com
```

### 3. Apply Database Migrations
```bash
python manage.py migrate
```

### 4. Access SSO Options
- **Login Page**: http://localhost:8000/auth/login/
- **Social Login URLs**: 
  - Google: http://localhost:8000/accounts/google/login/
  - GitHub: http://localhost:8000/accounts/github/login/
  - Microsoft: http://localhost:8000/accounts/microsoft/login/
  - LinkedIn: http://localhost:8000/accounts/linkedin_oauth2/login/
- **SAML Metadata**: http://localhost:8000/saml2/metadata/
- **OAuth2 Applications**: http://localhost:8000/oauth/applications/

## 🔧 Provider-Specific Setup

### Google OAuth 2.0

1. **Google Cloud Console**:
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create new project or select existing
   - Enable Google+ API
   - Create OAuth 2.0 credentials

2. **Configure Redirect URIs**:
   ```
   http://localhost:8000/accounts/google/login/callback/
   https://yourdomain.com/accounts/google/login/callback/
   ```

3. **Update .env**:
   ```bash
   GOOGLE_CLIENT_ID=your_client_id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your_client_secret
   ```

### GitHub OAuth 2.0

1. **GitHub Settings**:
   - Go to Settings → Developer settings → OAuth Apps
   - Create new OAuth App

2. **Configure**:
   - Application name: `Workflow System`
   - Homepage URL: `http://localhost:8000`
   - Authorization callback URL: `http://localhost:8000/accounts/github/login/callback/`

3. **Update .env**:
   ```bash
   GITHUB_CLIENT_ID=your_client_id
   GITHUB_CLIENT_SECRET=your_client_secret
   ```

### Microsoft OAuth 2.0/OpenID Connect

1. **Azure Portal**:
   - Go to [Azure Portal](https://portal.azure.com/)
   - Azure Active Directory → App registrations
   - New registration

2. **Configure**:
   - Name: `Workflow System`
   - Redirect URI: `http://localhost:8000/accounts/microsoft/login/callback/`
   - API permissions: `User.Read`, `profile`, `email`

3. **Update .env**:
   ```bash
   MICROSOFT_CLIENT_ID=your_application_id
   MICROSOFT_CLIENT_SECRET=your_client_secret
   ```

### LinkedIn OAuth 2.0

1. **LinkedIn Developer Portal**:
   - Go to [LinkedIn Developers](https://www.linkedin.com/developers/)
   - Create new app

2. **Configure**:
   - App name: `Workflow System`
   - Redirect URLs: `http://localhost:8000/accounts/linkedin_oauth2/login/callback/`
   - Products: Sign In with LinkedIn

3. **Update .env**:
   ```bash
   LINKEDIN_CLIENT_ID=your_client_id
   LINKEDIN_CLIENT_SECRET=your_client_secret
   ```

## 🏢 Enterprise SAML SSO

### SAML Identity Provider Setup

1. **Generate Certificates**:
   ```bash
   # Generate private key
   openssl genrsa -out private.key 2048
   
   # Generate certificate
   openssl req -new -x509 -key private.key -out certificate.crt -days 365
   ```

2. **Configure Identity Provider**:
   - **Entity ID**: `http://yourdomain.com/saml2/metadata/`
   - **ACS URL**: `http://yourdomain.com/saml2/acs/`
   - **SLS URL**: `http://yourdomain.com/saml2/ls/`
   - **Name ID Format**: Email Address

3. **Download IDP Metadata**:
   - Save IDP metadata XML file
   - Update `SAML_IDP_METADATA_PATH` in `.env`

### Common SAML Providers

#### Azure AD SAML
1. Azure Portal → Enterprise applications → New application
2. Create non-gallery application
3. Configure SAML settings with URLs above
4. Download Federation Metadata XML

#### Okta SAML
1. Okta Admin → Applications → Create App Integration
2. Choose SAML 2.0
3. Configure with URLs above
4. Download metadata

#### ADFS SAML
1. ADFS Management → Relying Party Trusts
2. Add new relying party trust
3. Configure endpoints and identifiers
4. Export metadata

## 🔐 OAuth2 Provider Setup

### Create OAuth2 Application

1. **Django Admin**:
   - Go to http://localhost:8000/admin/
   - OAuth2 Provider → Applications → Add

2. **Configure**:
   - **Name**: `External API Client`
   - **Client type**: `Confidential`
   - **Authorization grant type**: `Authorization code`
   - **Redirect uris**: `https://yourclient.com/callback/`

3. **Use Tokens**:
   ```bash
   # Authorization URL
   http://localhost:8000/oauth/authorize/?response_type=code&client_id=CLIENT_ID&redirect_uri=REDIRECT_URI
   
   # Token endpoint
   POST http://localhost:8000/oauth/token/
   ```

## 🔧 LDAP/Active Directory (Windows)

### Install Requirements (Windows)

1. **Install Visual C++ Build Tools**:
   - Download from [Microsoft](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   - Install C++ build tools

2. **Install python-ldap**:
   ```bash
   pip install django-auth-ldap
   ```

3. **Enable LDAP in settings.py**:
   - Uncomment LDAP configuration section
   - Add `'django_auth_ldap.backend.LDAPBackend'` to `AUTHENTICATION_BACKENDS`

### LDAP Configuration

1. **Test LDAP Connection**:
   ```python
   import ldap
   
   conn = ldap.initialize('ldap://your-dc.company.com:389')
   conn.simple_bind_s('CN=user,CN=Users,DC=company,DC=com', 'password')
   ```

2. **Configure Groups**:
   - Map AD groups to Django permissions
   - Set staff/superuser flags based on group membership

## 🧪 Testing SSO

### Test Social Authentication
1. Configure at least one social provider (Google recommended)
2. Visit login page
3. Click social login button
4. Complete OAuth flow
5. Verify user creation and login

### Test SAML SSO
1. Configure SAML identity provider
2. Access: `http://localhost:8000/saml2/login/`
3. Complete SAML authentication
4. Verify user attributes mapping

### Test OAuth2 API
```bash
# Get authorization code
curl -X GET "http://localhost:8000/oauth/authorize/?response_type=code&client_id=CLIENT_ID&redirect_uri=REDIRECT_URI"

# Exchange for token
curl -X POST "http://localhost:8000/oauth/token/" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=authorization_code&code=CODE&client_id=CLIENT_ID&client_secret=CLIENT_SECRET"

# Use token for API access
curl -X GET "http://localhost:8000/api/tasks/" \
  -H "Authorization: Bearer ACCESS_TOKEN"
```

## 🛡️ Security Considerations

### Production Security
1. **HTTPS Required**: All SSO must use HTTPS in production
2. **Secure Certificates**: Use proper SSL/TLS certificates
3. **Key Rotation**: Regularly rotate OAuth secrets and SAML certificates
4. **Audit Logging**: Monitor authentication events
5. **Rate Limiting**: Implement login rate limiting

### User Management
1. **Auto-provisioning**: Users created automatically on first SSO login
2. **Attribute Mapping**: Map SSO attributes to Django user fields
3. **Group Synchronization**: Sync groups from SSO provider
4. **Account Linking**: Link SSO accounts to existing users

## 📊 SSO Analytics

### Monitor Authentication
- Track login methods used
- Monitor SSO success/failure rates
- Audit user access patterns
- Generate SSO usage reports

### User Experience
- Seamless authentication flow
- Automatic account creation
- Profile synchronization
- Unified logout (SLO)

## 🚀 Production Deployment

### Environment Variables
Set all SSO configuration in production environment:
```bash
# Production URLs
SAML_ENTITY_ID=https://yourdomain.com/saml2/metadata/
GOOGLE_CLIENT_ID=production_client_id
# ... other production keys
```

### SSL/TLS Configuration
```nginx
# Nginx configuration for SSO endpoints
location /accounts/ {
    proxy_pass http://127.0.0.1:8000;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}

location /oauth/ {
    proxy_pass http://127.0.0.1:8000;
    # ... same headers
}

location /saml2/ {
    proxy_pass http://127.0.0.1:8000;
    # ... same headers
}
```

## 📞 Support

### Common Issues
1. **Redirect URI Mismatch**: Check OAuth provider configuration
2. **SAML Certificate Errors**: Verify certificate validity and paths
3. **LDAP Connection Failed**: Check network connectivity and credentials
4. **User Not Created**: Verify auto-signup settings

### Enterprise Support
- SSO provider documentation
- Identity provider support teams
- Django-allauth documentation
- SAML troubleshooting guides

**Your Django Workflow System now supports enterprise-wide SSO! 🎉**
