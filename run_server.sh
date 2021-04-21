#!/bin/ash
# source env.sh
# run required migrations
echo 'Running migrations'
python manage.py db upgrade

return_code=$?
if [ $return_code -ne 0 ]
then
    echo "Terminating... : error in running migrations"
    exit 1
fi

# Run all the tests
# pytest -v

# Run server
gunicorn -c gunicorn_config.py service.server:app 
# & celery -A service.server.celery_app worker --concurrency=1 -l INFO