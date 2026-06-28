# import os
# import dj_database_url
# from pathlib import Path

# BASE_DIR = Path(__file__).resolve().parent.parent

# DEBUG = False
# SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

# ALLOWED_HOSTS = [os.environ.get("RENDER_EXTERNAL_HOSTNAME")]

# # CSRF and CORS
# CSRF_TRUSTED_ORIGINS = [f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}"]
# CORS_ALLOWED_ORIGINS = [
#     f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}",
# ]
# CORS_ALLOW_CREDENTIALS = True

# # Installed apps (same as settings.py)
# INSTALLED_APPS = [
#     'django.contrib.admin',
#     'django.contrib.auth',
#     'django.contrib.contenttypes',
#     'django.contrib.sessions',
#     'django.contrib.messages',
#     'django.contrib.staticfiles',
#     'Order',
#     'API',
#     'Restaurants',
#     'Dishes',
#     'rest_framework',
#     'corsheaders',
#     'rest_framework_simplejwt',
#     'phonenumber_field',
# ]

# # Middleware
# MIDDLEWARE = [
#     'corsheaders.middleware.CorsMiddleware',
#     'django.middleware.security.SecurityMiddleware',
#     'whitenoise.middleware.WhiteNoiseMiddleware',
#     'django.contrib.sessions.middleware.SessionMiddleware',
#     'django.middleware.common.CommonMiddleware',
#     'django.middleware.csrf.CsrfViewMiddleware',
#     'django.contrib.auth.middleware.AuthenticationMiddleware',
#     'django.contrib.messages.middleware.MessageMiddleware',
#     'django.middleware.clickjacking.XFrameOptionsMiddleware',
# ]

# # JWT
# REST_FRAMEWORK = {
#     "DEFAULT_AUTHENTICATION_CLASSES": (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ),
# }
# from datetime import timedelta
# SIMPLE_JWT = {
#     "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
#     "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
# }

# # Database (PostgreSQL on Render)
# DATABASES = {
#     "default": dj_database_url.config(
#         default=os.environ.get("DATABASE_URL"),
#         conn_max_age=600
#     )
# }

# # Static files
# STATIC_URL = '/static/'
# STATIC_ROOT = BASE_DIR / "staticfiles"

# # Media files
# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / "media"

# DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

import os
import dj_database_url
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DEBUG = True
SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")

RENDER_HOST = os.environ.get("RENDER_EXTERNAL_HOSTNAME", "localhost")
ALLOWED_HOSTS = [RENDER_HOST]

CORS_ALLOWED_ORIGINS = [
    f"https://{RENDER_HOST}",
    "https://food-ordering-frontend-a3em.onrender.com",  # ✅ Add this
    "https://food-ordering-frontend-qf0i.onrender.com",  # ✅ Add this
]

CSRF_TRUSTED_ORIGINS = [
    f"https://{RENDER_HOST}",
    "https://food-ordering-frontend-a3em.onrender.com",  # ✅ Add this
    "https://food-ordering-frontend-qf0i.onrender.com",  # ✅ Add this
]
CORS_ALLOW_CREDENTIALS = True

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Order',
    'API',
    'Restaurants',
    'Dishes',
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    'phonenumber_field',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ✅ These were completely missing
ROOT_URLCONF = 'Food_Ordering.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Food_Ordering.wsgi.application'
ASGI_APPLICATION = 'Food_Ordering.asgi.application'  # ✅ needed since you use gunicorn+uvicorn

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

from datetime import timedelta
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600
    )
}

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
