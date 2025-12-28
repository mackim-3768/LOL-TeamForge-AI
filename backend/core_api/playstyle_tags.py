from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.shared.database import Summoner, MatchPerformance, SummonerPlaystyleTag

TAG_VERSION = "v1"


class DimensionScores(BaseModel):
    aggro: float
    risk: float
    vision: float
    farm: float
    damage: float
    winrate: float


class TagDefinition(BaseModel):
    id: str
    label_ko: str
    role_scope: str
    min_games: int
    weights: Dict[str, float]
    threshold: float
    risk_max: Optional[float] = None
    color: Optional[str] = None


ROLE_MAPPINGS: Dict[str, List[str]] = {
    "TOP": ["TOP"],
    "JUNGLE": ["JUNGLE"],
    "MIDDLE": ["MIDDLE", "MID"],
    "BOTTOM": ["BOTTOM", "BOT", "ADC"],
    "UTILITY": ["UTILITY", "SUPPORT"],
}


def _safe_div(numerator: float, denominator: float) -> float:
    if denominator <= 0:
        return 0.0
    return numerator / denominator


def compute_dimensions(matches: List[MatchPerformance]) -> DimensionScores:
    games = len(matches)
    if games == 0:
        return DimensionScores(aggro=0.0, risk=0.0, vision=0.0, farm=0.0, damage=0.0, winrate=0.0)

    total_kills = sum(m.kills for m in matches)
    total_deaths = sum(m.deaths for m in matches)
    total_assists = sum(m.assists for m in matches)
    avg_kda = _safe_div(total_kills + total_assists, max(1, total_deaths))

    avg_kills = _safe_div(total_kills, games)
    avg_assists = _safe_div(total_assists, games)
    avg_deaths = _safe_div(total_deaths, games)
    avg_gold_per_min = _safe_div(sum(m.gold_per_min for m in matches), games)
    avg_vision = _safe_div(sum(m.vision_score for m in matches), games)
    avg_cs = _safe_div(sum(m.total_minions_killed for m in matches), games)
    avg_damage = _safe_div(sum(m.total_damage_dealt_to_champions for m in matches), games)
    win_rate = _safe_div(sum(1 for m in matches if m.win), games)

    aggro = min(1.0, (avg_kills + 0.7 * avg_assists) / 15.0)
    risk_component = min(1.0, avg_deaths / 8.0)
    kda_component = min(1.0, avg_kda / 6.0)
    risk = max(0.0, risk_component * (1.0 - kda_component))
    vision = min(1.0, avg_vision / 50.0)
    farm = min(1.0, (avg_cs / 220.0 + avg_gold_per_min / 600.0) / 2.0)
    damage = min(1.0, avg_damage / 35000.0)
    winrate = win_rate

    return DimensionScores(
        aggro=aggro,
        risk=risk,
        vision=vision,
        farm=farm,
        damage=damage,
        winrate=winrate,
    )


TAG_DEFINITIONS: List[TagDefinition] = [
    TagDefinition(
        id="GLOBAL_AGGRO_EXTREME",
        label_ko="극공격적",
        role_scope="ANY",
        min_games=10,
        weights={"aggro": 1.0, "risk": 0.3},
        threshold=0.9,
        color="#ef5350",
    ),
    TagDefinition(
        id="GLOBAL_SAFE",
        label_ko="안정 추구",
        role_scope="ANY",
        min_games=10,
        weights={"risk": -1.0, "winrate": 0.4, "farm": 0.2},
        threshold=0.5,
        risk_max=0.4,
        color="#66bb6a",
    ),
    TagDefinition(
        id="GLOBAL_VISION_CONTROL",
        label_ko="시야 장악형",
        role_scope="ANY",
        min_games=5,
        weights={"vision": 1.0},
        threshold=0.75,
        color="#5c6bc0",
    ),
    TagDefinition(
        id="GLOBAL_EARLY_PRESSURE",
        label_ko="초반 압박형",
        role_scope="ANY",
        min_games=8,
        weights={"aggro": 0.8, "farm": 0.2},
        threshold=0.8,
        color="#ffb74d",
    ),
    TagDefinition(
        id="GLOBAL_LATE_SCALER",
        label_ko="후반 성장형",
        role_scope="ANY",
        min_games=8,
        weights={"farm": 0.6, "damage": 0.4},
        threshold=0.8,
        color="#26c6da",
    ),
    TagDefinition(
        id="TOP_LANE_BULLY",
        label_ko="라인전 킬러 탑",
        role_scope="TOP",
        min_games=8,
        weights={"aggro": 0.7, "damage": 0.3},
        threshold=0.8,
        risk_max=0.9,
        color="#ff8a65",
    ),
    TagDefinition(
        id="TOP_SCALING",
        label_ko="스케일링 탑",
        role_scope="TOP",
        min_games=8,
        weights={"farm": 0.6, "damage": 0.4},
        threshold=0.75,
        color="#4db6ac",
    ),
    TagDefinition(
        id="JUNGLE_GANKER",
        label_ko="갱킹형 정글",
        role_scope="JUNGLE",
        min_games=8,
        weights={"aggro": 0.8, "damage": 0.2},
        threshold=0.8,
        color="#ffb74d",
    ),
    TagDefinition(
        id="JUNGLE_FARMER",
        label_ko="파밍형 정글",
        role_scope="JUNGLE",
        min_games=8,
        weights={"farm": 0.8, "aggro": -0.2},
        threshold=0.6,
        color="#aed581",
    ),
    TagDefinition(
        id="MID_CARRY",
        label_ko="한타 캐리 미드",
        role_scope="MIDDLE",
        min_games=8,
        weights={"damage": 0.7, "aggro": 0.3},
        threshold=0.8,
        color="#ba68c8",
    ),
    TagDefinition(
        id="MID_SAFE_FARM",
        label_ko="세이프 파밍 미드",
        role_scope="MIDDLE",
        min_games=8,
        weights={"farm": 0.7, "risk": -0.3},
        threshold=0.7,
        color="#81c784",
    ),
    TagDefinition(
        id="BOTTOM_HYPER_CARRY",
        label_ko="스케일링 하이퍼 캐리 원딜",
        role_scope="BOTTOM",
        min_games=8,
        weights={"farm": 0.6, "damage": 0.4},
        threshold=0.8,
        color="#ffca28",
    ),
    TagDefinition(
        id="BOTTOM_LANE_TRADER",
        label_ko="라인전 딜교환형 원딜",
        role_scope="BOTTOM",
        min_games=8,
        weights={"aggro": 0.7, "damage": 0.3},
        threshold=0.75,
        color="#ff8a65",
    ),
    TagDefinition(
        id="SUPPORT_VISION",
        label_ko="시야 장악형 서포터",
        role_scope="UTILITY",
        min_games=8,
        weights={"vision": 1.0},
        threshold=0.8,
        color="#9575cd",
    ),
    TagDefinition(
        id="SUPPORT_SAFE_UTILITY",
        label_ko="유틸 보호형 서포터",
        role_scope="UTILITY",
        min_games=8,
        weights={"risk": -0.5, "vision": 0.3, "winrate": 0.2},
        threshold=0.6,
        color="#4fc3f7",
    ),
]


def evaluate_tags_for_role(matches: List[MatchPerformance], role: str) -> List[Dict[str, str]]:
    if not matches:
        return []
    dims = compute_dimensions(matches)
    games = len(matches)
    results: List[Dict[str, str]] = []
    for definition in TAG_DEFINITIONS:
        if definition.role_scope not in ("ANY", role):
            continue
        if games < definition.min_games:
            continue
        if definition.risk_max is not None and dims.risk > definition.risk_max:
            continue
        score = 0.0
        for key, weight in definition.weights.items():
            value = getattr(dims, key, 0.0)
            score += value * weight
        if score >= definition.threshold:
            results.append({
                "id": definition.id,
                "label_ko": definition.label_ko,
                "color": definition.color,
            })
    return results


def compute_playstyle_tags_for_summoner(db: Session, summoner: Summoner) -> Tuple[List[Dict[str, str]], Optional[str], int]:
    roles = ["TOP", "JUNGLE", "MIDDLE", "BOTTOM", "UTILITY"]
    role_to_matches: Dict[str, List[MatchPerformance]] = {}
    total_games = 0

    for role in roles:
        possible_lanes = ROLE_MAPPINGS.get(role, [role])
        matches = (
            db.query(MatchPerformance)
            .filter(
                MatchPerformance.summoner_id == summoner.id,
                MatchPerformance.lane.in_(possible_lanes),
            )
            .all()
        )
        if not matches:
            continue
        role_to_matches[role] = matches
        total_games += len(matches)

    if not role_to_matches:
        return [], None, 0

    primary_role = max(role_to_matches.items(), key=lambda item: len(item[1]))[0]

    tag_map: Dict[str, Dict[str, Optional[str]]] = {}
    for role, matches in role_to_matches.items():
        tags = evaluate_tags_for_role(matches, role)
        for tag in tags:
            tag_id = tag.get("id")
            if tag_id and tag_id not in tag_map:
                tag_map[tag_id] = {
                    "id": tag_id,
                    "label_ko": tag.get("label_ko", ""),
                    "color": tag.get("color"),
                }

    ordered_tags = list(tag_map.values())
    return ordered_tags, primary_role, total_games


def upsert_playstyle_snapshot(db: Session, summoner: Summoner) -> Tuple[SummonerPlaystyleTag, List[Dict[str, str]], Optional[str], int]:
    tags, primary_role, total_games = compute_playstyle_tags_for_summoner(db, summoner)
    now = datetime.utcnow()

    snapshot = (
        db.query(SummonerPlaystyleTag)
        .filter(SummonerPlaystyleTag.summoner_id == summoner.id)
        .first()
    )
    if snapshot is None:
        snapshot = SummonerPlaystyleTag(
            summoner_id=summoner.id,
            tags=tags,
            primary_role=primary_role,
            games_used=total_games,
            calculated_at=now,
            version=TAG_VERSION,
        )
        db.add(snapshot)
    else:
        snapshot.tags = tags
        snapshot.primary_role = primary_role
        snapshot.games_used = total_games
        snapshot.calculated_at = now
        snapshot.version = TAG_VERSION

    db.commit()
    db.refresh(snapshot)
    return snapshot, tags, primary_role, total_games
