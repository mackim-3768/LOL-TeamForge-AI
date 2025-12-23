import requests
import time
from .config import Config

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

    def get_match_ids(self, puuid, count=20):
        self._update_headers()
        # queue=440 is Flex Rank
        url = f"https://{Config.ROUTING_VALUE}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids"
        params = {
            "queue": Config.QUEUE_ID,
            "start": 0,
            "count": count
        }
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code == 200:
            return response.json()
        return []

    def get_match_details(self, match_id):
        self._update_headers()
        url = f"https://{Config.ROUTING_VALUE}.api.riotgames.com/lol/match/v5/matches/{match_id}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return None
