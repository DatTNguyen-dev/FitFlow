# FitFlow Configuration Guide

## Environment Variables Template

Create a `.env` file in the project root with the following variables:

### Required
```env
# Gemini API
GOOGLE_API_KEY=your_google_gemini_api_key_here

# Django
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Database (SQLite by default)
# For PostgreSQL:
# DATABASE_URL=postgresql://username:password@localhost:5432/fitflow_db

# Cache (Redis)
REDIS_URL=redis://localhost:6379/0
```

### Optional
```env
# Email Configuration (for notifications)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password

# Celery
CELERY_BROKER_URL=redis://localhost:6379/1
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Gemini Settings (Optional - defaults provided)
GEMINI_MODEL=gemini-2.5-flash
GEMINI_TEMPERATURE=0.7
GEMINI_MAX_TOKENS=2048
```

## Step-by-Step Setup

### 1. Get Google Gemini API Key

1. Visit https://aistudio.google.com
2. Click "Get API Key"
3. Create a new API key
4. Copy and paste into `.env`

### 2. Database Setup

```bash
# For SQLite (default - development only)
python manage.py migrate

# For PostgreSQL (production)
pip install psycopg2-binary
# Update DATABASE_URL in .env
python manage.py migrate
```

### 3. Create Admin User

```bash
python manage.py createsuperuser
```

### 4. Install Redis (Optional - for task queue)

**Windows**:
```bash
# Using WSL or Docker
docker run -d -p 6379:6379 redis:latest
```

**macOS**:
```bash
brew install redis
redis-server
```

**Linux**:
```bash
sudo apt-get install redis-server
redis-server
```

### 5. Create Directory Structure

```bash
mkdir -p logs
mkdir -p static
mkdir -p media
```

## Django Settings Override

You can override settings by modifying `fitflow/settings.py`:

### Database

```python
# SQLite (Development)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# PostgreSQL (Production)
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://user:password@localhost:5432/fitflow'
    )
}
```

### Cache

```python
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

### Static Files

```python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

## Agent Configuration

### Customize Agent Parameters

In `fitflowapp/agents_config/agent_manager.py`:

```python
# Adjust LLM parameters
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=api_key,
    temperature=0.7,        # 0 = deterministic, 1 = creative
    max_tokens=2048,        # Max response length
    top_p=0.95,            # Nucleus sampling
)
```

### Agent Memory Settings

```python
# Increase/decrease conversation history
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True,
    k=5  # Keep last 5 messages
)
```

## REST Framework Configuration

### Add to settings.py

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}
```

## CORS Configuration

### For Local Development

```python
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",      # Vite
    "http://localhost:3000",      # React dev
    "http://127.0.0.1:5173",
]

CORS_ALLOW_ALL_ORIGINS = False
```

### For Production

```python
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]
```

## Logging Configuration

Add to `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'fitflow.log',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}
```

## Security Settings (Production)

```python
# settings.py
DEBUG = False
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'",),
}
```

## Dependencies Verification

```bash
# Check all packages are installed
pip check

# Show installed packages
pip list

# Freeze requirements
pip freeze > requirements_lock.txt
```

## Testing Configuration

Create `pytest.ini`:

```ini
[pytest]
DJANGO_SETTINGS_MODULE = fitflow.settings
python_files = tests.py test_*.py *_tests.py
python_classes = Test*
python_functions = test_*
```

Run tests:

```bash
pytest
# or
python manage.py test
```

## Performance Optimization

### Enable Query Optimization

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'CONN_MAX_AGE': 600,  # Persistent connections
    }
}
```

### Add Middleware Optimization

```python
MIDDLEWARE = [
    # ... existing middleware ...
    'django.middleware.gzip.GZipMiddleware',  # Compress responses
    'django.middleware.http.ConditionalGetMiddleware',  # Cache control
]
```

## Deployment Checklist

- [ ] Set `DEBUG = False`
- [ ] Change `SECRET_KEY` to secure random string
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up database backups
- [ ] Configure email backend
- [ ] Enable HTTPS (SSL/TLS)
- [ ] Set up monitoring/logging
- [ ] Configure CDN for static files
- [ ] Set up environment variables on server
- [ ] Test migrations on production database
- [ ] Configure CORS properly
- [ ] Set up API rate limiting
- [ ] Enable CSRF protection
- [ ] Configure security headers

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'google'`
**Solution**: 
```bash
pip install --upgrade google-generativeai
```

### Issue: PostgreSQL connection error
**Solution**:
```bash
# Check PostgreSQL is running
psql --version
# Verify credentials in DATABASE_URL
```

### Issue: Redis connection refused
**Solution**:
```bash
# Start Redis
redis-server
# or use Docker
docker run -d -p 6379:6379 redis
```

### Issue: API key invalid
**Solution**:
- Regenerate key at https://aistudio.google.com
- Check .env file has correct key
- Check GOOGLE_API_KEY is exported: `echo $GOOGLE_API_KEY`

## Resources

- Django Documentation: https://docs.djangoproject.com/en/6.0/
- Django REST Framework: https://www.django-rest-framework.org/
- LangChain Documentation: https://js.langchain.com/docs/get_started/introduction.html
- Google Gemini API: https://ai.google.dev/

---

Last Updated: February 5, 2026
