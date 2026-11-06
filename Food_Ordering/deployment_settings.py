import os
import dj_database_url
from .settings import *

DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")
SECRET_KEY = os.environ.get("SECRET_KEY", SECRET_KEY)

RENDER_HOST = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_HOST:
    if RENDER_HOST not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(RENDER_HOST)
    CSRF_TRUSTED_ORIGINS = [f"https://{RENDER_HOST}"]

if os.environ.get("DATABASE_URL"):
    DATABASES["default"] = dj_database_url.config(conn_max_age=600)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
