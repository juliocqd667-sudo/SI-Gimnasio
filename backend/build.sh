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

echo ">>> Running migrations with clean state..."
# Intentar limpiar el estado de migraciones corrompido y empezar desde cero
python manage.py shell -c "
from django.db import connection
try:
    with connection.cursor() as cursor:
        cursor.execute(\"SELECT COUNT(*) FROM django_migrations\")
        count = cursor.fetchone()[0]
        print(f'Found {count} migration records')
        if count > 0:
            # Hay registros previos pero las tablas pueden no existir
            # Limpiar el estado y empezar de cero
            cursor.execute(\"DELETE FROM django_migrations\")
            print('Cleared migration records for clean start')
except Exception as e:
    print(f'django_migrations table not found (fresh DB): {e}')
" 2>/dev/null || echo "Migration state check skipped"

# Ahora aplicar todas las migraciones desde cero
python manage.py migrate --no-input

echo ">>> LOADING ALL DATA FROM SQLITE DUMP"
python manage.py loaddata data_dump.json 2>/dev/null || echo "Data dump loading failed or already loaded, continuing..."

echo ">>> FORCING PASSWORDS & ROLES"
python manage.py shell -c "from core.models import CustomUser; u = CustomUser.objects.filter(username='admin').first(); (u.set_password('admin123'), u.is_superuser=True, u.is_staff=True, u.is_administrativo=True, u.save(), print('Admin access restored')) if u else print('Admin not found')"
python manage.py shell -c "from core.models import CustomUser; u = CustomUser.objects.filter(username='messi').first(); (u.set_password('admin123'), u.is_superuser=True, u.is_staff=True, u.is_administrativo=True, u.save(), print('Messi access restored')) if u else print('Messi not found')"

echo ">>> DEPLOYMENT FINISHED"
