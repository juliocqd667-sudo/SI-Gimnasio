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

echo ">>> LIMPIANDO TABLAS RESIDUALES"
python - <<'PYEOF'
import os, sys
db_url = os.environ.get('DATABASE_URL')
if not db_url:
    print("Sin DATABASE_URL, saltando limpieza")
    sys.exit(0)
try:
    import psycopg2
    from urllib.parse import urlparse
    r = urlparse(db_url)
    conn = psycopg2.connect(
        dbname=r.path[1:], user=r.username, password=r.password,
        host=r.hostname, port=r.port or 5432, sslmode='require'
    )
    conn.autocommit = True
    cur = conn.cursor()
    # Forzar search_path=public tambien aqui
    cur.execute("SET search_path TO public")
    cur.execute("SELECT tablename FROM pg_tables WHERE schemaname='public'")
    tables = [row[0] for row in cur.fetchall()]
    if tables:
        cur.execute('DROP TABLE IF EXISTS ' + ', '.join(f'"public"."{t}"' for t in tables) + ' CASCADE')
        print(f"Eliminadas {len(tables)} tablas de public: {tables}")
    else:
        print("Base de datos limpia en esquema public")
    cur.close()
    conn.close()
except Exception as e:
    print(f"Advertencia limpieza: {e}")
PYEOF

echo ">>> EJECUTANDO MIGRACIONES (con search_path=public via settings.py)"
python manage.py migrate --no-input

echo ">>> CARGANDO DATOS INICIALES"
python manage.py loaddata data_dump.json 2>/dev/null || echo "Carga de datos falló o ya estaba cargado, continuando..."

echo ">>> RESTAURANDO CONTRASEÑAS Y ROLES"
python manage.py shell -c "
from core.models import CustomUser
for uname in ['admin', 'messi']:
    u = CustomUser.objects.filter(username=uname).first()
    if u:
        u.set_password('admin123')
        u.is_superuser = True
        u.is_staff = True
        u.is_administrativo = True
        u.save()
        print(f'{uname}: restaurado')
    else:
        print(f'{uname}: no encontrado')
"

echo ">>> DESPLIEGUE FINALIZADO CON EXITO"
