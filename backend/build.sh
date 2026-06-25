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

echo ">>> RUNNING MIGRATIONS"
python manage.py migrate --no-input

echo ">>> SEEDING LEGACY DATA"
python manage.py migrate_legacy_data

echo ">>> SETTING UP ROLES"
python manage.py setup_roles

echo ">>> FORCING PASSWORDS & ROLES"
python manage.py shell -c "from core.models import CustomUser
for uname in ['admin', 'messi']:
    u = CustomUser.objects.filter(username=uname).first()
    if u:
        u.set_password('admin123')
        u.is_superuser = True
        u.is_staff = True
        u.is_administrativo = True
        u.save()
        print(uname + ': restaurado')
    else:
        print(uname + ': no encontrado')
"

echo ">>> CREATING DEMO USERS FOR FRONTEND"
python manage.py shell -c "from core.models import CustomUser; u, _ = CustomUser.objects.get_or_create(username='superadmin', defaults={'is_superuser':True,'is_staff':True}); u.set_password('admin123'); u.save(); print('superadmin created')"
python manage.py shell -c "from core.models import CustomUser, Administrativo; u, _ = CustomUser.objects.get_or_create(username='admin', defaults={'is_administrativo':True}); u.set_password('admin123'); u.save(); Administrativo.objects.get_or_create(user=u, defaults={'cargo':'Admin','turno':'Mañana'}); print('admin created')"
python manage.py shell -c "from core.models import CustomUser, Cliente; u, _ = CustomUser.objects.get_or_create(username='cliente1', defaults={'is_cliente':True}); u.set_password('cliente123'); u.save(); Cliente.objects.get_or_create(user=u); print('cliente1 created')"
python manage.py shell -c "from core.models import CustomUser, Instructor; u, _ = CustomUser.objects.get_or_create(username='instructor1', defaults={'is_instructor':True}); u.set_password('instr123'); u.save(); Instructor.objects.get_or_create(user=u, defaults={'especialidad':'General'}); print('instructor1 created')"
python manage.py shell -c "from core.models import CustomUser, Nutricionista; u, _ = CustomUser.objects.get_or_create(username='nutri1', defaults={'is_nutricionista':True}); u.set_password('nutri123'); u.save(); Nutricionista.objects.get_or_create(user=u, defaults={'horario_atencion':'Lunes a Viernes'}); print('nutri1 created')"

echo ">>> DEPLOYMENT FINISHED"
