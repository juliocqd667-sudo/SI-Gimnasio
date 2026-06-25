#!/usr/bin/env bash
# exit on error
set -o errexit

echo ">>> PREPARING BACKEND ONLY (SKIPPING FRONTEND BUILD)"
# We're already in backend/ directory due to rootDir setting
pip install -r requirements.txt

echo ">>> DJANGO TASKS"
python manage.py collectstatic --no-input
echo ">>> Running migrations..."
python manage.py migrate --no-input || echo "Migration failed, but continuing..."

echo ">>> LOADING ALL DATA FROM SQLITE DUMP"
python manage.py loaddata data_dump.json 2>/dev/null || echo "Data dump loading failed, but continuing..."

echo ">>> FORCING PASSWORDS & ROLES"
python manage.py shell -c "from core.models import CustomUser; u = CustomUser.objects.filter(username='admin').first(); (u.set_password('admin123'), u.is_superuser=True, u.is_staff=True, u.is_administrativo=True, u.save(), print('Admin access restored')) if u else print('Admin not found')"
python manage.py shell -c "from core.models import CustomUser; u = CustomUser.objects.filter(username='messi').first(); (u.set_password('admin123'), u.is_superuser=True, u.is_staff=True, u.is_administrativo=True, u.save(), print('Messi access restored')) if u else print('Messi not found')"

echo ">>> DEPLOYMENT FINISHED"
