import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'testing'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
TIME_ZONE = 'UTC'
USE_TZ = True
INSTALLED_APPS = ('django.contrib.auth',
                  'django.contrib.contenttypes',
                  'django.contrib.sessions',
                  'django.contrib.messages',
                  'django.contrib.staticfiles',
                  'django.contrib.sites',
                  'testapp'
                  )
MIGRATION_MODULES = {}
