# Django Workflow System - Deployment Guide

This guide covers deployment options for the Django Workflow System in various environments.

## Table of Contents
1. [Development Deployment](#development-deployment)
2. [Production Deployment](#production-deployment)
3. [Docker Deployment](#docker-deployment)
4. [Cloud Deployment](#cloud-deployment)
5. [Database Setup](#database-setup)
6. [Environment Configuration](#environment-configuration)
7. [Security Considerations](#security-considerations)
8. [Monitoring & Maintenance](#monitoring--maintenance)

## Development Deployment

### Local Development Setup

1. **Prerequisites:**
   ```bash
   # Install Python 3.8+
   python --version
   
   # Install PostgreSQL
   # Windows: Download from postgresql.org
   # macOS: brew install postgresql
   # Ubuntu: sudo apt-get install postgresql postgresql-contrib
   ```

2. **Project Setup:**
   ```bash
   cd sb_vws
   
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Database Configuration:**
   ```bash
   # Start PostgreSQL service
   # Windows: Start from Services or pgAdmin
   # macOS: brew services start postgresql
   # Ubuntu: sudo systemctl start postgresql
   
   # Create database
   createdb workflow_db
   ```

4. **Environment Setup:**
   ```bash
   cp .env.example .env
   # Edit .env file with your settings
   ```

5. **Initialize Application:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic
   ```

6. **Run Development Server:**
   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

## Production Deployment

### Ubuntu Server Deployment

1. **Server Setup:**
   ```bash
   # Update system
   sudo apt update && sudo apt upgrade -y
   
   # Install required packages
   sudo apt install python3 python3-pip python3-venv nginx postgresql postgresql-contrib supervisor git -y
   ```

2. **Database Setup:**
   ```bash
   # Switch to postgres user
   sudo -u postgres psql
   
   # Create database and user
   CREATE DATABASE workflow_db;
   CREATE USER workflow_user WITH ENCRYPTED PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE workflow_db TO workflow_user;
   ALTER USER workflow_user CREATEDB;
   \q
   ```

3. **Application Deployment:**
   ```bash
   # Create application directory
   sudo mkdir -p /var/www/workflow-system
   sudo chown $USER:$USER /var/www/workflow-system
   
   # Clone/copy application
   cp -r sb_vws/* /var/www/workflow-system/
   cd /var/www/workflow-system
   
   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   pip install gunicorn
   ```

4. **Production Settings:**
   ```bash
   # Create production environment file
   cat > .env << EOF
   DEBUG=False
   SECRET_KEY=your-super-secret-production-key-here
   ALLOWED_HOSTS=your-domain.com,www.your-domain.com
   DB_NAME=workflow_db
   DB_USER=workflow_user
   DB_PASSWORD=secure_password
   DB_HOST=localhost
   DB_PORT=5432
   EOF
   
   # Set proper permissions
   chmod 600 .env
   ```

5. **Initialize Database:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic --noinput
   ```

6. **Gunicorn Configuration:**
   ```bash
   # Create gunicorn configuration
   cat > gunicorn.conf.py << EOF
   bind = "127.0.0.1:8000"
   workers = 3
   worker_class = "sync"
   worker_connections = 1000
   max_requests = 1000
   max_requests_jitter = 100
   timeout = 30
   keepalive = 2
   preload_app = True
   user = "www-data"
   group = "www-data"
   EOF
   ```

7. **Supervisor Configuration:**
   ```bash
   # Create supervisor configuration
   sudo cat > /etc/supervisor/conf.d/workflow-system.conf << EOF
   [program:workflow-system]
   command=/var/www/workflow-system/venv/bin/gunicorn workflow_system.wsgi:application -c /var/www/workflow-system/gunicorn.conf.py
   directory=/var/www/workflow-system
   user=www-data
   autostart=true
   autorestart=true
   redirect_stderr=true
   stdout_logfile=/var/log/workflow-system.log
   environment=PATH="/var/www/workflow-system/venv/bin"
   EOF
   
   # Start supervisor
   sudo supervisorctl reread
   sudo supervisorctl update
   sudo supervisorctl start workflow-system
   ```

8. **Nginx Configuration:**
   ```bash
   # Create nginx configuration
   sudo cat > /etc/nginx/sites-available/workflow-system << EOF
   server {
       listen 80;
       server_name your-domain.com www.your-domain.com;
       
       client_max_body_size 50M;
       
       location /static/ {
           alias /var/www/workflow-system/staticfiles/;
           expires 1y;
           add_header Cache-Control "public, immutable";
       }
       
       location /media/ {
           alias /var/www/workflow-system/media/;
           expires 1y;
           add_header Cache-Control "public, immutable";
       }
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host \$host;
           proxy_set_header X-Real-IP \$remote_addr;
           proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto \$scheme;
       }
   }
   EOF
   
   # Enable site
   sudo ln -s /etc/nginx/sites-available/workflow-system /etc/nginx/sites-enabled/
   sudo nginx -t
   sudo systemctl restart nginx
   ```

## Docker Deployment

### Dockerfile
```dockerfile
# Create Dockerfile
cat > Dockerfile << EOF
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port
EXPOSE 8000

# Run application
CMD ["gunicorn", "workflow_system.wsgi:application", "--bind", "0.0.0.0:8000"]
EOF
```

### Docker Compose
```yaml
# Create docker-compose.yml
cat > docker-compose.yml << EOF
version: '3.8'

services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      POSTGRES_DB: workflow_db
      POSTGRES_USER: workflow_user
      POSTGRES_PASSWORD: secure_password
    ports:
      - "5432:5432"

  web:
    build: .
    command: gunicorn workflow_system.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/app
      - static_volume:/app/staticfiles
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DB_HOST=db
      - DB_NAME=workflow_db
      - DB_USER=workflow_user
      - DB_PASSWORD=secure_password
    depends_on:
      - db

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/app/staticfiles
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
EOF
```

### Deploy with Docker
```bash
# Build and run
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser
```

## Cloud Deployment

### AWS Elastic Beanstalk

1. **Requirements:**
   ```bash
   pip install awsebcli
   ```

2. **Configuration:**
   ```bash
   # Initialize EB application
   eb init workflow-system
   
   # Create environment
   eb create production
   
   # Deploy
   eb deploy
   ```

### Heroku Deployment

1. **Heroku Setup:**
   ```bash
   # Install Heroku CLI
   # Create Procfile
   echo "web: gunicorn workflow_system.wsgi" > Procfile
   
   # Create runtime.txt
   echo "python-3.11.0" > runtime.txt
   
   # Update requirements.txt
   echo "gunicorn" >> requirements.txt
   ```

2. **Deploy:**
   ```bash
   heroku create workflow-system-app
   heroku addons:create heroku-postgresql:hobby-dev
   heroku config:set DEBUG=False
   heroku config:set SECRET_KEY=your-secret-key
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

## Database Setup

### PostgreSQL Production Configuration

1. **Optimization Settings:**
   ```sql
   -- Add to postgresql.conf
   shared_buffers = 256MB
   effective_cache_size = 1GB
   maintenance_work_mem = 64MB
   checkpoint_completion_target = 0.9
   wal_buffers = 16MB
   default_statistics_target = 100
   random_page_cost = 1.1
   effective_io_concurrency = 200
   ```

2. **Backup Strategy:**
   ```bash
   # Create backup script
   cat > backup_db.sh << EOF
   #!/bin/bash
   pg_dump -h localhost -U workflow_user workflow_db > backup_$(date +%Y%m%d_%H%M%S).sql
   EOF
   
   # Schedule with cron
   crontab -e
   # Add: 0 2 * * * /path/to/backup_db.sh
   ```

## Environment Configuration

### Production Environment Variables

```bash
# Security
DEBUG=False
SECRET_KEY=your-super-secret-production-key-here
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database
DB_NAME=workflow_db
DB_USER=workflow_user
DB_PASSWORD=secure_password
DB_HOST=localhost
DB_PORT=5432

# Email (optional)
EMAIL_HOST=smtp.your-provider.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@domain.com
EMAIL_HOST_PASSWORD=your-email-password

# Static/Media files
STATIC_ROOT=/var/www/workflow-system/staticfiles
MEDIA_ROOT=/var/www/workflow-system/media
```

## Security Considerations

### 1. SSL/HTTPS Configuration
```bash
# Install Certbot for Let's Encrypt
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 2. Firewall Configuration
```bash
# Configure UFW
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

### 3. Security Headers
```nginx
# Add to nginx configuration
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Referrer-Policy "no-referrer-when-downgrade" always;
add_header Content-Security-Policy "default-src 'self' http: https: data: blob: 'unsafe-inline'" always;
```

### 4. Database Security
```sql
-- Limit connections
ALTER SYSTEM SET max_connections = 100;

-- Enable logging
ALTER SYSTEM SET log_statement = 'all';
ALTER SYSTEM SET log_destination = 'csvlog';
```

## Monitoring & Maintenance

### 1. Log Monitoring
```bash
# Check application logs
sudo tail -f /var/log/workflow-system.log

# Check nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Check PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-*.log
```

### 2. Health Checks
```bash
# Create health check script
cat > health_check.sh << EOF
#!/bin/bash
curl -f http://localhost:8000/ || exit 1
echo "Application is healthy"
EOF
```

### 3. Performance Monitoring
```bash
# Install monitoring tools
pip install django-debug-toolbar  # Development only
pip install sentry-sdk[django]    # Error tracking
```

### 4. Regular Maintenance
```bash
# Create maintenance script
cat > maintenance.sh << EOF
#!/bin/bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Clean old logs
find /var/log -name "*.log" -mtime +30 -delete

# Vacuum database
sudo -u postgres vacuumdb -a -z

# Restart services
sudo supervisorctl restart workflow-system
sudo systemctl restart nginx
EOF
```

## Troubleshooting

### Common Issues

1. **Static files not loading:**
   ```bash
   python manage.py collectstatic --noinput
   sudo chown -R www-data:www-data /var/www/workflow-system/staticfiles
   ```

2. **Database connection errors:**
   ```bash
   # Check PostgreSQL status
   sudo systemctl status postgresql
   
   # Test database connection
   psql -h localhost -U workflow_user -d workflow_db
   ```

3. **Permission errors:**
   ```bash
   sudo chown -R www-data:www-data /var/www/workflow-system
   sudo chmod -R 755 /var/www/workflow-system
   ```

4. **Gunicorn not starting:**
   ```bash
   # Check supervisor logs
   sudo supervisorctl tail workflow-system
   
   # Restart manually
   sudo supervisorctl restart workflow-system
   ```

For additional support, refer to the Django documentation and your hosting provider's guides.
