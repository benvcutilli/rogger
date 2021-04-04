# This file and its contents, less this comment, were created by django-admin startproject
# [79, "startproject" documentation]
"""
WSGI config for rogger project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rogger.settings")

application = get_wsgi_application()
