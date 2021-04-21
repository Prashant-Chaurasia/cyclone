import os
reload=True
bind = '0.0.0.0:7007'
backlog = 2048

workers = int(os.environ.get('GUNICORN_NUMBER_WORKERS', 1))
worker_class = 'sync'
worker_connections = 1000
timeout = 600
keepalive = 2
spew = False

errorlog = '-'
accesslog = '-'
loglevel = 'info'