from os.path import abspath, dirname, join
import sys
import site

site_dir = dirname(abspath(__file__))

# add application directoy to system
sys.path.insert(0, dirname(site_dir))
sys.path.insert(0, site_dir)

version = "python" + ".".join(map(str, sys.version_info[:2]))

# add virtualenv site-packages
site.addsitedir(join(site_dir, "venv", "lib", version, "site-packages"))

# -------------------------------------------------------------------------
# now we can import module from virtualenv

import django
from django.core.management import setup_environ
from django.core.handlers.wsgi import WSGIHandler
from werkzeug.debug import DebuggedApplication
import settings

# setup django environment
setup_environ(settings)

# start WSGIHandler
application = WSGIHandler()

# setup werkzerg
application = DebuggedApplication(application, evalex=True)

# error page handling
def null_technical_500_response(request, exc_type, exc_value, tb):
    raise exc_type, exc_value, tb

django.views.debug.technical_500_response = null_technical_500_response
