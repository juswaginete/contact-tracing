# Configurable Settings
DB_NAME = ''
DB_USER = ''
DB_PASSWORD = ''
DB_HOST = 'localhost'

# Config Start
SECRET_KEY = 't_gt#)i7$-z=tg3s4v_8^jidhpfdzk#bp^l5!#qwztjpg37-x8'

DEBUG = True

DATABASES = {
    # Ends with "postgresql", "mysql", "sqlite3" or "oracle".
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': '5432',
    },
}

# INSTALLED_APPS += ['django_extensions']

# if DEBUG_TOOLBAR:
#     INSTALLED_APPS = [
#         'debug_toolbar',
#     ] + INSTALLED_APPS

#     MIDDLEWARE = [
#         'debug_toolbar.middleware.DebugToolbarMiddleware',
#     ] + MIDDLEWARE


# EMAIL BACKEND
# https://docs.djangoproject.com/en/2.1/topics/email/#smtp-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = True


# Django Session Security
# https://django-session-security.readthedocs.io/en/latest/full.html
SESSION_SECURITY_WARN_AFTER = 540
SESSION_EXPIRE_AFTER = 600
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
