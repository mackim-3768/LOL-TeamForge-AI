from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from backend.shared.database import get_db, Summoner, MatchPerformance
from backend.collector.collector_service import CollectorService
from backend.collector.config import Config
from backend.core_api.ai_module import get_ai_provider, AIProvider
from backend.tasks import collect_summoner_data
from fastapi.middleware.cors import CORSMiddleware
import logging

# Setup Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="LoL Flex Rank Analyst")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow all for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency injection for Collector Service
def get_collector_service():
    return CollectorService()

# --- Constants ---
ROLE_MAPPINGS = {
    "TOP": ["TOP"],
    "JUNGLE": ["JUNGLE"],
    "MIDDLE": ["MIDDLE", "MID"],
    "BOTTOM": ["BOTTOM", "BOT", "ADC"],
    "UTILITY": ["UTILITY", "SUPPORT"]
}

# --- Pydantic Models ---
class SummonerCreate(BaseModel):
    name: str

class SummonerResponse(BaseModel):
    id: int
    name: str
    level: int
    # Add other fields as needed

    class Config:
        from_attributes = True

class ScoreResponse(BaseModel):
    role: str
    score: float
    win_rate: float
    kda: float
    avg_gold: float
    vision_score: float

class AnalysisResponse(BaseModel):
    analysis: str

class TeamCompRequest(BaseModel):
    summoner_names: List[str]

class ConfigUpdate(BaseModel):
    riot_api_key: str

# --- Endpoints ---

@app.post("/summoners/", response_model=SummonerResponse)
def register_summoner(
    summoner: SummonerCreate, 
    db: Session = Depends(get_db),
    collector: CollectorService = Depends(get_collector_service)
):
    """
    Registers a new summoner. If they don't exist in DB, fetches from Riot API.
    """
    # Check if exists
    db_summoner = db.query(Summoner).filter(Summoner.summoner_name == summoner.name).first()
    if db_summoner:
        return SummonerResponse(id=db_summoner.id, name=db_summoner.summoner_name, level=db_summoner.summoner_level)

    # Trigger collection (This relies on Riot API being valid)
    # In a real async MSA, we might push a message to a queue.
    # Here we call the service method directly.
    new_summoner = collector.add_summoner(summoner.name)
    if not new_summoner:
        raise HTTPException(status_code=404, detail="Summoner not found on Riot API")
    
    # Push collection task to the queue
    try:
        collect_summoner_data.delay(new_summoner.id)
    except Exception as e:
        logger.error(f"Failed to enqueue background collection task: {e}. Falling back to synchronous collection.")
        collector.update_summoner_data(db, new_summoner)

    return SummonerResponse(id=new_summoner.id, name=new_summoner.summoner_name, level=new_summoner.summoner_level)

@app.get("/summoners/", response_model=List[SummonerResponse])
def list_summoners(db: Session = Depends(get_db)):
    summoners = db.query(Summoner).all()
    return [SummonerResponse(id=s.id, name=s.summoner_name, level=s.summoner_level) for s in summoners]

@app.get("/summoners/{name}/scores", response_model=List[ScoreResponse])
def get_summoner_scores(name: str, db: Session = Depends(get_db)):
    """
    Calculates 0-100 score for each role based on stored match data.
    """
    summoner = db.query(Summoner).filter(Summoner.summoner_name == name).first()
    if not summoner:
        raise HTTPException(status_code=404, detail="Summoner not found")

    scores = []
    roles = ["TOP", "JUNGLE", "MIDDLE", "BOTTOM", "UTILITY"] # Standardizing
    
    for role in roles:
        # Filter matches for this role using fuzzy matching/strict mapping
        possible_lanes = ROLE_MAPPINGS.get(role, [role])
        matches = db.query(MatchPerformance).filter(
            MatchPerformance.summoner_id == summoner.id,
            MatchPerformance.lane.in_(possible_lanes)
        ).all()
        
        if not matches:
            continue
            
        # Calculate Metrics
        total_games = len(matches)
        wins = sum(1 for m in matches if m.win)
        avg_kda = sum(m.kda for m in matches) / total_games
        avg_gold = sum(m.gold_per_min for m in matches) / total_games
        avg_vision = sum(m.vision_score for m in matches) / total_games
        win_rate = (wins / total_games) * 100
        
        # Simple Scoring Algorithm (0-100)
        # Weights: WR(40%), KDA(30%), Gold(15%), Vision(15%)
        # Normalize: 
        # WR: 50% is baseline(50pts). 
        # KDA: 3.0 is baseline.
        # Gold: 400 is baseline.
        # Vision: 20 is baseline.
        
        score_wr = min(100, win_rate)
        score_kda = min(100, (avg_kda / 5.0) * 100)
        score_gold = min(100, (avg_gold / 600) * 100) 
        score_vision = min(100, (avg_vision / 40) * 100)
        
        final_score = (score_wr * 0.4) + (score_kda * 0.3) + (score_gold * 0.15) + (score_vision * 0.15)
        
        scores.append(ScoreResponse(
            role=role,
            score=round(final_score, 1),
            win_rate=round(win_rate, 1),
            kda=round(avg_kda, 2),
            avg_gold=round(avg_gold, 1),
            vision_score=round(avg_vision, 1)
        ))
        
    return scores

@app.put("/admin/config/riot-key")
def update_riot_key(config: ConfigUpdate):
    Config.update_api_key(config.riot_api_key)
    return {"message": "API Key updated successfully"}

@app.get("/analysis/summoner/{name}", response_model=AnalysisResponse)
def analyze_summoner(name: str, db: Session = Depends(get_db)):
    scores = get_summoner_scores(name, db) # Reuse logic to get stats
    # Convert ScoreResponse objects to dicts for AI
    stats_dicts = [s.dict() for s in scores]
    
    ai = get_ai_provider()
    analysis = ai.analyze_summoner_performance(name, stats_dicts)
    return AnalysisResponse(analysis=analysis)

@app.post("/analysis/recommend-comp", response_model=AnalysisResponse)
def recommend_team(request: TeamCompRequest, db: Session = Depends(get_db)):
    # Gather stats for all 5 summoners
    all_stats = {}
    for name in request.summoner_names:
        try:
            scores = get_summoner_scores(name, db)
            all_stats[name] = [s.dict() for s in scores]
        except HTTPException:
            all_stats[name] = [] # Handle missing summoner
            
    ai = get_ai_provider()
    recommendation = ai.recommend_team_composition(request.summoner_names, all_stats)
    return AnalysisResponse(analysis=recommendation)
