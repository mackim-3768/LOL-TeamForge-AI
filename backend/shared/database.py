from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, ForeignKey, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

# Default to MariaDB for development; can be overridden via DB_URL env var
# Example: DB_URL="mysql+pymysql://lol_user:lol_pass@localhost:3306/lol_flex_analyst"
DB_URL = os.getenv("DB_URL", "mysql+pymysql://lol_user:lol_pass@localhost:3306/lol_flex_analyst")

engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if "sqlite" in DB_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Summoner(Base):
    __tablename__ = "summoners"

    id = Column(Integer, primary_key=True, index=True)
    summoner_name = Column(String(100), unique=True, index=True) # Normalized name?
    puuid = Column(String(100), unique=True, index=True)
    summoner_id = Column(String(100), unique=True) # Encrypted Summoner ID
    account_id = Column(String(100))
    profile_icon_id = Column(Integer)
    summoner_level = Column(Integer)
    last_updated = Column(DateTime, default=datetime.utcnow)
    
    matches = relationship("MatchPerformance", back_populates="summoner")

class MatchPerformance(Base):
    __tablename__ = "match_performances"

    id = Column(Integer, primary_key=True, index=True)
    summoner_id = Column(Integer, ForeignKey("summoners.id"))
    match_id = Column(String(50), index=True) # Riot Match ID (e.g., KR_123456789)
    game_creation = Column(DateTime) # Timestamp of the game
    
    # Lane/Role info
    lane = Column(String(20)) # TOP, JUNGLE, MIDDLE, BOTTOM, UTILITY (or parsed role)
    role = Column(String(20))
    champion_name = Column(String(50))
    
    # Stats for scoring
    win = Column(Boolean)
    kills = Column(Integer)
    deaths = Column(Integer)
    assists = Column(Integer)
    kda = Column(Float) # Calculated or stored? Storing for query speed
    gold_per_min = Column(Float)
    vision_score = Column(Integer)
    total_minions_killed = Column(Integer)
    
    # Additional Context for AI
    total_damage_dealt_to_champions = Column(Integer)
    
    summoner = relationship("Summoner", back_populates="matches")

class MatchDetail(Base):
    __tablename__ = "match_details"

    id = Column(Integer, primary_key=True, index=True)
    match_id = Column(String(50), unique=True, index=True)
    raw = Column(JSON)

def init_db():
    Base.metadata.create_all(bind=engine)
