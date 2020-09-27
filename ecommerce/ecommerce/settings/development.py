from .base import *


try:
    db_name = credentials['DB_NAME']
except KeyError:
    raise ImproperlyConfigured(
        "Improperly configured database settings in config.yaml.")


if credentials['DB_ENGINE'] == 'mysql':
    try:
        db_user = credentials['DB_USER']
        db_password = credentials['DB_PASSWORD']
        db_port = credentials['DB_PORT']
    except KeyError:
        raise ImproperlyConfigured(
            "Improperly configured database settings in config.yaml.")

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': db_name,
            'USER': db_user,
            'PASSWORD': db_password,
            'PORT': db_port
        }
    }
elif credentials['DB_ENGINE'] == 'sqlite3':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, db_name+'.sqlite3'),
        }
    }
