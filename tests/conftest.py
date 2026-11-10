"""Test suite bootstrap."""

from __future__ import annotations

import os
from pathlib import Path

import environ

environ.Env.read_env(Path(__file__).resolve().parents[1] / ".env")

os.environ.setdefault("SECRET_KEY", "test-only-secret-key")
os.environ.setdefault("DEBUG", "False")
os.environ.setdefault("ALLOWED_HOSTS", "testserver")
os.environ.setdefault(
    "DATABASE_URL",
    "postgres://mars_rover:mars_rover@localhost:5432/mars_rover",
)
os.environ.setdefault("SECURE_SSL_REDIRECT", "False")
os.environ.setdefault("SESSION_COOKIE_SECURE", "False")
os.environ.setdefault("CSRF_COOKIE_SECURE", "False")
os.environ.setdefault("USE_SECURE_PROXY_SSL_HEADER", "False")
