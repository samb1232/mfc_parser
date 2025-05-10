from celery import Celery
from mfc_parser import update_mfc_db
from chromadb_functions import update_chromadb, get_situation_from_chromadb_by_id
from config import Config


celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)

@celery.task
def update_mfc_db_task():
    try:
        update_mfc_db()
        return {"status": "OK"}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

@celery.task
def update_chromadb_task():
    try:
        result = update_chromadb()
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}
