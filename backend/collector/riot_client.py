import requests
import time
import logging
from .config import Config

logger = logging.getLogger(__name__)

class RiotAPIClient:
    def __init__(self):
        self.headers = {
            "X-Riot-Token": Config.RIOT_API_KEY
        }

    def _update_headers(self):
        self.headers["X-Riot-Token"] = Config.RIOT_API_KEY

    def get_summoner_by_name(self, summoner_name):
        self._update_headers()
        url = f"https://{Config.PLATFORM_ROUTING_VALUE}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{summoner_name}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return None

    def get_account_by_riot_id(self, game_name, tag_line):
        self._update_headers()
        url = f"https://{Config.ROUTING_VALUE}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return None

    def get_summoner_by_puuid(self, puuid):
        self._update_headers()
        url = f"https://{Config.PLATFORM_ROUTING_VALUE}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return None

    def get_match_ids(self, puuid, start=0, count=20):
        self._update_headers()
        # queue=440 is Flex Rank
        url = f"https://{Config.ROUTING_VALUE}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
        params = {
            "queue": Config.QUEUE_ID,
            "start": start,
            "count": count
        }
        # Simple retry loop to handle rate limiting (HTTP 429)
        for attempt in range(3):
            logger.info(f"[get_match_ids] puuid={puuid[:12]}..., start={start}, count={count}, attempt={attempt+1}")
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                data = response.json()
                logger.info(f"[get_match_ids] 200 OK puuid={puuid[:12]}..., start={start}, got={len(data)}")
                return data
            if response.status_code == 429:
                # Respect Retry-After header when present
                retry_after = response.headers.get("Retry-After")
                try:
                    delay = int(retry_after) if retry_after is not None else 2
                except ValueError:
                    delay = 2
                logger.warning(f"[get_match_ids] 429 rate limited puuid={puuid[:12]}..., start={start}, retry_after={delay}s")
                time.sleep(delay)
                continue
            logger.error(f"[get_match_ids] HTTP {response.status_code} puuid={puuid[:12]}..., start={start}, body={response.text[:200]}")
            break
        return []

    def get_match_details(self, match_id):
        self._update_headers()
        url = f"https://{Config.ROUTING_VALUE}.api.riotgames.com/lol/match/v5/matches/{match_id}"
        # Simple retry loop to handle rate limiting (HTTP 429)
        for attempt in range(3):
            logger.info(f"[get_match_details] match_id={match_id}, attempt={attempt+1}")
            response = requests.get(url, headers=self.headers)
            if response.status_code == 200:
                logger.info(f"[get_match_details] 200 OK match_id={match_id}")
                return response.json()
            if response.status_code == 429:
                retry_after = response.headers.get("Retry-After")
                try:
                    delay = int(retry_after) if retry_after is not None else 2
                except ValueError:
                    delay = 2
                logger.warning(f"[get_match_details] 429 rate limited match_id={match_id}, retry_after={delay}s")
                time.sleep(delay)
                continue
            logger.error(f"[get_match_details] HTTP {response.status_code} match_id={match_id}, body={response.text[:200]}")
            break
        return None
