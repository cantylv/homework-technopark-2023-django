# gainSkills.settings
raw_env = ['SECRET_KEY=django-insecure-g@@-sggo!g%6p39q$_p)oddz9#l!*d$ue46i-eoh@wdm#&=*b5']


# непосредственная настройка Application Server
port = 8000

bind = f'localhost:{port}'
workers = 2

# логи работы WSGI-server
accesslog = './var/tmp/gunicorn_logs/access.g.log'

# команды для запуска приложения из скрипта
wsgi_app = 'gainSkills.wsgi'

# для задания:
# wsgi_app = 'test_wsgi.test'


# Настройка сокета
# максимальное кол-во коннектов, ожидающих обработку запроса
backlog = 100

# максимальное кол-во обрабатываемых коннектов
worker_connections = 500

# максимальное кол-во запросов, которое обработает воркер перед перезагрузкой
max_requests = 50

# Время, которое воркер будет жить перед рестартом. Таймер обновляется, если пришел запрос на обработку
timeout = 60
