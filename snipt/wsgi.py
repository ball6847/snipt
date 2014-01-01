"""
WSGI config for myproject project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "snipt.settings")

from django.core.wsgi import get_wsgi_application
from werkzeug.debug import DebuggedApplication

application = get_wsgi_application()



# @todo check if settings.DEBUG is True or False
# setup werkzerg
application = DebuggedApplication(application, evalex=True)

# error page handling
def null_technical_500_response(request, exc_type, exc_value, tb):
    raise exc_type, exc_value, tb

django.views.debug.technical_500_response = null_technical_500_response