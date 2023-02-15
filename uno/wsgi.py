"""
WSGI config for uno project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os
import socketio
from socket_game.views import sio

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uno.settings')

application = get_wsgi_application()
application = socketio.WSGIApp(sio, application)


import eventlet
import eventlet.wsgi

eventlet.wsgi.server(eventlet.listen(("127.0.0.1", 8000)), application)