"""
ASGI config for sentinel_tracker project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sentinel_tracker.settings')

application = get_asgi_application()
