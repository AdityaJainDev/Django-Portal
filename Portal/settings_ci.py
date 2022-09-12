"""
Django settings for sepaPayment project. for CI
"""

# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import

from Portal.settings import *
import os

ALLOWED_HOSTS = ["127.0.0.1", "localhost", "::1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        'NAME': 'nice_marmot',
        'USER': 'runner',
        'PASSWORD': 'password',
        'HOST': 'db',
    },
}