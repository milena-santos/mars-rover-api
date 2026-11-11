#!/bin/sh
set -eu

cd /app/src

python <<'PY'
import os
import time

import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.db import connection

attempts = 0
while attempts < 30:
    try:
        connection.ensure_connection()
    except Exception:
        attempts += 1
        time.sleep(1)
        continue
    break
else:
    raise SystemExit("Database was not ready in time.")
PY

python manage.py migrate --noinput
python manage.py collectstatic --noinput

exec "$@"
