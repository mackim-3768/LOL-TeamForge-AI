from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from backend.shared.database import get_db, Summoner, MatchPerformance, MatchDetail
from backend.collector.collector_service import CollectorService
from backend.collector.config import Config
from backend.core_api.ai_module import get_ai_provider, AIProvider
from backend.tasks import collect_summoner_data
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime, timedelta

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

# OP Score weights & baselines (0~10 scale)
OP_W_KILL = 0.2
OP_W_KDA = 0.25
OP_W_DAMAGE = 0.3
OP_W_GOLD = 0.15
OP_W_CS = 0.1

OP_BASE_KILLS = 10  # 10킬이면 만점 근처
OP_BASE_KDA = 3.0   # KDA 3.0을 기준
OP_BASE_DAMAGE = 30000  # 3만 딜
OP_BASE_GOLD = 12000    # 1.2만 골드
OP_BASE_CS = 200        # 200 CS

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

class MatchPerformanceResponse(BaseModel):
    id: int
    match_id: str
    game_creation: datetime
    lane: str
    role: str
    champion_name: str
    win: bool
    kills: int
    deaths: int
    assists: int
    kda: float
    gold_per_min: float
    vision_score: int
    total_minions_killed: int
    total_damage_dealt_to_champions: int

    class Config:
        from_attributes = True

class MatchListResponse(BaseModel):
    matches: List[MatchPerformanceResponse]
    has_more: bool

class MatchDetailParticipant(BaseModel):
    summoner_name: str
    champion_name: str
    team_id: int
    lane: str
    role: str
    kills: int
    deaths: int
    assists: int
    kda: float
    total_damage_dealt_to_champions: int
    total_minions_killed: int
    gold_earned: int
    win: bool
    items: List[int]
    primary_rune_id: Optional[int] = None
    op_score: float

class MatchDetailResponse(BaseModel):
    match_id: str
    game_creation: datetime
    game_duration: int
    queue_id: int
    blue_team: List[MatchDetailParticipant]
    red_team: List[MatchDetailParticipant]
    blue_total_kills: int
    red_total_kills: int
    blue_total_gold: int
    red_total_gold: int

class LeaderboardEntry(BaseModel):
    name: str
    level: int
    best_role: Optional[str]
    best_score: float
    games: int

class TeamCompRequest(BaseModel):
    summoner_names: List[str]

class ConfigUpdate(BaseModel):
    riot_api_key: str

class OpenAIConfigUpdate(BaseModel):
    openai_api_key: str

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

def _compute_role_scores_for_summoner(
    summoner: Summoner,
    db: Session,
    since: Optional[datetime] = None,
) -> List[ScoreResponse]:
    """Internal helper to compute role scores, optionally filtered by time."""
    scores: List[ScoreResponse] = []
    roles = ["TOP", "JUNGLE", "MIDDLE", "BOTTOM", "UTILITY"]  # Standardizing

    for role in roles:
        # Filter matches for this role using fuzzy matching/strict mapping
        possible_lanes = ROLE_MAPPINGS.get(role, [role])
        query = db.query(MatchPerformance).filter(
            MatchPerformance.summoner_id == summoner.id,
            MatchPerformance.lane.in_(possible_lanes),
        )
        if since is not None:
            query = query.filter(MatchPerformance.game_creation >= since)
        matches = query.all()

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
        score_wr = min(100, win_rate)
        score_kda = min(100, (avg_kda / 5.0) * 100)
        score_gold = min(100, (avg_gold / 600) * 100)
        score_vision = min(100, (avg_vision / 40) * 100)

        final_score = (
            score_wr * 0.4
            + score_kda * 0.3
            + score_gold * 0.15
            + score_vision * 0.15
        )

        scores.append(
            ScoreResponse(
                role=role,
                score=round(final_score, 1),
                win_rate=round(win_rate, 1),
                kda=round(avg_kda, 2),
                avg_gold=round(avg_gold, 1),
                vision_score=round(avg_vision, 1),
            )
        )

    return scores


def _volume_weight(games: int, target_games: int) -> float:
    """Return a weight 0~1 that penalizes low game counts.

    - 0 games: 0
    - few games: ~0.3~0.5
    - target_games 이상: 1.0
    """
    if games <= 0 or target_games <= 0:
        return 0.0

    ratio = min(1.0, games / float(target_games))
    base = 0.3  # 최소 신뢰도
    return base + (1.0 - base) * ratio


@app.get("/summoners/{name}/scores", response_model=List[ScoreResponse])
def get_summoner_scores(name: str, db: Session = Depends(get_db)):
    """Calculates 0-100 score for each role based on stored match data (all-time)."""
    summoner = db.query(Summoner).filter(Summoner.summoner_name == name).first()
    if not summoner:
        raise HTTPException(status_code=404, detail="Summoner not found")

    return _compute_role_scores_for_summoner(summoner, db)

@app.get("/summoners/{name}/matches", response_model=MatchListResponse)
def get_summoner_matches(
    name: str,
    offset: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
):
    """Return paginated matches for a summoner, most recent first."""
    if limit <= 0 or limit > 100:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 100")

    summoner = db.query(Summoner).filter(Summoner.summoner_name == name).first()
    if not summoner:
        raise HTTPException(status_code=404, detail="Summoner not found")

    query = (
        db.query(MatchPerformance)
        .filter(MatchPerformance.summoner_id == summoner.id)
        .order_by(MatchPerformance.game_creation.desc())
    )

    items = query.offset(offset).limit(limit + 1).all()
    has_more = len(items) > limit
    matches = items[:limit]

    return MatchListResponse(matches=matches, has_more=has_more)


@app.get("/leaderboard", response_model=List[LeaderboardEntry])
def get_leaderboard(timeframe: str = "daily", db: Session = Depends(get_db)):
    """Return leaderboard of summoners based on role scores within a timeframe."""
    valid_timeframes = {"daily", "weekly", "monthly", "yearly"}
    if timeframe not in valid_timeframes:
        raise HTTPException(status_code=400, detail="Invalid timeframe")

    now = datetime.utcnow()
    if timeframe == "daily":
        since = now - timedelta(days=1)
        target_games = 5
    elif timeframe == "weekly":
        since = now - timedelta(days=7)
        target_games = 10
    elif timeframe == "monthly":
        since = now - timedelta(days=30)
        target_games = 20
    else:  # yearly
        since = now - timedelta(days=365)
        target_games = 50

    summoners = db.query(Summoner).all()
    entries: List[LeaderboardEntry] = []

    for summoner in summoners:
        scores = _compute_role_scores_for_summoner(summoner, db, since=since)
        if not scores:
            continue

        role_candidates = []
        for s in scores:
            possible_lanes = ROLE_MAPPINGS.get(s.role, [s.role])
            games = (
                db.query(MatchPerformance)
                .filter(
                    MatchPerformance.summoner_id == summoner.id,
                    MatchPerformance.game_creation >= since,
                    MatchPerformance.lane.in_(possible_lanes),
                )
                .count()
            )
            if games == 0:
                continue

            weight = _volume_weight(games, target_games)
            effective_score = round(s.score * weight, 1)
            role_candidates.append((s.role, effective_score, games))

        if not role_candidates:
            continue

        # Select best role using volume-weighted (effective) score
        best_role, best_effective_score, best_games = max(
            role_candidates, key=lambda x: x[1]
        )

        entries.append(
            LeaderboardEntry(
                name=summoner.summoner_name,
                level=summoner.summoner_level,
                best_role=best_role,
                best_score=best_effective_score,
                games=best_games,
            )
        )

    # Sort by adjusted best_score desc, then by games desc
    entries.sort(key=lambda e: (e.best_score, e.games), reverse=True)

    # Limit to top 50 to keep payload size manageable
    return entries[:50]

@app.get("/matches/{match_id}", response_model=MatchDetailResponse)
def get_match_detail(match_id: str, db: Session = Depends(get_db)):
    db_match = db.query(MatchDetail).filter(MatchDetail.match_id == match_id).first()
    if not db_match:
        raise HTTPException(status_code=404, detail="Match not found")

    data = db_match.raw or {}
    info = data.get("info", {})
    participants = info.get("participants", [])

    participant_models: List[MatchDetailParticipant] = []
    for p in participants:
        kills = p.get("kills", 0)
        deaths = p.get("deaths", 0)
        assists = p.get("assists", 0)
        kda = (kills + assists) / max(1, deaths)

        lane = p.get("teamPosition") or p.get("lane") or ""

        items = [p.get(f"item{i}", 0) for i in range(7)]

        primary_rune_id: Optional[int] = None
        perks = p.get("perks") or {}
        styles = perks.get("styles") or []
        if styles:
            primary_style = None
            for s in styles:
                if s.get("description") == "primaryStyle":
                    primary_style = s
                    break
            if primary_style is None:
                primary_style = styles[0]
            selections = primary_style.get("selections") or []
            if selections:
                primary_rune_id = selections[0].get("perk")

        total_minions = p.get("totalMinionsKilled", 0) + p.get("neutralMinionsKilled", 0)
        total_damage = p.get("totalDamageDealtToChampions", 0)
        gold_earned = p.get("goldEarned", 0)

        # Normalize each component to 0~10 around typical baselines
        kill_score = min(10.0, (kills / OP_BASE_KILLS) * 10.0) if OP_BASE_KILLS > 0 else 0.0
        kda_score = min(10.0, (kda / OP_BASE_KDA) * 10.0) if OP_BASE_KDA > 0 else 0.0
        damage_score = min(10.0, (total_damage / OP_BASE_DAMAGE) * 10.0) if OP_BASE_DAMAGE > 0 else 0.0
        gold_score = min(10.0, (gold_earned / OP_BASE_GOLD) * 10.0) if OP_BASE_GOLD > 0 else 0.0
        cs_score = min(10.0, (total_minions / OP_BASE_CS) * 10.0) if OP_BASE_CS > 0 else 0.0

        raw_score = (
            kill_score * OP_W_KILL
            + kda_score * OP_W_KDA
            + damage_score * OP_W_DAMAGE
            + gold_score * OP_W_GOLD
            + cs_score * OP_W_CS
        )

        if p.get("win"):
            raw_score *= 1.1

        op_score = max(0.0, min(10.0, round(raw_score, 1)))

        participant_models.append(
            MatchDetailParticipant(
                summoner_name=p.get("riotIdGameName") or p.get("summonerName") or "",
                champion_name=p.get("championName", ""),
                team_id=p.get("teamId", 0),
                lane=lane,
                role=p.get("role", ""),
                kills=kills,
                deaths=deaths,
                assists=assists,
                kda=kda,
                total_damage_dealt_to_champions=total_damage,
                total_minions_killed=total_minions,
                gold_earned=gold_earned,
                win=p.get("win", False),
                items=items,
                primary_rune_id=primary_rune_id,
                op_score=op_score,
            )
        )

    blue_team = [p for p in participant_models if p.team_id == 100]
    red_team = [p for p in participant_models if p.team_id == 200]

    raw_game_creation = info.get("gameCreation", 0)
    try:
        game_creation = datetime.fromtimestamp(raw_game_creation / 1000) if raw_game_creation else datetime.utcfromtimestamp(0)
    except Exception:
        game_creation = datetime.utcfromtimestamp(0)

    game_duration = int(info.get("gameDuration", 0))
    queue_id = int(info.get("queueId", 0))

    blue_total_kills = sum(p.kills for p in blue_team)
    red_total_kills = sum(p.kills for p in red_team)
    blue_total_gold = sum(p.gold_earned for p in blue_team)
    red_total_gold = sum(p.gold_earned for p in red_team)

    return MatchDetailResponse(
        match_id=match_id,
        game_creation=game_creation,
        game_duration=game_duration,
        queue_id=queue_id,
        blue_team=blue_team,
        red_team=red_team,
        blue_total_kills=blue_total_kills,
        red_total_kills=red_total_kills,
        blue_total_gold=blue_total_gold,
        red_total_gold=red_total_gold,
    )

@app.put("/admin/config/riot-key")
def update_riot_key(config: ConfigUpdate):
    Config.update_api_key(config.riot_api_key)
    return {"message": "API Key updated successfully"}

@app.put("/admin/config/openai-key")
def update_openai_key(config: OpenAIConfigUpdate):
    Config.update_openai_key(config.openai_api_key)
    return {"message": "OpenAI API Key updated successfully"}

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
