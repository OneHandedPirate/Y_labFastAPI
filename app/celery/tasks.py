from app.celery.celeryconfig import celery_app
from app.utils.sync_db import sync_db


@celery_app.task
def sync_database():
    res = sync_db()
    return res
