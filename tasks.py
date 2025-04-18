from celery import Celery
from parser import update_mfc_db

celery = Celery(__name__, broker='redis://localhost:6379/0')

@celery.task
def update_mfc_db_task():
    update_mfc_db()
