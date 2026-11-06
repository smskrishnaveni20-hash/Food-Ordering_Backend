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
if ".onrender.com" not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(".onrender.com")

CSRF_TRUSTED_ORIGINS: list[str] = ["https://*.onrender.com"]
RENDER_HOST = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
if RENDER_HOST:
    if RENDER_HOST not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(RENDER_HOST)
    render_origin = f"https://{RENDER_HOST}"
    if render_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(render_origin)

if not os.environ.get("CORS_ALLOWED_ORIGINS"):
    CORS_ALLOW_ALL_ORIGINS = True

DATABASES: dict[str, Any] = dict(base_settings.DATABASES)
database_url = os.environ.get("DATABASE_URL", "").strip().strip("'\"")
if database_url:
    if "://" not in database_url and "@" in database_url and "/" in database_url:
        database_url = f"postgresql://{database_url}"
    try:
        parsed_db: dict[str, Any] = dict(
            dj_database_url.parse(
                database_url,
                conn_max_age=600,
                conn_health_checks=True,
                ssl_require=".render.com" in database_url,
            )
        )
        engine = str(parsed_db.get("ENGINE") or "")
        db_name = str(parsed_db.get("NAME") or "")
        db_host = str(parsed_db.get("HOST") or "")
        raw_port = parsed_db.get("PORT")
        db_port = int(raw_port) if raw_port else 5432

        if "sqlite" not in engine and (not db_host or not db_name):
            raise ValueError("missing host or database name in DATABASE_URL")

        if db_host and not db_host.startswith("/"):
            socket.getaddrinfo(db_host, db_port)

        DATABASES["default"] = parsed_db
    except Exception as exc:
        warnings.warn(
            f"Skipping invalid or unreachable DATABASE_URL ({exc}). "
            "Falling back to SQLite so the build and server can run. "
            "For PostgreSQL, set DATABASE_URL to a full 'postgresql://user:password@host/dbname' URL.",
            RuntimeWarning,
        )

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}
