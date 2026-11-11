"""Django settings controlled exclusively by environment variables."""

from pathlib import Path

import environ

BASE_DIR = Path(__file__).resolve().parent.parent
REPO_DIR = BASE_DIR.parent

env = environ.Env()
environ.Env.read_env(REPO_DIR / ".env")

SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")
DATABASES = {"default": env.db("DATABASE_URL")}

SECURE_SSL_REDIRECT = env.bool("SECURE_SSL_REDIRECT")
SESSION_COOKIE_SECURE = env.bool("SESSION_COOKIE_SECURE")
CSRF_COOKIE_SECURE = env.bool("CSRF_COOKIE_SECURE")

if env.bool("USE_SECURE_PROXY_SSL_HEADER"):
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "drf_spectacular",
    "probes.apps.ProbesConfig",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "EXCEPTION_HANDLER": "probes.api.exception_handler.domain_exception_handler",
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Mars Rover API",
    "DESCRIPTION": (
        "REST API for launching and controlling robotic probes "
        "on a rectangular Martian plateau."
    ),
    "VERSION": "0.1.0",
    "SERVE_INCLUDE_SCHEMA": False,
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

STATIC_ROOT = REPO_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
