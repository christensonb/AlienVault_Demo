"""
WSGI config for Alien_Vault project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""
__author__ = 'Ben Christenson'
__date__ = "2/8/16"

import os
import sys
from django.core.wsgi import get_wsgi_application


sys.path.append(os.path.split(__file__)[0])
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

application = get_wsgi_application()
