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
        page_size = 50
        start = 0

        while True:
            match_ids = self.riot_client.get_match_ids(summoner.puuid, start=start, count=page_size)
            if not match_ids:
                break

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

            if len(match_ids) < page_size:
                break

            start += page_size
                
    def add_summoner(self, name: str):
        # This might be called by the API service, or we just rely on DB shared state
        # Logic: Check Riot, get info, save to DB
        session = SessionLocal()
        try:
            summoner_data = None
            base_name = name

            if "#" in name:
                game_name, tag_line = name.split("#", 1)
                game_name = game_name.strip()
                tag_line = tag_line.strip()
                base_name = game_name

                existing = session.query(Summoner).filter_by(summoner_name=game_name).first()
                if existing:
                    return existing

                account_data = self.riot_client.get_account_by_riot_id(game_name, tag_line)
                if not account_data:
                    return None

                puuid = account_data.get("puuid")
                if not puuid:
                    return None

                summoner_data = self.riot_client.get_summoner_by_puuid(puuid)
            else:
                existing = session.query(Summoner).filter_by(summoner_name=name).first()
                if existing:
                    return existing

                summoner_data = self.riot_client.get_summoner_by_name(name)

            if not summoner_data:
                return None
            
            puuid = summoner_data.get('puuid')
            summoner_name = summoner_data.get('name') or summoner_data.get('gameName') or base_name
            summoner_id = summoner_data.get('id') or summoner_data.get('summonerId')
            account_id = summoner_data.get('accountId')
            profile_icon_id = summoner_data.get('profileIconId')
            summoner_level = summoner_data.get('summonerLevel', 0)

            if not puuid:
                logger.error(f"Invalid summoner data from Riot API (missing puuid): {summoner_data}")
                return None

            existing = session.query(Summoner).filter_by(puuid=puuid).first()
            if existing:
                return existing

            existing = session.query(Summoner).filter_by(summoner_name=summoner_name).first()
            if existing:
                return existing

            new_summoner = Summoner(
                summoner_name=summoner_name,
                puuid=puuid,
                summoner_id=summoner_id,
                account_id=account_id,
                profile_icon_id=profile_icon_id,
                summoner_level=summoner_level
            )
            session.add(new_summoner)
            session.commit()
            session.refresh(new_summoner)
            
            # Initial fetch
            self.update_summoner_data(session, new_summoner)
            
            return new_summoner
        finally:
            session.close()
