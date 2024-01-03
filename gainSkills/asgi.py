"""
ASGI config for gainSkills project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gainSkills.settings')

application = get_asgi_application()

# Файл asgi.py в Django представляет собой ASGI (Asynchronous Server Gateway Interface) конфигурацию для вашего проекта.
# ASGI - это интерфейс для взаимодействия между веб-серверами и веб-приложениями в асинхронном стиле, что позволяет
# обрабатывать больше одновременных соединений и асинхронных операций.
