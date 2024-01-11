from config.settings.base import *


ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS").split(" ")
X_FRAME_OPTIONS = 'SAMEORIGIN'
CSP_FRAME_ANCESTORS = "http://213.230.99.101"

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

# media
MEDIA_URL = "/var/www/tkti_uz/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "/var/www/tkti_uz/media/")
