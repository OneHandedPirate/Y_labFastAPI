import asyncio

from app.celery.celeryconfig import celery_app
from app.utils.sync_db import sync_db


@celery_app.task
def sync_database():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    res = loop.run_until_complete(sync_db())
    loop.close()

    return res
