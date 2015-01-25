import os
import environ

# Reads the environment file (.env)
environ.Env.read_env(env_file="../.env")
env = environ.Env()
API_KEY = env("api_key")

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
    #'django.contrib.auth',
    'app',
)

SECRET_KEY = "1"
