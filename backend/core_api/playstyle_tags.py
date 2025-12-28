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
    # Global axes: Early pressure
    TagDefinition(
        id="GLOBAL_EARLY_PRESSURE_EXTREME",
        label_ko="극단적 초반 압박형",
        role_scope="ANY",
        min_games=10,
        weights={"earlyAggro": 0.5, "laneLead": 0.3, "aggro": 0.2},
        threshold=0.8,
        color="#ff7043",
    ),
    TagDefinition(
        id="GLOBAL_EARLY_PRESSURE_CORE",
        label_ko="초반 주도형",
        role_scope="ANY",
        min_games=10,
        weights={"earlyAggro": 0.5, "laneLead": 0.3, "aggro": 0.2},
        threshold=0.7,
        color="#ffa726",
    ),
    TagDefinition(
        id="GLOBAL_EARLY_PRESSURE_TENDENCY",
        label_ko="초반 압박 성향",
        role_scope="ANY",
        min_games=10,
        weights={"earlyAggro": 0.5, "laneLead": 0.3, "aggro": 0.2},
        threshold=0.6,
        color="#ffcc80",
    ),

    # Global axes: Late-game carry
    TagDefinition(
        id="GLOBAL_LATE_SCALER_EXTREME",
        label_ko="극단적 후반 캐리형",
        role_scope="ANY",
        min_games=10,
        weights={"lateCarry": 0.5, "farmFocus": 0.3, "damage": 0.2},
        threshold=0.8,
        color="#ffca28",
    ),
    TagDefinition(
        id="GLOBAL_LATE_SCALER_CORE",
        label_ko="후반 성장형",
        role_scope="ANY",
        min_games=10,
        weights={"lateCarry": 0.5, "farmFocus": 0.3, "damage": 0.2},
        threshold=0.7,
        color="#ffd54f",
    ),
    TagDefinition(
        id="GLOBAL_LATE_SCALER_TENDENCY",
        label_ko="후반 지향 성향",
        role_scope="ANY",
        min_games=10,
        weights={"lateCarry": 0.5, "farmFocus": 0.3, "damage": 0.2},
        threshold=0.6,
        color="#ffe082",
    ),

    # Global axes: Vision control
    TagDefinition(
        id="GLOBAL_VISION_COMMANDER",
        label_ko="시야 사령관",
        role_scope="ANY",
        min_games=10,
        weights={"visionControl": 0.7, "vision": 0.3},
        threshold=0.8,
        color="#5c6bc0",
    ),
    TagDefinition(
        id="GLOBAL_VISION_CONTROL",
        label_ko="시야 장악형",
        role_scope="ANY",
        min_games=10,
        weights={"visionControl": 0.7, "vision": 0.3},
        threshold=0.7,
        color="#7986cb",
    ),
    TagDefinition(
        id="GLOBAL_VISION_TENDENCY",
        label_ko="시야 의식 성향",
        role_scope="ANY",
        min_games=10,
        weights={"visionControl": 0.7, "vision": 0.3},
        threshold=0.6,
        color="#9fa8da",
    ),

    # Global axes: Objective focus
    TagDefinition(
        id="GLOBAL_OBJECTIVE_CAPTAIN",
        label_ko="오브젝트 사령관",
        role_scope="ANY",
        min_games=10,
        weights={"objectiveFocus": 0.6, "teamfight": 0.2, "visionControl": 0.2},
        threshold=0.8,
        color="#26a69a",
    ),
    TagDefinition(
        id="GLOBAL_OBJECTIVE_FOCUSED",
        label_ko="오브젝트 집중형",
        role_scope="ANY",
        min_games=10,
        weights={"objectiveFocus": 0.6, "teamfight": 0.2, "visionControl": 0.2},
        threshold=0.7,
        color="#4db6ac",
    ),
    TagDefinition(
        id="GLOBAL_OBJECTIVE_TENDENCY",
        label_ko="오브젝트 관여 성향",
        role_scope="ANY",
        min_games=10,
        weights={"objectiveFocus": 0.6, "teamfight": 0.2, "visionControl": 0.2},
        threshold=0.6,
        color="#80cbc4",
    ),

    # Global axes: Map pressure (roam + split push)
    TagDefinition(
        id="GLOBAL_PLAYMAKER",
        label_ko="글로벌 플레이메이커",
        role_scope="ANY",
        min_games=10,
        weights={"roam": 0.4, "splitPush": 0.3, "teamfight": 0.3},
        threshold=0.8,
        color="#ab47bc",
    ),
    TagDefinition(
        id="GLOBAL_MAP_PRESSURE",
        label_ko="맵 압박형",
        role_scope="ANY",
        min_games=10,
        weights={"roam": 0.4, "splitPush": 0.3, "teamfight": 0.3},
        threshold=0.7,
        color="#ba68c8",
    ),
    TagDefinition(
        id="GLOBAL_MAP_TENDENCY",
        label_ko="맵 장악 성향",
        role_scope="ANY",
        min_games=10,
        weights={"roam": 0.4, "splitPush": 0.3, "teamfight": 0.3},
        threshold=0.6,
        color="#ce93d8",
    ),

    # TOP role tags (10)
    TagDefinition(
        id="TOP_LANE_BULLY",
        label_ko="라인전 킬러 탑",
        role_scope="TOP",
        min_games=8,
        weights={"earlyAggro": 0.4, "laneLead": 0.4, "aggro": 0.2},
        threshold=0.75,
        color="#ff8a65",
    ),
    TagDefinition(
        id="TOP_FRONTLINE_TANK",
        label_ko="전면 이니시 탱커",
        role_scope="TOP",
        min_games=8,
        weights={"teamfight": 0.5, "objectiveFocus": 0.3, "risk": 0.2},
        threshold=0.7,
        color="#8d6e63",
    ),
    TagDefinition(
        id="TOP_SPLIT_PUSHER",
        label_ko="사이드 스플릿 탑",
        role_scope="TOP",
        min_games=8,
        weights={"splitPush": 0.6, "objectiveFocus": 0.4},
        threshold=0.7,
        color="#f57c00",
    ),
    TagDefinition(
        id="TOP_SCALING_FIGHTER",
        label_ko="후반 파이터 탑",
        role_scope="TOP",
        min_games=8,
        weights={"lateCarry": 0.5, "teamfight": 0.3, "farmFocus": 0.2},
        threshold=0.7,
        color="#ffb74d",
    ),
    TagDefinition(
        id="TOP_ISLAND_FARMER",
        label_ko="섬 파밍형 탑",
        role_scope="TOP",
        min_games=8,
        weights={"farmFocus": 0.6, "lateCarry": 0.2, "roam": -0.2},
        threshold=0.6,
        risk_max=0.7,
        color="#a1887f",
    ),
    TagDefinition(
        id="TOP_ROAMING_FIGHTER",
        label_ko="로밍 파이터 탑",
        role_scope="TOP",
        min_games=8,
        weights={"roam": 0.4, "earlyAggro": 0.3, "teamfight": 0.3},
        threshold=0.7,
        color="#f06292",
    ),
    TagDefinition(
        id="TOP_COUNTER_DUELLER",
        label_ko="카운터 듀얼러 탑",
        role_scope="TOP",
        min_games=8,
        weights={"laneLead": 0.4, "damage": 0.3, "earlyAggro": 0.3},
        threshold=0.7,
        color="#ff7043",
    ),
    TagDefinition(
        id="TOP_SAFE_SCALER",
        label_ko="안정 성장형 탑",
        role_scope="TOP",
        min_games=8,
        weights={"farmFocus": 0.4, "lateCarry": 0.3, "risk": -0.3},
        threshold=0.65,
        risk_max=0.5,
        color="#81c784",
    ),
    TagDefinition(
        id="TOP_SKIRMISHER",
        label_ko="난전형 싸움꾼 탑",
        role_scope="TOP",
        min_games=8,
        weights={"teamfight": 0.4, "earlyAggro": 0.3, "objectiveFocus": 0.3},
        threshold=0.7,
        color="#e57373",
    ),
    TagDefinition(
        id="TOP_UTILITY_TANK",
        label_ko="유틸 탱커 탑",
        role_scope="TOP",
        min_games=8,
        weights={"visionControl": 0.3, "objectiveFocus": 0.4, "teamfight": 0.3},
        threshold=0.65,
        color="#64b5f6",
    ),

    # JUNGLE role tags (10)
    TagDefinition(
        id="JUNGLE_EARLY_GANKER",
        label_ko="초반 갱킹형 정글",
        role_scope="JUNGLE",
        min_games=8,
        weights={"earlyAggro": 0.4, "roam": 0.4, "aggro": 0.2},
        threshold=0.75,
        color="#ffb74d",
    ),
    TagDefinition(
        id="JUNGLE_FARMER",
        label_ko="파밍형 정글",
        role_scope="JUNGLE",
        min_games=8,
        weights={"farmFocus": 0.6, "lateCarry": 0.3, "earlyAggro": -0.1},
        threshold=0.65,
        color="#aed581",
    ),
    TagDefinition(
        id="JUNGLE_OBJECTIVE_CONTROLLER",
        label_ko="오브젝트 컨트롤 정글",
        role_scope="JUNGLE",
        min_games=8,
        weights={"objectiveFocus": 0.6, "visionControl": 0.2, "teamfight": 0.2},
        threshold=0.7,
        color="#26a69a",
    ),
    TagDefinition(
        id="JUNGLE_PATHING_MACRO",
        label_ko="동선 설계형 정글",
        role_scope="JUNGLE",
        min_games=8,
        weights={"roam": 0.3, "objectiveFocus": 0.3, "visionControl": 0.4},
        threshold=0.7,
        color="#4db6ac",
    ),
    TagDefinition(
        id="JUNGLE_INVADER",
        label_ko="침투형 정글",
        role_scope="JUNGLE",
        min_games=8,
        weights={"earlyAggro": 0.4, "aggro": 0.3, "roam": 0.3},
        threshold=0.7,
        color="#ff8a65",
    ),
    TagDefinition(
        id="JUNGLE_TANK_UTILITY",
        label_ko="유틸 탱커 정글",
        role_scope="JUNGLE",
        min_games=8,
        weights={"teamfight": 0.4, "objectiveFocus": 0.3, "risk": 0.3},
        threshold=0.65,
        color="#81d4fa",
    ),
    TagDefinition(
        id="JUNGLE_ASSASSIN",
        label_ko="암살형 정글",
        role_scope="JUNGLE",
        min_games=8,
        weights={"earlyAggro": 0.4, "damage": 0.3, "risk": 0.3},
        threshold=0.7,
        color="#f06292",
    ),
    TagDefinition(
        id="JUNGLE_VISION",
        label_ko="시야 운영형 정글",
        role_scope="JUNGLE",
        min_games=8,
        weights={"visionControl": 0.6, "objectiveFocus": 0.2, "teamfight": 0.2},
        threshold=0.7,
        color="#9575cd",
    ),
    TagDefinition(
        id="JUNGLE_SUPPORTIVE",
        label_ko="라인 케어형 정글",
        role_scope="JUNGLE",
        min_games=8,
        weights={"roam": 0.4, "teamfight": 0.3, "visionControl": 0.3},
        threshold=0.65,
        color="#64b5f6",
    ),
    TagDefinition(
        id="JUNGLE_CLEANUP_CARRY",
        label_ko="한타 마무리형 정글",
        role_scope="JUNGLE",
        min_games=8,
        weights={"teamfight": 0.5, "lateCarry": 0.3, "aggro": 0.2},
        threshold=0.7,
        color="#ba68c8",
    ),

    # MIDDLE role tags (10)
    TagDefinition(
        id="MID_LANE_BULLY",
        label_ko="라인전 킬러 미드",
        role_scope="MIDDLE",
        min_games=8,
        weights={"earlyAggro": 0.4, "laneLead": 0.4, "aggro": 0.2},
        threshold=0.75,
        color="#ff8a65",
    ),
    TagDefinition(
        id="MID_ROAMING_MAGE",
        label_ko="로밍형 미드",
        role_scope="MIDDLE",
        min_games=8,
        weights={"roam": 0.5, "earlyAggro": 0.2, "teamfight": 0.3},
        threshold=0.7,
        color="#f06292",
    ),
    TagDefinition(
        id="MID_CONTROL_MAGE",
        label_ko="컨트롤 메이지형 미드",
        role_scope="MIDDLE",
        min_games=8,
        weights={"teamfight": 0.4, "visionControl": 0.3, "objectiveFocus": 0.3},
        threshold=0.7,
        color="#7986cb",
    ),
    TagDefinition(
        id="MID_ASSASSIN",
        label_ko="암살형 미드",
        role_scope="MIDDLE",
        min_games=8,
        weights={"earlyAggro": 0.4, "damage": 0.4, "risk": 0.2},
        threshold=0.75,
        color="#e57373",
    ),
    TagDefinition(
        id="MID_LATE_SCALER",
        label_ko="후반 캐리형 미드",
        role_scope="MIDDLE",
        min_games=8,
        weights={"lateCarry": 0.5, "farmFocus": 0.3, "teamfight": 0.2},
        threshold=0.7,
        color="#ffca28",
    ),
    TagDefinition(
        id="MID_UTILITY_SUPPORT",
        label_ko="유틸 서포팅 미드",
        role_scope="MIDDLE",
        min_games=8,
        weights={"visionControl": 0.4, "roam": 0.3, "teamfight": 0.3},
        threshold=0.65,
        color="#4dd0e1",
    ),
    TagDefinition(
        id="MID_POKE",
        label_ko="포킹형 미드",
        role_scope="MIDDLE",
        min_games=8,
        weights={"damage": 0.5, "risk": -0.3, "visionControl": 0.2},
        threshold=0.65,
        risk_max=0.7,
        color="#ba68c8",
    ),
    TagDefinition(
        id="MID_PUSH_AND_ROAM",
        label_ko="푸시 후 로밍형 미드",
        role_scope="MIDDLE",
        min_games=8,
        weights={"splitPush": 0.4, "roam": 0.4, "objectiveFocus": 0.2},
        threshold=0.7,
        color="#f48fb1",
    ),
    TagDefinition(
        id="MID_SAFE_FARMER",
        label_ko="세이프 파밍 미드",
        role_scope="MIDDLE",
        min_games=8,
        weights={"farmFocus": 0.5, "lateCarry": 0.2, "risk": -0.3},
        threshold=0.65,
        risk_max=0.5,
        color="#81c784",
    ),
    TagDefinition(
        id="MID_SKIRMISHER",
        label_ko="난전형 미드",
        role_scope="MIDDLE",
        min_games=8,
        weights={"teamfight": 0.4, "earlyAggro": 0.3, "objectiveFocus": 0.3},
        threshold=0.7,
        color="#ffb74d",
    ),

    # BOTTOM role tags (10)
    TagDefinition(
        id="BOTTOM_HYPER_CARRY",
        label_ko="하이퍼 캐리 원딜",
        role_scope="BOTTOM",
        min_games=8,
        weights={"lateCarry": 0.5, "farmFocus": 0.3, "teamfight": 0.2},
        threshold=0.75,
        color="#ffca28",
    ),
    TagDefinition(
        id="BOTTOM_LANE_DUELLER",
        label_ko="라인전 딜교환형 원딜",
        role_scope="BOTTOM",
        min_games=8,
        weights={"laneLead": 0.4, "earlyAggro": 0.4, "aggro": 0.2},
        threshold=0.75,
        color="#ffb74d",
    ),
    TagDefinition(
        id="BOTTOM_SAFE_DPS",
        label_ko="안전 딜링형 원딜",
        role_scope="BOTTOM",
        min_games=8,
        weights={"farmFocus": 0.4, "lateCarry": 0.3, "risk": -0.3},
        threshold=0.65,
        risk_max=0.5,
        color="#81c784",
    ),
    TagDefinition(
        id="BOTTOM_SIEGE",
        label_ko="포탑 압박형 원딜",
        role_scope="BOTTOM",
        min_games=8,
        weights={"splitPush": 0.5, "objectiveFocus": 0.3, "damage": 0.2},
        threshold=0.7,
        color="#ff8a65",
    ),
    TagDefinition(
        id="BOTTOM_TEAMFIGHT_CARRY",
        label_ko="한타 캐리형 원딜",
        role_scope="BOTTOM",
        min_games=8,
        weights={"teamfight": 0.5, "lateCarry": 0.3, "damage": 0.2},
        threshold=0.7,
        color="#fdd835",
    ),
    TagDefinition(
        id="BOTTOM_POKE",
        label_ko="포킹형 원딜",
        role_scope="BOTTOM",
        min_games=8,
        weights={"damage": 0.5, "risk": -0.3, "laneLead": 0.2},
        threshold=0.65,
        risk_max=0.7,
        color="#ffb300",
    ),
    TagDefinition(
        id="BOTTOM_EARLY_SNOWBALL",
        label_ko="초반 스노우볼형 원딜",
        role_scope="BOTTOM",
        min_games=8,
        weights={"earlyAggro": 0.5, "laneLead": 0.3, "damage": 0.2},
        threshold=0.75,
        color="#ff7043",
    ),
    TagDefinition(
        id="BOTTOM_SPLIT_PUSH_MARKSMAN",
        label_ko="사이드 운영형 원딜",
        role_scope="BOTTOM",
        min_games=8,
        weights={"splitPush": 0.5, "farmFocus": 0.3, "objectiveFocus": 0.2},
        threshold=0.7,
        color="#ffb74d",
    ),
    TagDefinition(
        id="BOTTOM_KITE_DPS",
        label_ko="카이팅 딜러형 원딜",
        role_scope="BOTTOM",
        min_games=8,
        weights={"damage": 0.4, "teamfight": 0.3, "risk": -0.3},
        threshold=0.7,
        risk_max=0.6,
        color="#fbc02d",
    ),
    TagDefinition(
        id="BOTTOM_UTILITY_MARKSMAN",
        label_ko="유틸리티형 원딜",
        role_scope="BOTTOM",
        min_games=8,
        weights={"visionControl": 0.3, "teamfight": 0.3, "objectiveFocus": 0.4},
        threshold=0.65,
        color="#64b5f6",
    ),

    # UTILITY role tags (10)
    TagDefinition(
        id="SUPPORT_VISION",
        label_ko="시야 장악형 서포터",
        role_scope="UTILITY",
        min_games=8,
        weights={"visionControl": 0.7, "vision": 0.3},
        threshold=0.75,
        color="#5c6bc0",
    ),
    TagDefinition(
        id="SUPPORT_ENCHANTER",
        label_ko="보호형 인챈터 서포터",
        role_scope="UTILITY",
        min_games=8,
        weights={"teamfight": 0.4, "visionControl": 0.3, "risk": -0.3},
        threshold=0.7,
        risk_max=0.6,
        color="#4dd0e1",
    ),
    TagDefinition(
        id="SUPPORT_TANK_INITIATOR",
        label_ko="이니시 탱커 서포터",
        role_scope="UTILITY",
        min_games=8,
        weights={"teamfight": 0.5, "objectiveFocus": 0.3, "earlyAggro": 0.2},
        threshold=0.7,
        color="#7986cb",
    ),
    TagDefinition(
        id="SUPPORT_ROAMER",
        label_ko="로밍형 서포터",
        role_scope="UTILITY",
        min_games=8,
        weights={"roam": 0.5, "visionControl": 0.3, "objectiveFocus": 0.2},
        threshold=0.7,
        color="#f48fb1",
    ),
    TagDefinition(
        id="SUPPORT_POKE",
        label_ko="포킹형 서포터",
        role_scope="UTILITY",
        min_games=8,
        weights={"damage": 0.4, "visionControl": 0.3, "risk": -0.3},
        threshold=0.65,
        risk_max=0.7,
        color="#ba68c8",
    ),
    TagDefinition(
        id="SUPPORT_PEELER",
        label_ko="보호형 서포터",
        role_scope="UTILITY",
        min_games=8,
        weights={"teamfight": 0.4, "visionControl": 0.3, "risk": -0.3},
        threshold=0.65,
        risk_max=0.6,
        color="#4fc3f7",
    ),
    TagDefinition(
        id="SUPPORT_ALL_IN",
        label_ko="올인 교전형 서포터",
        role_scope="UTILITY",
        min_games=8,
        weights={"earlyAggro": 0.4, "teamfight": 0.4, "risk": 0.2},
        threshold=0.7,
        color="#ef5350",
    ),
    TagDefinition(
        id="SUPPORT_ROAM_OBJECTIVE",
        label_ko="로밍 오브젝트형 서포터",
        role_scope="UTILITY",
        min_games=8,
        weights={"roam": 0.4, "objectiveFocus": 0.4, "visionControl": 0.2},
        threshold=0.7,
        color="#4db6ac",
    ),
    TagDefinition(
        id="SUPPORT_MACRO",
        label_ko="매크로 운영형 서포터",
        role_scope="UTILITY",
        min_games=8,
        weights={"visionControl": 0.4, "objectiveFocus": 0.3, "roam": 0.3},
        threshold=0.7,
        color="#81d4fa",
    ),
    TagDefinition(
        id="SUPPORT_SNOWBALL",
        label_ko="라인전 스노우볼 서포터",
        role_scope="UTILITY",
        min_games=8,
        weights={"earlyAggro": 0.4, "laneLead": 0.3, "roam": 0.3},
        threshold=0.7,
        color="#ffb74d",
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
