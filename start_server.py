#!/usr/bin/env python
import os
import sys
import subprocess
import django

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'banque_api.settings')
django.setup()

# Run migrations
print("Running migrations...")
from django.core.management import call_command
try:
    call_command('migrate', verbosity=2, interactive=False)
    print("✅ Migrations completed successfully!")
except Exception as e:
    print(f"❌ Migration error: {e}")
    sys.exit(1)

# Collect static files
print("Collecting static files...")
try:
    call_command('collectstatic', verbosity=0, interactive=False)
    print("✅ Static files collected!")
except Exception as e:
    print(f"⚠️ Static files warning: {e}")

# Get port from environment or default to 8000
port = os.environ.get('PORT', '8000')

# Launch Gunicorn
print(f"Starting Gunicorn on port {port}...")
os.execvp('gunicorn', ['gunicorn', 'banque_api.wsgi:application', f'--bind=0.0.0.0:{port}'])
