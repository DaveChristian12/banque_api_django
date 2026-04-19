#!/bin/bash
# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start Gunicorn
gunicorn banque_api.wsgi:application --bind 0.0.0.0:$PORT
