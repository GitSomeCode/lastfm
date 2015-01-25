import os
"""
Contains the database access settings.
"""

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'db.sqlite3',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': ''
    }
}

INSTALLED_APPS = (
    'django.contrib.auth',
    'app',
)

SECRET_KEY = "1"
