import os
import socket
import warnings
from typing import Any

import dj_database_url

from . import settings as base_settings
from .settings import *  # noqa: F401,F403

DEBUG = os.environ.get("DEBUG", "False").lower() in ("true", "1", "yes")
SECRET_KEY = os.environ.get("SECRET_KEY", base_settings.SECRET_KEY)

ALLOWED_HOSTS: list[str] = list(base_settings.ALLOWED_HOSTS)
RENDER_HOST = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_HOST:
    if RENDER_HOST not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(RENDER_HOST)
    CSRF_TRUSTED_ORIGINS = [f"https://{RENDER_HOST}"]

DATABASES: dict[str, Any] = dict(base_settings.DATABASES)
database_url = os.environ.get("DATABASE_URL", "").strip().strip("'\"")
if database_url:
    parsed_db: dict[str, Any] = dict(
        dj_database_url.parse(
            database_url,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=".render.com" in database_url,
        )
    )
    db_host = str(parsed_db.get("HOST") or "")
    raw_port = parsed_db.get("PORT")
    db_port = int(raw_port) if raw_port else 5432
    if db_host and not db_host.startswith("/"):
        try:
            socket.getaddrinfo(db_host, db_port)
            DATABASES["default"] = parsed_db
        except socket.gaierror:
            warnings.warn(
                f"Could not resolve DATABASE_URL host '{db_host}' "
                "(the Render PostgreSQL instance may have expired or is in a different region). "
                "Falling back to SQLite so the build can proceed. "
                "Update or remove DATABASE_URL in Render Environment settings for persistent storage.",
                RuntimeWarning,
            )
    else:
        DATABASES["default"] = parsed_db

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
