import os
from celery.schedules import crontab

class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(
        os.getenv('DB_USER'),
        os.getenv('DB_PASSWORD'),
        os.getenv('POSTGRES_SERVICE_HOST'),
        os.getenv('POSTGRES_SERVICE_PORT'),
        os.getenv('DB_NAME')
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

    BEAT_SCHEDULE = {
        'test-celery': {
            'task': 'tasks.tasks.print_x',
            # Every minute
            'schedule': 30.0,
        }
    }