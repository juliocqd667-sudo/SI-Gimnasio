#!/usr/bin/env bash
# exit on error
set -o errexit

# 1. Construir el Frontend
echo ">>> BUILDING FRONTEND"
cd frontend
npm install
npm run build
cd ..

# 2. Preparar el Backend
echo ">>> PREPARING BACKEND"
cd backend
pip install -r requirements.txt

echo ">>> DJANGO TASKS"
python manage.py collectstatic --no-input

echo ">>> Running migrations..."
# Primero aplicamos las migraciones de contenttypes y auth explícitamente
python manage.py migrate contenttypes --no-input
python manage.py migrate auth --no-input
# Luego el resto
python manage.py migrate --no-input

echo ">>> LOADING ALL DATA FROM SQLITE DUMP"
python manage.py loaddata data_dump.json 2>/dev/null || echo "Data dump loading failed or already loaded, continuing..."

echo ">>> FORCING PASSWORDS & ROLES"
python manage.py shell -c "from core.models import CustomUser; u = CustomUser.objects.filter(username='admin').first(); (u.set_password('admin123'), u.is_superuser=True, u.is_staff=True, u.is_administrativo=True, u.save(), print('Admin access restored')) if u else print('Admin not found')"
python manage.py shell -c "from core.models import CustomUser; u = CustomUser.objects.filter(username='messi').first(); (u.set_password('admin123'), u.is_superuser=True, u.is_staff=True, u.is_administrativo=True, u.save(), print('Messi access restored')) if u else print('Messi not found')"

echo ">>> DEPLOYMENT FINISHED"
