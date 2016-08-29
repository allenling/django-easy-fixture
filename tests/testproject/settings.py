# coding=utf-8
from __future__ import unicode_literals
from __future__ import absolute_import
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
SECRET_KEY = 'testing'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
    }
}
INSTALLED_APPS = ('django.contrib.auth',
                  'django.contrib.contenttypes',
                  'django.contrib.sessions',
                  'django.contrib.messages',
                  'django.contrib.staticfiles',
                  'django.contrib.sites',
                  'testapp'
                  )
MIGRATION_MODULES = {}
