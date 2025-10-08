#!/usr/bin/env bash
set -e

echo "== Docker entrypoint: starting up (migrate + seed + collectstatic) =="

# Try to run migrate several times to wait for DB readiness
MAX_RETRIES=${MAX_RETRIES:-10}
SLEEP_SECONDS=${SLEEP_SECONDS:-3}
COUNT=0
while [ $COUNT -lt $MAX_RETRIES ]; do
  echo "Attempt $((COUNT+1))/$MAX_RETRIES: running migrate..."
  if python manage.py migrate --noinput; then
    echo "Migrate succeeded"
    break
  fi
  COUNT=$((COUNT+1))
  echo "Migrate failed or DB not ready yet — sleeping $SLEEP_SECONDS seconds"
  sleep $SLEEP_SECONDS
done

echo "Running demo seed (create_demo.py) — best effort"
python scripts/create_demo.py || echo "create_demo.py failed (continuing)"

echo "Collecting static files"
python manage.py collectstatic --noinput || echo "collectstatic failed (continuing)"

echo "Entrypoint finished — execing CMD"
exec "$@"
