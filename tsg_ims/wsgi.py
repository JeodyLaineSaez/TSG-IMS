"""
WSGI config for tsg_ims project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tsg_ims.settings')

application = get_wsgi_application() 