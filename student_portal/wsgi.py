"""
WSGI config for student_portal project.

Exposes the WSGI callable as a module-level variable named application.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'student_portal.settings')

application = get_wsgi_application()
