"""
WSGI config for gainSkills project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gainSkills.settings')


# напишем декоратор для get_wsgi_application(), чтобы выводить переменные окружения

# def wsgi_app(func):
#     def wsgi_wrapper():
#         print('Переменные окружения: ', os.environ)
#         return func
#
#     return wsgi_wrapper
#
#
# get_wsgi_application = wsgi_app(get_wsgi_application)

application = get_wsgi_application()
