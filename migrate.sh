#!/bin/bash

# Manual migration script
echo "Running Django migrations..."
docker-compose exec web python manage.py migrate

echo "Creating superuser (optional)..."
docker-compose exec web python manage.py createsuperuser --noinput --username admin --email admin@example.com || true

echo "Collecting static files..."
docker-compose exec web python manage.py collectstatic --noinput