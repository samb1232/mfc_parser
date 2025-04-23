from celery import Celery
from mfc_parser import update_mfc_db

from config import Config

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)


@celery.task
def update_mfc_db_task():
    update_mfc_db()
