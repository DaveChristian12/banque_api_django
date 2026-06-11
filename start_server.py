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
print("\n" + "="*60)
print("Running migrations...")
print("="*60)
from django.core.management import call_command
try:
    call_command('migrate', verbosity=2, interactive=False)
    print("✓ Migrations completed successfully!")
except Exception as e:
    print(f"✗ Migration error: {e}")
    sys.exit(1)

# Collect static files
print("\n" + "="*60)
print("Collecting static files...")
print("="*60)
try:
    call_command('collectstatic', verbosity=0, interactive=False)
    print("✓ Static files collected!")
except Exception as e:
    print(f"! Static files warning: {e}")

# Get port from environment or default to 8000
port = os.environ.get('PORT', '8000')

# Get workers from environment (Render sets WEB_CONCURRENCY)
workers = int(os.environ.get('WEB_CONCURRENCY', 1))

# Launch Gunicorn with proper error handling
print("\n" + "="*60)
print(f"Starting Gunicorn on port {port} with {workers} worker(s)...")
print("="*60 + "\n")

try:
    os.execvp('gunicorn', [
        'gunicorn',
        'banque_api.wsgi:application',
        f'--bind=0.0.0.0:{port}',
        f'--workers={workers}',
        '--worker-class=sync',
        '--threads=2',
        '--timeout=30',
        '--access-logfile=-',
        '--error-logfile=-'
    ])
except FileNotFoundError:
    print("ERROR: gunicorn not found. Make sure it's installed in requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"ERROR: Failed to start Gunicorn: {e}")
    sys.exit(1)

