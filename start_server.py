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

# Check if migrations are needed (only warn, don't apply)
print("\n" + "="*60)
print("Checking migration status...")
print("="*60)
from django.core.management import call_command
from django.db import connection
try:
    from django.db.migrations.executor import MigrationExecutor
    executor = MigrationExecutor(connection)
    plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
    if plan:
        print(f"! Found {len(plan)} pending migrations (should have been applied at build time)")
    else:
        print("✓ All migrations are applied")
except Exception as e:
    print(f"! Could not check migrations: {e}")

# Collect static files (safe to do multiple times)
print("\n" + "="*60)
print("Ensuring static files are collected...")
print("="*60)
try:
    call_command('collectstatic', verbosity=0, interactive=False)
    print("✓ Static files ready")
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


