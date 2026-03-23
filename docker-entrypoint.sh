#!/bin/bash
set -e

echo "========================================="
echo "STARTING SAACB DOCKER CONTAINER"
echo "========================================="

# SEMPRE usar DATABASE_URL configurado, sem verificações hardcoded
echo "📦 DATABASE_URL configurado: $DATABASE_URL"

# Migrations
python manage.py migrate --noinput

# Static files
python manage.py collectstatic --noinput --clear

# System check
python manage.py check

echo "========================================="
echo "✅ READY TO START GUNICORN"
echo "========================================="

exec "$@"
