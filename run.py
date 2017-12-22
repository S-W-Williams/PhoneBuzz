from celery import current_app
from celery.bin import worker
from LendUpCodingChallenge import app

application = current_app._get_current_object()

worker = worker.worker(app=application)

options = {
    'broker': app.config['CELERY_BROKER_URL'],
    'loglevel': 'NOTSET',
    'traceback': True,
}

worker.run(**options)
