from datetime import datetime

class DataProcessor:
    @staticmethod
    def extract_performance(match_data, puuid):
        """
        Extracts stats for the specific summoner from the match detail JSON.
        Returns a dictionary suitable for MatchPerformance model.
        """
        info = match_data.get("info", {})
        participants = info.get("participants", [])
        
        target_participant = None
        for p in participants:
            if p.get("puuid") == puuid:
                target_participant = p
                break
        
        if not target_participant:
            return None

        # Map role/lane
        lane = target_participant.get("lane", "")
        role = target_participant.get("role", "")
        team_position = target_participant.get("teamPosition", "") # TOP, JUNGLE, MIDDLE, BOTTOM, UTILITY
        
        # Calculate KDA
        kills = target_participant.get("kills", 0)
        deaths = target_participant.get("deaths", 0)
        assists = target_participant.get("assists", 0)
        kda = (kills + assists) / max(1, deaths)

        # Gold per min
        game_duration_sec = info.get("gameDuration", 1)
        gold_earned = target_participant.get("goldEarned", 0)
        gold_per_min = (gold_earned / game_duration_sec) * 60

        return {
            "match_id": match_data.get("metadata", {}).get("matchId"),
            "game_creation": datetime.fromtimestamp(info.get("gameCreation", 0) / 1000),
            "lane": team_position if team_position else lane, # Prefer teamPosition
            "role": role,
            "champion_name": target_participant.get("championName"),
            "win": target_participant.get("win"),
            "kills": kills,
            "deaths": deaths,
            "assists": assists,
            "kda": kda,
            "gold_per_min": gold_per_min,
            "vision_score": target_participant.get("visionScore", 0),
            "total_minions_killed": target_participant.get("totalMinionsKilled", 0) + target_participant.get("neutralMinionsKilled", 0),
            "total_damage_dealt_to_champions": target_participant.get("totalDamageDealtToChampions", 0)
        }
