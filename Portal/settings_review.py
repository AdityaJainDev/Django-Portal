""" crm2 review settings"""

from crm.settings import *

import os

url = f"{os.environ['BRANCH_NAME']}.Portal-review.aditsystems.de"
ALLOWED_HOSTS = ['127.0.0.1', 'localhost', url]
STATIC_ROOT = os.path.join(BASE_DIR, f"../{os.environ['BRANCH_NAME']}-static")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        'NAME': os.environ['BRANCH_NAME'],
    },
}
