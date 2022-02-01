#!/usr/bin/python
import sys
import os

sys.path.insert(0, '/var/www/sepaPaymentdev/priv/sepaPayment')
sys.path.insert(0, '/var/www/sepaPaymentdev/priv/venv/lib/python3.5/site-packages/')

"""
WSGI config for sepaPayment project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "sepaPayment.settings_prod")

application = get_wsgi_application()
