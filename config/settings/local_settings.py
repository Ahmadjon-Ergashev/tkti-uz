from config.settings.base import *

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': "django.db.backends.postgresql_psycopg2",
        'NAME': "tkti",
        'USER': "postgres",
        'PASSWORD': "123456",
        'HOST': "localhost",
        'PORT': "5432",
    }
}