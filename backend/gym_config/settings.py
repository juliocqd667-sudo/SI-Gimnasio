"""
Django settings for gym_config project.
Configurado para entornos Local y Produccion (Render.com).
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ─────────────────────────────────────────────────────────────────────────────
# SEGURIDAD
# ─────────────────────────────────────────────────────────────────────────────
# En produccion (Render), SECRET_KEY se genera automaticamente como variable
# de entorno. En local, usa el valor de desarrollo.
SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-)sr9zv1@k$p@0t--ac^i)z043+c4#vg@7s^h9+q0%tgd35b($*'
)

# DEBUG = False en produccion (Render lo setea en False via render.yaml)
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'novafit.onrender.com',
    '.onrender.com',
]

CSRF_TRUSTED_ORIGINS = [
    'https://novafit.onrender.com',
]

# ─────────────────────────────────────────────────────────────────────────────
# APLICACIONES INSTALADAS
# ─────────────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Terceros
    "rest_framework",
    "corsheaders",
    "django_extensions",
    # Aplicaciones del proyecto
    "core",        # Usuarios, Clientes, Instructores, Nutricionistas
    "finanzas",    # Pagos, Suscripciones, Comprobantes, Promociones
    "actividades", # Rutinas, Horarios, Disciplinas, Reservas, Antecedentes
    "api",         # Endpoints REST centralizados
]

# ─────────────────────────────────────────────────────────────────────────────
# MIDDLEWARE
# ─────────────────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",    # Archivos estaticos en prod
    "django.contrib.sessions.middleware.SessionMiddleware",
    "core.middleware.RequestMiddleware",            # Middleware para obtener request actual
    "corsheaders.middleware.CorsMiddleware",         # CORS antes de CommonMiddleware
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "gym_config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR.parent / 'frontend' / 'dist'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "gym_config.wsgi.application"

# ─────────────────────────────────────────────────────────────────────────────
# BASE DE DATOS
# En produccion (Render) se usa DATABASE_URL (PostgreSQL).
# En local se usa SQLite para comodidad de desarrollo.
# ─────────────────────────────────────────────────────────────────────────────
DATABASE_URL = os.environ.get('DATABASE_URL')

if DATABASE_URL:
    # Produccion: PostgreSQL via DATABASE_URL
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=DATABASE_URL,
            conn_max_age=600,
        )
    }
    # Forzar search_path=public para evitar problemas de esquema en Render PostgreSQL.
    # Render configura search_path="$user", public por defecto, lo que puede causar
    # que las tablas se creen en el esquema del usuario y no sean visibles en migraciones
    # subsecuentes que buscan en 'public'.
    DATABASES['default']['OPTIONS'] = {
        'options': '-c search_path=public'
    }
else:
    # Desarrollo local: SQLite
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# ─────────────────────────────────────────────────────────────────────────────
# VALIDACION DE CONTRASENAS
# ─────────────────────────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ─────────────────────────────────────────────────────────────────────────────
# INTERNACIONALIZACION
# ─────────────────────────────────────────────────────────────────────────────
LANGUAGE_CODE = "es-bo"
TIME_ZONE = "America/La_Paz"
USE_I18N = True
USE_TZ = True

# ─────────────────────────────────────────────────────────────────────────────
# ARCHIVOS ESTATICOS (WhiteNoise los sirve en produccion)
# ─────────────────────────────────────────────────────────────────────────────
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR.parent / 'frontend' / 'dist',
]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACION GENERAL
# ─────────────────────────────────────────────────────────────────────────────
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = 'core.CustomUser'

# CORS - Permite solicitudes desde el frontend Vue.js en Render
# ─────────────────────────────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://novafit.onrender.com",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True  # Temporalmente para asegurar acceso

# ─────────────────────────────────────────────────────────────────────────────
# DJANGO REST FRAMEWORK + JWT
# ─────────────────────────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ]
}
