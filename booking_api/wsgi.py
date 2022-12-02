"""
WSGI config for booking_api project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booking_api.settings')

application = get_wsgi_application()

schema_view = get_schema_view(
    openapi.Info(
        title='Python18 Hotel project',
        description='Бронь отелей',
        default_version='v1',
    ),
    public=True
)
