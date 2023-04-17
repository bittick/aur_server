nohup python manage.py runserver &
nohup celery -A parseServer worker --beat --loglevel=info &
nohup celery -A parseServer flower --address=0.0.0.0 --port=5555 -broker_api=redis://localhost:6379/0 &