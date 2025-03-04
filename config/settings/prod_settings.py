from config.settings.base import *


ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS").split(" ")
X_FRAME_OPTIONS = 'SAMEORIGIN'
CSP_FRAME_ANCESTORS = "https://tkti.uz/"

DATABASES = {
    'default': {
        'ENGINE': env("POSTGRES_ENGINE"),
        'NAME': env("POSTGRES_DB"),
        'USER': env("POSTGRES_USER"),
        'PASSWORD': env("POSTGRES_PASSWORD"),
        'HOST': env("POSTGRES_HOST"),
        'PORT': env("POSTGRES_PORT"),
    }
}
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https') 

# media
MEDIA_URL = "/var/www/tkti_uz/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "/var/www/tkti_uz/media/")

# redis

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
