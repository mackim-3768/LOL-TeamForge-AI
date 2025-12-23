from abc import ABC, abstractmethod
from typing import List, Dict

class AIProvider(ABC):
    @abstractmethod
    def analyze_summoner_performance(self, summoner_name: str, role_stats: List[Dict]) -> str:
        """Returns a textual analysis of the summoner's strengths/weaknesses."""
        pass

    @abstractmethod
    def recommend_team_composition(self, summoners: List[str], summoner_stats: Dict[str, List[Dict]]) -> str:
        """Returns a recommendation for lane assignments."""
        pass

class MockAIProvider(AIProvider):
    def analyze_summoner_performance(self, summoner_name: str, role_stats: List[Dict]) -> str:
        return f"[MOCK AI] {summoner_name} shows strong mechanics in Top lane but needs better vision control."

    def recommend_team_composition(self, summoners: List[str], summoner_stats: Dict[str, List[Dict]]) -> str:
        return f"[MOCK AI] Recommended Comp: {summoners[0]} (Top), {summoners[1]} (Jungle), ..."

class OpenAIProvider(AIProvider):
    def __init__(self, api_key: str):
        # self.client = OpenAI(api_key=api_key)
        self.api_key = api_key

    def analyze_summoner_performance(self, summoner_name: str, role_stats: List[Dict]) -> str:
        # Construct Prompt
        # call openai
        return "OpenAI integration not fully active without key."

    def recommend_team_composition(self, summoners: List[str], summoner_stats: Dict[str, List[Dict]]) -> str:
        # Construct Context
        # call openai
        return "OpenAI integration not fully active without key."

def get_ai_provider():
    # Logic to switch based on env or config
    return MockAIProvider()
