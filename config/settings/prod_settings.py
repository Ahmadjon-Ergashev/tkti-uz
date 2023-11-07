from config.settings.base import *


ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS").split(" ")
X_FRAME_OPTIONS = 'SAMEORIGIN'
CSP_FRAME_ANCESTORS = "http://185.74.5.139"

DATABASES = {
    'default': {
        'ENGINE': env("POSTGRES_ENGINE"),
        'NAME': env("POSTGRES_DB"),
        'USER': env("POSTGRES_USER"),
        'PASSWORD': env("POSTGRES_PASSWORD"),
        'HOST': env("POSTGRES_HOST"),
        'PORT': 5432,
    }
}