"""
Django settings for sepaPayment project. for CI
"""

# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import

from Portal.settings import *

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '::1']
SECRET_KEY = "CI ONLY"