"""
Django settings for Portal project. for Docker container

"""
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import

from Portal.settings import *

# Api flags
CALL_EXTERNAL_SERVICES = True
PRODUCTION = True


# sepa server
SEPASERVER_URL = "http://sepaserver:80"
SEPASERVER_API_KEY = "yetanotherapikey"
