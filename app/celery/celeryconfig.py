from celery import Celery

from app.core.settings import RABBITMQ_URL

celery_app = Celery('celery',
                    broker=RABBITMQ_URL,
                    include=['app.celery.tasks'])

celery_app.conf.beat_schedule = {
    'sync-db-every-15-seconds': {
        'task': 'app.celery.tasks.sync_database',
        'schedule': 15,
    },
}
