# syntax=docker/dockerfile:1

# ---- AdTubers (Django) production image, tuned for Render ----
FROM python:3.13-slim

# Sensible Python runtime behaviour
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install dependencies first so this layer is cached across code changes.
# All wheels (Django, Pillow, psycopg[binary]) ship manylinux builds, so no
# compiler / system libs are required on top of the slim base.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the Django project. manage.py lives in ./tubers/, so its contents land
# at the image root (/app/manage.py, /app/tubers/settings.py, ...).
COPY tubers/ ./

# Bake static files into the image (served by WhiteNoise at runtime).
# Uses the built-in insecure default SECRET_KEY; no database is touched.
RUN python manage.py collectstatic --noinput

# Render injects $PORT at runtime; default to 8000 for local `docker run`.
ENV PORT=8000
EXPOSE 8000

# Apply migrations, optionally seed demo data, then serve with gunicorn.
# Shell form is intentional so ${PORT} / ${WEB_CONCURRENCY} expand at start.
# WEB_CONCURRENCY defaults to 2 (safe for Render's 512 MB free tier); raise it
# on a larger instance without touching this file.
# seed_demo is idempotent and only runs when SEED_DEMO=true; `|| true` keeps a
# seeding hiccup from blocking startup. Set SEED_DEMO=false once data exists.
CMD python manage.py migrate --noinput && \
    if [ "$SEED_DEMO" = "true" ]; then python manage.py seed_demo || true; fi && \
    exec gunicorn tubers.wsgi:application \
        --bind 0.0.0.0:${PORT} \
        --workers ${WEB_CONCURRENCY:-2} \
        --timeout 120
