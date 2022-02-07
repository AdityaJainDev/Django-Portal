"""
Django settings for Portal project. for Docker container

"""
# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import

from Portal.settings import *

# chromedriver path
CHROMEDRIVER_PATH = "/usr/local/bin/chromedriver"
CHROMEDRIVER_SHOW_UI = False

# Api flags
CALL_EXTERNAL_SERVICES = True
PRODUCTION = True

# sepa server
SEPASERVER_URL = "http://sepaserver:80"
SEPASERVER_API_KEY = "yetanotherapikey"
