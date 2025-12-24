import time
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from backend.shared.database import SessionLocal, Summoner, MatchPerformance, engine, Base
from .riot_client import RiotAPIClient
from .data_processor import DataProcessor
import logging

# Ensure tables exist
Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CollectorService:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.riot_client = RiotAPIClient()
        self.db = SessionLocal()

    def start(self):
        # Poll every 30 minutes
        self.scheduler.add_job(self.poll_summoners, 'interval', minutes=30)
        self.scheduler.start()
        logger.info("Collector Service started.")

    def poll_summoners(self):
        logger.info("Polling all summoners...")
        session = SessionLocal()
        try:
            summoners = session.query(Summoner).all()
            for summoner in summoners:
                self.update_summoner_data(session, summoner)
        finally:
            session.close()

    def update_summoner_data(self, session: Session, summoner: Summoner):
        logger.info(f"Updating data for {summoner.summoner_name}...")
        match_ids = self.riot_client.get_match_ids(summoner.puuid)
        
        for match_id in match_ids:
            # Check if match already exists
            exists = session.query(MatchPerformance).filter_by(match_id=match_id, summoner_id=summoner.id).first()
            if exists:
                continue
            
            match_details = self.riot_client.get_match_details(match_id)
            if not match_details:
                continue

            performance_data = DataProcessor.extract_performance(match_details, summoner.puuid)
            if performance_data:
                performance = MatchPerformance(**performance_data)
                performance.summoner_id = summoner.id
                session.add(performance)
                session.commit()
                logger.info(f"Saved match {match_id} for {summoner.summoner_name}")
                
    def add_summoner(self, name: str):
        # This might be called by the API service, or we just rely on DB shared state
        # Logic: Check Riot, get info, save to DB
        session = SessionLocal()
        try:
            existing = session.query(Summoner).filter_by(summoner_name=name).first()
            if existing:
                return existing

            summoner_data = self.riot_client.get_summoner_by_name(name)
            if not summoner_data:
                return None
            
            new_summoner = Summoner(
                summoner_name=summoner_data['name'],
                puuid=summoner_data['puuid'],
                summoner_id=summoner_data['id'],
                account_id=summoner_data['accountId'],
                profile_icon_id=summoner_data['profileIconId'],
                summoner_level=summoner_data['summonerLevel']
            )
            session.add(new_summoner)
            session.commit()
            session.refresh(new_summoner)
            
            # Note: Initial fetch is now handled by the async queue
            
            return new_summoner
        finally:
            session.close()
