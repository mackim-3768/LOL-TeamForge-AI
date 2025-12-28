from typing import Dict, List, Tuple

from sqlalchemy.orm import Session

from backend.shared.database import Summoner, MatchPerformance, MatchDetail
from backend.core_api.playstyle_tags import (
    DimensionScores,
    compute_dimensions,
    compute_advanced_dimensions_for_role,
)


def _compute_overall_dimension_scores_for_summoner(
    db: Session,
    summoner: Summoner,
) -> Tuple[DimensionScores, int]:
    matches = (
        db.query(MatchPerformance)
        .filter(MatchPerformance.summoner_id == summoner.id)
        .all()
    )
    games = len(matches)
    if games == 0:
        return DimensionScores(
            aggro=0.0,
            risk=0.0,
            vision=0.0,
            farm=0.0,
            damage=0.0,
            winrate=0.0,
        ), 0

    basic = compute_dimensions(matches)
    adv = compute_advanced_dimensions_for_role(db, summoner, matches)

    dims = DimensionScores(
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
    return dims, games


def _sim_scalar(v1: float, v2: float) -> float:
    avg = (v1 + v2) / 2.0
    diff = abs(v1 - v2)
    score = (1.0 - diff) * avg
    if score < 0.0:
        return 0.0
    if score > 1.0:
        return 1.0
    return score


def _sim_risk(r1: float, r2: float) -> float:
    align = 1.0 - abs(r1 - r2)
    level = 1.0 - (r1 + r2) / 2.0
    if level < 0.0:
        level = 0.0
    score = align * level
    if score < 0.0:
        return 0.0
    if score > 1.0:
        return 1.0
    return score


def compute_style_synergy(
    d1: DimensionScores,
    d2: DimensionScores,
) -> Tuple[float, Dict[str, float]]:
    early = (
        _sim_scalar(d1.earlyAggro, d2.earlyAggro)
        + _sim_scalar(d1.laneLead, d2.laneLead)
        + _sim_scalar(d1.aggro, d2.aggro)
    ) / 3.0

    late = (
        _sim_scalar(d1.lateCarry, d2.lateCarry)
        + _sim_scalar(d1.farmFocus, d2.farmFocus)
        + _sim_scalar(d1.damage, d2.damage)
    ) / 3.0

    vision_obj = (
        _sim_scalar(d1.visionControl, d2.visionControl)
        + _sim_scalar(d1.vision, d2.vision)
        + _sim_scalar(d1.objectiveFocus, d2.objectiveFocus)
    ) / 3.0

    map_pressure = (
        _sim_scalar(d1.roam, d2.roam)
        + _sim_scalar(d1.splitPush, d2.splitPush)
        + _sim_scalar(d1.teamfight, d2.teamfight)
    ) / 3.0

    risk_control = _sim_risk(d1.risk, d2.risk)

    style = (
        0.25 * early
        + 0.25 * late
        + 0.20 * vision_obj
        + 0.20 * map_pressure
        + 0.10 * risk_control
    )
    if style < 0.0:
        style = 0.0
    if style > 1.0:
        style = 1.0

    breakdown = {
        "early_game": early,
        "late_game": late,
        "vision_objective": vision_obj,
        "map_pressure": map_pressure,
        "risk_control": risk_control,
    }

    return style, breakdown


def _get_duo_match_stats(
    db: Session,
    s1: Summoner,
    s2: Summoner,
) -> List[Tuple[MatchPerformance, MatchPerformance, int]]:
    matches1 = (
        db.query(MatchPerformance)
        .filter(MatchPerformance.summoner_id == s1.id)
        .all()
    )
    matches2 = (
        db.query(MatchPerformance)
        .filter(MatchPerformance.summoner_id == s2.id)
        .all()
    )

    by_id1 = {m.match_id: m for m in matches1}
    by_id2 = {m.match_id: m for m in matches2}

    duo: List[Tuple[MatchPerformance, MatchPerformance, int]] = []

    shared_ids = set(by_id1.keys()) & set(by_id2.keys())
    if not shared_ids:
        return duo

    for match_id in shared_ids:
        mp1 = by_id1[match_id]
        mp2 = by_id2[match_id]

        db_match = (
            db.query(MatchDetail)
            .filter(MatchDetail.match_id == match_id)
            .first()
        )
        if not db_match or not db_match.raw:
            continue

        data = db_match.raw or {}
        info = data.get("info", {}) or {}
        participants = info.get("participants", []) or []

        team1 = None
        team2 = None
        for p in participants:
            puuid = p.get("puuid")
            if puuid == s1.puuid:
                team1 = p.get("teamId")
            elif puuid == s2.puuid:
                team2 = p.get("teamId")

        if team1 is None or team2 is None:
            continue
        if team1 != team2:
            continue

        team_kills = 0
        for p in participants:
            if p.get("teamId") == team1:
                team_kills += int(p.get("kills", 0))

        duo.append((mp1, mp2, team_kills))

    return duo


def compute_duo_performance(
    duo_matches: List[Tuple[MatchPerformance, MatchPerformance, int]],
) -> Tuple[float, int]:
    games = len(duo_matches)
    if games == 0:
        return 0.0, 0

    wins = 0
    kda_values: List[float] = []
    kp_values: List[float] = []

    for mp1, mp2, team_kills in duo_matches:
        if mp1.win and mp2.win:
            wins += 1

        deaths_sum = (mp1.deaths or 0) + (mp2.deaths or 0)
        kills_sum = (mp1.kills or 0) + (mp2.kills or 0)
        assists_sum = (mp1.assists or 0) + (mp2.assists or 0)

        kda = (kills_sum + assists_sum) / max(1, deaths_sum)
        kda_values.append(kda)

        if team_kills > 0:
            kp = (kills_sum + assists_sum) / float(team_kills)
            kp_values.append(kp)

    winrate_duo = wins / float(games)
    winrate_score = min(1.0, winrate_duo / 0.65) if games > 0 else 0.0

    avg_kda = sum(kda_values) / len(kda_values) if kda_values else 0.0
    kda_score = min(1.0, avg_kda / 6.0) if avg_kda > 0 else 0.0

    if kp_values:
        avg_kp = sum(kp_values) / len(kp_values)
        kp_score = min(1.0, avg_kp / 0.9)
    else:
        kp_score = 0.0

    core = 0.5 * winrate_score + 0.3 * kda_score + 0.2 * kp_score
    sample_factor = min(1.0, games / 20.0)
    perf = core * sample_factor
    if perf < 0.0:
        perf = 0.0
    if perf > 1.0:
        perf = 1.0

    return perf, games


def compute_duo_synergy(
    db: Session,
    summoner1: Summoner,
    summoner2: Summoner,
) -> Dict[str, object]:
    dims1, games1 = _compute_overall_dimension_scores_for_summoner(db, summoner1)
    dims2, games2 = _compute_overall_dimension_scores_for_summoner(db, summoner2)

    style_score, breakdown = compute_style_synergy(dims1, dims2)

    duo_matches = _get_duo_match_stats(db, summoner1, summoner2)
    perf_score, duo_games = compute_duo_performance(duo_matches)

    total = 0.6 * style_score + 0.4 * perf_score
    total_int = int(round(total * 100.0))
    if total_int < 0:
        total_int = 0
    if total_int > 100:
        total_int = 100

    return {
        "style_score": style_score,
        "performance_score": perf_score,
        "synergy_score": total_int,
        "games_together": duo_games,
        "style_breakdown": breakdown,
        "summoner1_games": games1,
        "summoner2_games": games2,
    }
