import redis
import logging
from celery import Celery
from mfc_parser import update_mfc_db
from chromadb_functions import update_chromadb, get_situation_from_chromadb_by_id
from config import Config


celery = Celery(__name__, broker=Config.CELERY_BROKER_URL, backend=Config.CELERY_RESULT_BACKEND)

redis_client = redis.StrictRedis.from_url(Config.CELERY_BROKER_URL)
logging.basicConfig(level=logging.DEBUG)

@celery.task
def update_mfc_db_task():
    try:
        logging.info("Starting update_mfc_db_task")
        redis_client.set("is_updating", "1")
        update_mfc_db()
        return {"status": "OK"}
    except Exception as e:
        logging.error(f"Error in update_mfc_db_task: {e}")
        return {"status": "ERROR", "message": str(e)}
    finally:
        redis_client.set("is_updating", "0")
        logging.info("Finished update_mfc_db_task")


@celery.task
def update_chromadb_task():
    try:
        result = update_chromadb()
        return result
    except Exception as e:
        return {"status": "error", "message": str(e)}
