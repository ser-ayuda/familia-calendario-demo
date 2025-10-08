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

# Copy entrypoint and make executable
COPY docker-entrypoint.sh /usr/local/bin/docker-entrypoint.sh
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# Note: we run migrations and seed at container start (entrypoint) so we
# operate against the runtime DATABASE_URL (useful for Render and other
# hosted DB providers). The build step keeps a best-effort attempt but the
# real work happens in the entrypoint.

EXPOSE 8000
ENTRYPOINT ["/usr/local/bin/docker-entrypoint.sh"]
CMD ["gunicorn", "hogar.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
