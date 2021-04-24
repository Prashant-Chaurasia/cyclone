from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
from .config import Config 
import os, json

def create_app():
    app = Flask(__name__)
    CORS(app, resources=r'/*', supports_credentials=True)
    app.config.from_object(Config)
    return app


def create_celery(app):
    app.config['CELERY_BROKER_URL'] = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
    # create context tasks in celery
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'], include=['main.tasks.tasks'])
    celery.conf.update(app.config)
    celery.conf.beat_schedule = app.config['BEAT_SCHEDULE']
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery

app = create_app()
db = SQLAlchemy(app)
celery_app = create_celery(app)


@app.after_request
def add_header(response):
    response.headers['Content-type'] = 'application/json'
    return response


@app.route('/ready', methods = ['GET'])
def index():
    response = jsonify({"message": "Service is ready!"})
    return response


# Any url with /cyclones will be routed to the cyclone_module.apis
from main.cyclone_module import cyclone_apis
app.register_blueprint(cyclone_apis, url_prefix='/cyclones')


