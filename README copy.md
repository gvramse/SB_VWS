# SB Volunteer Workflow System

A comprehensive task management system built with Django, featuring user authentication, CRUD operations, email notifications, and enterprise SSO integration for Samskrita Bharati USA volunteers.

## Features

### ✅ Authentication & Authorization
- Django's built-in login/logout system with custom templates
- Social authentication with Google OAuth (django-allauth)
- Enterprise SSO ready (SAML, LDAP, OAuth2)
- Protected CRUD views (login required)
- User-specific task filtering
- Admin panel restricted to superusers only
- Session management with auto-logout capabilities

### 📝 Task Management
- **Create**: Add new tasks with assignee details, dates, priority, and status
- **Read**: View all user's tasks with search and filtering by status
- **Update**: Edit existing tasks with real-time AJAX status updates
- **Delete**: Remove tasks with confirmation prompts
- **Email Notifications**: Automatic emails for task creation, updates, and deletion

### 📊 Enhanced Task Fields
- Assignee Name, Email, and Location
- Start Date and Due Date
- Priority levels (High, Medium, Low)
- Status tracking (Pending, In Progress, Completed, Cancelled)
- Automatic timestamps for created/updated dates

### 🗄️ Database
- SQLite database for development (easily configurable for PostgreSQL)
- User-task relationships with foreign keys
- Sample data population via management command
- Robust data validation

### 🎨 User Interface
- Modern Bootstrap 5 responsive design with Samskrita Bharati USA branding
- Real-time status updates via AJAX with CSRF protection
- Quick status filter buttons (Pending, In Progress, Completed)
- Clickable dashboard cards for status filtering
- Search and filter functionality
- Mobile-friendly interface with clean navigation
- Home page with organizational information and external links

## Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory:**
   ```bash
   cd sb_vws
   ```

2. **Create and activate virtual environment:** [[memory:7192838]]
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```bash
   SECRET_KEY=your_secret_key_here
   DEBUG=True
   
   # Email configuration (for notifications)
   EMAIL_HOST_USER=sbvwsdmn@gmail.com
   EMAIL_HOST_PASSWORD=your_app_password
   
   # Google OAuth (if using social auth)
   GOOGLE_OAUTH2_CLIENT_ID=your_client_id
   GOOGLE_OAUTH2_CLIENT_SECRET=your_client_secret
   ```

5. **Run database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Populate sample data (optional):**
   ```bash
   python manage.py populate_sample_tasks
   ```

8. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

9. **Access the application:**
   - Main app: http://localhost:8000
   - Dashboard: http://localhost:8000/dashboard
   - Admin panel: http://localhost:8000/admin (superuser only)

## Project Structure

```
sb_vws/
├── manage.py                   # Django management script
├── requirements.txt           # Python dependencies
├── run.bat                   # Windows batch file to start server
├── .env                      # Environment variables (create from template)
├── README.md                 # This file
├── DEPLOYMENT.md             # Deployment guide
├── SSO_CONFIGURATION.md      # SSO setup guide
├── GOOGLE_OAUTH_SETUP.md     # Google OAuth setup guide
├── workflow_system/          # Django project settings
│   ├── settings.py           # Main configuration
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI configuration
├── tasks/                    # Main application
│   ├── models.py            # Task model with enhanced fields
│   ├── views.py             # View logic with AJAX endpoints
│   ├── forms.py             # Form definitions
│   ├── urls.py              # App URL patterns
│   ├── admin.py             # Admin configuration
│   ├── signals.py           # Email notification signals
│   └── management/
│       └── commands/
│           └── populate_sample_tasks.py  # Sample data command
├── templates/               # HTML templates
│   ├── base.html           # Base template with navigation
│   ├── home.html           # Landing page with org branding
│   ├── tasks/              # Task-related templates
│   ├── registration/       # Authentication templates
│   └── emails/             # Email notification templates
└── static/                 # Static files
    ├── css/               # Custom stylesheets
    └── js/                # JavaScript files with AJAX
```

## Usage

### For Volunteers

1. **Home Page**: Visit the landing page with Samskrita Bharati USA information
2. **Login**: Use your credentials or Google OAuth to sign in
3. **Dashboard**: View task statistics with clickable status cards
4. **Create Tasks**: Click "New Task" to add volunteer assignments
5. **Manage Tasks**: Use filter buttons (Pending, In Progress, Completed) for quick access
6. **Real-time Updates**: Click status buttons to update task progress instantly
7. **Navigation**: Use the clean navigation menu (Home, My Tasks, New Task)

### For Administrators

1. **Access Admin Panel**: Superusers see an "Admin" button in the header
2. **User Management**: Create and manage volunteer accounts
3. **Task Oversight**: View and manage all tasks across volunteers
4. **Email Monitoring**: Track task notification emails
5. **System Configuration**: Manage SSO settings and site configuration

## SSO Integration (Available)

The system includes enterprise SSO capabilities:

### Google OAuth (Configured)
- Ready-to-use Google authentication
- Seamless login/logout flow
- User profile integration

### SAML SSO (Enterprise Ready)
- `djangosaml2` package included
- Configuration templates available
- Enterprise-grade security

### OAuth2 Provider
- `django-oauth-toolkit` included
- Custom OAuth applications support

### LDAP/Active Directory (Available)
- Configuration ready for Windows environments
- User directory synchronization

## Key Features

### Email Notifications
- Automatic emails for task creation, updates, and deletion
- Gmail SMTP integration
- HTML email templates with task details

### AJAX Status Updates
- Real-time task status changes without page refresh
- CSRF-protected endpoints
- User feedback with success/error messages

### Smart Navigation
- Context-aware navigation (hides menu on home page)
- Auto-logout prevention during normal navigation
- Session management with timeout warnings

### Dashboard Analytics
- Task count by status with clickable cards
- Recent activity overview
- Quick access to filtered task lists

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Home page (redirects to dashboard if authenticated) |
| `/dashboard/` | GET | User dashboard with statistics |
| `/tasks/` | GET | Task list with optional status filtering |
| `/tasks/create/` | GET/POST | Create new task |
| `/tasks/<id>/` | GET | Task detail view |
| `/tasks/<id>/edit/` | GET/POST | Edit task |
| `/tasks/<id>/delete/` | GET/POST | Delete task |
| `/tasks/<id>/status/` | POST | AJAX status update |
| `/auth/login/` | GET/POST | Login page |
| `/auth/signup/` | GET/POST | User registration |
| `/auth/logout/` | POST | Logout |
| `/admin/` | GET | Admin panel (superuser only) |
| `/accounts/google/login/` | GET | Google OAuth login |

## Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SECRET_KEY` | Django secret key | `your-secret-key-here` |
| `DEBUG` | Debug mode | `True` or `False` |
| `EMAIL_HOST_USER` | Gmail username | `sbvwsdmn@gmail.com` |
| `EMAIL_HOST_PASSWORD` | Gmail app password | `your-app-password` |
| `GOOGLE_OAUTH2_CLIENT_ID` | Google OAuth client ID | `your-client-id.googleusercontent.com` |
| `GOOGLE_OAUTH2_CLIENT_SECRET` | Google OAuth secret | `your-client-secret` |

## Security Features

- CSRF protection on all forms and AJAX requests
- User authentication required for all task operations
- Admin panel restricted to superusers
- Secure password validation
- Session-based authentication with auto-logout
- SQL injection protection via Django ORM
- Email notification security with app passwords

## Development Notes

- Uses Django 5.2.5 with modern Python practices
- SQLite for development, PostgreSQL-ready for production
- Bootstrap 5 for responsive UI
- jQuery for AJAX functionality
- FontAwesome icons for professional appearance
- Comprehensive error handling and user feedback

## Support & Documentation

- **SSO Setup**: See `SSO_CONFIGURATION.md` for enterprise integration
- **Google OAuth**: See `GOOGLE_OAUTH_SETUP.md` for social auth setup
- **Deployment**: See `DEPLOYMENT.md` for production deployment
- **Django Documentation**: https://docs.djangoproject.com/

## Contributing

This system is designed for Samskrita Bharati USA volunteer management. For feature requests or issues:

1. Test in the development environment
2. Document any configuration changes
3. Update this README if adding new features
4. Ensure all security features remain intact

## License

Built with Django framework, following Django's BSD license model.

---

**Samskrita Bharati USA** - Promoting Sanskrit language and Bharatiya culture across America.
- Main Website: https://samskritabharatiusa.org/
- SAFL: https://safl.org/
- Bookstore: https://www.sbusapustakapanah.org/