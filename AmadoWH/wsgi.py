"""
WSGI config for AmadoWH project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import os, sys
# add the hellodjango project path into the sys.path
sys.path.append('/home/AmadoWH/AmadoWH')

# add the virtualenv site-packages path to the sys.path
sys.path.append('/venvs/AmadoWH/lib/python3.6/site-packages')
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AmadoWH.settings")

application = get_wsgi_application()
import sys
sys.path.insert(0, '/home/AmadoWH/AmadoWH')