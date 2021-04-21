from service.server import app, db, celery_app


@celery_app.task
def print_x():
    print("I am beating every 5 seconds")