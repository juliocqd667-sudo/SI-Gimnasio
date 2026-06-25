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

echo ">>> PREPARANDO POSTGRESQL (search_path + limpieza)"
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
        host=r.hostname, port=r.port or 5432, sslmode='require',
        # Forzar search_path=public desde el nivel de conexion
        options='-c search_path=public'
    )
    conn.autocommit = True
    cur = conn.cursor()
    
    # Verificar y reportar search_path actual
    cur.execute("SHOW search_path")
    print(f"search_path actual: {cur.fetchone()[0]}")
    
    # Verificar esquemas existentes
    cur.execute("SELECT nspname FROM pg_namespace WHERE nspname NOT LIKE 'pg_%' AND nspname != 'information_schema'")
    schemas = [row[0] for row in cur.fetchall()]
    print(f"Esquemas disponibles: {schemas}")
    
    # Buscar tablas en TODOS los esquemas (no solo public)
    cur.execute("""
        SELECT schemaname, tablename 
        FROM pg_tables 
        WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
    """)
    all_tables = cur.fetchall()
    print(f"Todas las tablas encontradas: {all_tables}")
    
    # Eliminar tablas en todos los esquemas de usuario
    for schema, table in all_tables:
        cur.execute(f'DROP TABLE IF EXISTS "{schema}"."{table}" CASCADE')
        print(f"Eliminada: {schema}.{table}")
    
    # Forzar search_path=public a nivel de ROL para futuras conexiones
    if r.username:
        try:
            cur.execute(f"ALTER ROLE \"{r.username}\" SET search_path TO public")
            print(f"search_path=public asignado permanentemente al rol: {r.username}")
        except Exception as e:
            print(f"No se pudo cambiar search_path del rol (puede no tener permiso): {e}")
    
    cur.close()
    conn.close()
    print("Preparación completada")
except Exception as e:
    print(f"Error en preparación: {e}")
    import traceback
    traceback.print_exc()
PYEOF

echo ">>> EJECUTANDO MIGRACIONES"
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

echo ">>> DESPLIEGUE FINALIZADO"
