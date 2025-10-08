FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install minimal system dependencies (libpq for psycopg2 if needed)
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev gcc ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app

# Directories for static/media
RUN mkdir -p /vol/static /vol/media
ENV STATIC_ROOT=/vol/static
ENV MEDIA_ROOT=/vol/media

ENV DJANGO_SETTINGS_MODULE=hogar.settings

# Run migrations, create demo data and collect static (best-effort)
RUN python manage.py migrate --noinput || true
RUN python scripts/create_demo.py || true
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000
CMD ["gunicorn", "hogar.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
