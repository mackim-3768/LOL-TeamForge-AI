from typing import Dict, List, Optional, Tuple
from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.orm import Session
from backend.shared.database import Summoner, MatchPerformance, MatchDetail, SummonerPlaystyleTag

TAG_VERSION = "v1"


class DimensionScores(BaseModel):
    aggro: float
    risk: float
    vision: float
    farm: float
    damage: float
    winrate: float
    earlyAggro: float = 0.0
    lateCarry: float = 0.0
    laneLead: float = 0.0
    objectiveFocus: float = 0.0
    teamfight: float = 0.0
    roam: float = 0.0
    splitPush: float = 0.0
    farmFocus: float = 0.0
    visionControl: float = 0.0


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


def _extract_participant(raw: dict, puuid: str) -> Optional[dict]:
    info = raw.get("info", {}) or {}
    participants = info.get("participants", []) or []
    for p in participants:
        if p.get("puuid") == puuid:
            return p
    return None


def _compute_advanced_dimensions_for_match(raw: dict, participant: dict) -> Dict[str, float]:
    info = raw.get("info", {}) or {}
    challenges = participant.get("challenges", {}) or {}

    time_played = float(participant.get("timePlayed") or info.get("gameDuration") or 0.0)
    if time_played <= 0:
        time_played = 1.0
    time_min = max(1.0, time_played / 60.0)

    kills = int(participant.get("kills", 0))
    deaths = int(participant.get("deaths", 0))
    assists = int(participant.get("assists", 0))

    # early aggro
    early_takedowns = float(challenges.get("takedownsFirstXMinutes", 0.0))
    early_solos = float(challenges.get("soloKills", 0.0))
    norm_early_takedowns = min(1.0, early_takedowns / 6.0)
    norm_early_solos = min(1.0, early_solos / 3.0)
    early_aggro = 0.4 * norm_early_takedowns + 0.6 * norm_early_solos

    # late carry (DPM + team damage share)
    dpm = float(challenges.get("damagePerMinute", 0.0))
    team_share = float(challenges.get("teamDamagePercentage", 0.0))
    norm_dpm = min(1.0, dpm / 800.0)
    norm_share = min(1.0, team_share / 0.35) if team_share > 0 else 0.0
    late_carry = 0.5 * norm_dpm + 0.5 * norm_share

    # lane lead (CS/골드 우위 근사)
    cs10 = float(challenges.get("laneMinionsFirst10Minutes", 0.0))
    cs_adv = float(challenges.get("maxCsAdvantageOnLaneOpponent", 0.0))
    lane_gold_adv = float(challenges.get("laningPhaseGoldExpAdvantage", 0.0))
    norm_cs10 = min(1.0, cs10 / 80.0)
    norm_cs_adv = min(1.0, max(0.0, cs_adv) / 30.0)
    norm_gold = min(1.0, max(0.0, lane_gold_adv) / 800.0)
    lane_lead = 0.4 * norm_cs10 + 0.3 * norm_cs_adv + 0.3 * norm_gold

    # vision control (시야)
    vs_pm = float(challenges.get("visionScorePerMinute", 0.0))
    ctrl = float(challenges.get("controlWardsPlaced", 0.0))
    ward_kills = float(challenges.get("wardTakedowns", 0.0))
    norm_vs = min(1.0, vs_pm / 1.5)
    norm_ctrl = min(1.0, ctrl / 5.0)
    norm_wk = min(1.0, ward_kills / 6.0)
    vision_control = 0.4 * norm_vs + 0.3 * norm_ctrl + 0.3 * norm_wk

    # objective focus
    drag = float(participant.get("dragonKills", 0.0))
    herald = float(participant.get("riftHeraldTakedowns", 0.0))
    baron = float(participant.get("baronKills", 0.0))
    obj_dmg = float(participant.get("damageDealtToObjectives", 0.0))
    turret_takedowns = float(challenges.get("turretTakedowns", 0.0))
    plates = float(challenges.get("turretPlatesTaken", 0.0))
    norm_obj_kills = min(1.0, (drag + herald + baron) / 4.0)
    norm_obj_dmg = min(1.0, obj_dmg / 20000.0)
    norm_turret = min(1.0, (turret_takedowns + plates / 2.0) / 4.0)
    objective_focus = 0.5 * norm_obj_kills + 0.3 * norm_obj_dmg + 0.2 * norm_turret

    # teamfight (킬관여 + 팀딜 비중)
    kp = float(challenges.get("killParticipation", 0.0))
    norm_kp = min(1.0, kp / 0.7) if kp > 0 else 0.0
    teamfight = 0.6 * norm_kp + 0.4 * norm_share

    # roam (TP/라인 이동)
    tp_tks = float(challenges.get("teleportTakedowns", 0.0))
    crosslane = float(challenges.get("killsOnOtherLanesEarlyJungleAsLaner", 0.0))
    alllanes = float(challenges.get("getTakedownsInAllLanesEarlyJungleAsLaner", 0.0))
    norm_tp = min(1.0, tp_tks / 3.0)
    norm_cross = min(1.0, crosslane / 3.0)
    norm_all = min(1.0, alllanes / 3.0)
    roam = 0.5 * norm_tp + 0.3 * norm_cross + 0.2 * norm_all

    # split push (타워/플레이트)
    tower_dmg = float(participant.get("damageDealtToBuildings", 0.0))
    norm_tower_dmg = min(1.0, tower_dmg / 15000.0)
    split_push = 0.6 * norm_tower_dmg + 0.4 * norm_turret

    # farm focus (CS/분 + GPM)
    cs = float(participant.get("totalMinionsKilled", 0.0)) + float(participant.get("neutralMinionsKilled", 0.0))
    cs_per_min = cs / time_min
    gpm = float(challenges.get("goldPerMinute", 0.0)) or float(info.get("gameLength", 0.0) and (participant.get("goldEarned", 0.0) / time_min))
    norm_cs = min(1.0, cs_per_min / 9.0)
    norm_gpm = min(1.0, gpm / 500.0) if gpm else 0.0
    farm_focus = 0.7 * norm_cs + 0.3 * norm_gpm

    return {
        "earlyAggro": early_aggro,
        "lateCarry": late_carry,
        "laneLead": lane_lead,
        "objectiveFocus": objective_focus,
        "teamfight": teamfight,
        "roam": roam,
        "splitPush": split_push,
        "farmFocus": farm_focus,
        "visionControl": vision_control,
    }


def compute_advanced_dimensions_for_role(
    db: Session,
    summoner: Summoner,
    matches: List[MatchPerformance],
) -> Dict[str, float]:
    if not matches:
        return {
            "earlyAggro": 0.0,
            "lateCarry": 0.0,
            "laneLead": 0.0,
            "objectiveFocus": 0.0,
            "teamfight": 0.0,
            "roam": 0.0,
            "splitPush": 0.0,
            "farmFocus": 0.0,
            "visionControl": 0.0,
        }

    sums = {
        "earlyAggro": 0.0,
        "lateCarry": 0.0,
        "laneLead": 0.0,
        "objectiveFocus": 0.0,
        "teamfight": 0.0,
        "roam": 0.0,
        "splitPush": 0.0,
        "farmFocus": 0.0,
        "visionControl": 0.0,
    }
    count = 0

    for mp in matches:
        db_match = db.query(MatchDetail).filter(MatchDetail.match_id == mp.match_id).first()
        if not db_match or not db_match.raw:
            continue
        participant = _extract_participant(db_match.raw, summoner.puuid)
        if not participant:
            continue
        adv = _compute_advanced_dimensions_for_match(db_match.raw, participant)
        for k in sums.keys():
            sums[k] += adv.get(k, 0.0)
        count += 1

    if count <= 0:
        return {k: 0.0 for k in sums.keys()}

    return {k: v / float(count) for k, v in sums.items()}


def compute_dimension_scores_for_role(
    db: Session,
    summoner: Summoner,
    matches: List[MatchPerformance],
) -> DimensionScores:
    basic = compute_dimensions(matches)
    adv = compute_advanced_dimensions_for_role(db, summoner, matches)
    return DimensionScores(
        aggro=basic.aggro,
        risk=basic.risk,
        vision=basic.vision,
        farm=basic.farm,
        damage=basic.damage,
        winrate=basic.winrate,
        earlyAggro=adv["earlyAggro"],
        lateCarry=adv["lateCarry"],
        laneLead=adv["laneLead"],
        objectiveFocus=adv["objectiveFocus"],
        teamfight=adv["teamfight"],
        roam=adv["roam"],
        splitPush=adv["splitPush"],
        farmFocus=adv["farmFocus"],
        visionControl=adv["visionControl"],
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


def evaluate_tags_for_role(dims: DimensionScores, games: int, role: str) -> List[Dict[str, str]]:
    if games <= 0:
        return []
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
        dims = compute_dimension_scores_for_role(db, summoner, matches)
        tags = evaluate_tags_for_role(dims, len(matches), role)
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
