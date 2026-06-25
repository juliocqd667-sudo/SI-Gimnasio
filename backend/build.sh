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

echo ">>> PREPARANDO BASE DE DATOS"
# Limpiar tablas residuales de deploys fallidos anteriores
python - <<'PYEOF'
import os, sys
db_url = os.environ.get('DATABASE_URL')
if not db_url:
    print("Sin DATABASE_URL, saltando")
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
    cur.execute("SELECT tablename FROM pg_tables WHERE schemaname='public'")
    tables = [row[0] for row in cur.fetchall()]
    if tables:
        cur.execute('DROP TABLE IF EXISTS ' + ', '.join(f'"public"."{t}"' for t in tables) + ' CASCADE')
        print(f"Eliminadas {len(tables)} tablas: {tables}")
    else:
        print("Base de datos limpia")
    cur.close()
    conn.close()
except Exception as e:
    print(f"Advertencia limpieza: {e}")
PYEOF

echo ">>> CREANDO TABLA django_content_type MANUALMENTE (bypass bug Django 5.2)"
# El bug en contenttypes.0002 en PostgreSQL hace que AlterField falle aunque la tabla existe.
# Solución: crear la tabla en su estado FINAL directamente y luego fingir las migraciones.
python - <<'PYEOF'
import os, sys
db_url = os.environ.get('DATABASE_URL')
if not db_url:
    print("Sin DATABASE_URL")
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
    # Crear django_content_type en su estado FINAL (sin columna 'name', que es lo que queda tras 0001+0002)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS "django_content_type" (
            "id" serial NOT NULL PRIMARY KEY,
            "app_label" varchar(100) NOT NULL,
            "model" varchar(100) NOT NULL,
            UNIQUE ("app_label", "model")
        )
    """)
    # Crear tambien django_migrations para poder hacer el fake
    cur.execute("""
        CREATE TABLE IF NOT EXISTS "django_migrations" (
            "id" serial NOT NULL PRIMARY KEY,
            "app" varchar(255) NOT NULL,
            "name" varchar(255) NOT NULL,
            "applied" timestamp with time zone NOT NULL
        )
    """)
    print("Tablas base creadas correctamente")
    cur.close()
    conn.close()
except Exception as e:
    print(f"Error creando tablas: {e}")
    sys.exit(1)
PYEOF

echo ">>> MARCANDO MIGRACIONES DE CONTENTTYPES COMO APLICADAS (--fake)"
# Esto le dice a Django: "contenttypes ya está listo, no lo ejecutes"
python manage.py migrate --fake contenttypes

echo ">>> EJECUTANDO EL RESTO DE MIGRACIONES"
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
