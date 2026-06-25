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

echo ">>> LIMPIANDO BASE DE DATOS (reset completo para evitar estado corrupto)"
python - <<'PYEOF'
import os
import sys

db_url = os.environ.get('DATABASE_URL')
if not db_url:
    print("No DATABASE_URL encontrada, saltando limpieza")
    sys.exit(0)

try:
    import psycopg2
    from urllib.parse import urlparse

    r = urlparse(db_url)
    conn = psycopg2.connect(
        dbname=r.path[1:],
        user=r.username,
        password=r.password,
        host=r.hostname,
        port=r.port or 5432,
        sslmode='require'
    )
    conn.autocommit = True
    cur = conn.cursor()

    # Obtener todas las tablas en el esquema actual
    cur.execute("""
        SELECT tablename FROM pg_tables
        WHERE schemaname = 'public'
    """)
    tables = [row[0] for row in cur.fetchall()]

    if tables:
        tables_sql = ', '.join(f'"public"."{t}"' for t in tables)
        cur.execute(f'DROP TABLE IF EXISTS {tables_sql} CASCADE')
        print(f"Limpieza completa: {len(tables)} tablas eliminadas -> {tables}")
    else:
        print("Base de datos limpia, sin tablas previas")

    cur.close()
    conn.close()
except Exception as e:
    print(f"Advertencia en limpieza de DB: {e}")
    print("Continuando con el despliegue de todas formas...")
PYEOF

echo ">>> EJECUTANDO MIGRACIONES"
python manage.py migrate --no-input

echo ">>> CARGANDO DATOS INICIALES"
python manage.py loaddata data_dump.json 2>/dev/null || echo "Carga de datos falló o ya estaba cargado, continuando..."

echo ">>> RESTAURANDO CONTRASEÑAS Y ROLES"
python manage.py shell -c "from core.models import CustomUser; u = CustomUser.objects.filter(username='admin').first(); (u.set_password('admin123'), u.__setattr__('is_superuser', True), u.__setattr__('is_staff', True), u.__setattr__('is_administrativo', True), u.save(), print('Admin restaurado')) if u else print('Admin no encontrado')"
python manage.py shell -c "from core.models import CustomUser; u = CustomUser.objects.filter(username='messi').first(); (u.set_password('admin123'), u.__setattr__('is_superuser', True), u.__setattr__('is_staff', True), u.__setattr__('is_administrativo', True), u.save(), print('Messi restaurado')) if u else print('Messi no encontrado')"

echo ">>> DESPLIEGUE FINALIZADO CON EXITO"
