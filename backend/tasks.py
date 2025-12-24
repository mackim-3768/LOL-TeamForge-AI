from backend.celery_app import celery_app
from backend.collector.collector_service import CollectorService
from backend.shared.database import SessionLocal, Summoner
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3)
def collect_summoner_data(self, summoner_id: int):
    """
    Background task to collect summoner match data.
    """
    logger.info(f"Starting background collection for summoner_id={summoner_id}")
    db = SessionLocal()
    try:
        summoner = db.query(Summoner).filter(Summoner.id == summoner_id).first()
        if not summoner:
            logger.error(f"Summoner {summoner_id} not found in DB.")
            return

        collector = CollectorService()
        collector.update_summoner_data(db, summoner)
        logger.info(f"Completed background collection for {summoner.summoner_name}")
    except Exception as e:
        logger.error(f"Error collecting data for {summoner_id}: {e}")
        # Retry with exponential backoff
        raise self.retry(exc=e, countdown=60 * (2 ** self.request.retries))
    finally:
        db.close()
