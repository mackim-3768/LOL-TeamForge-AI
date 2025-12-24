from abc import ABC, abstractmethod
from typing import List, Dict
from openai import OpenAI
from backend.collector.config import Config

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
        self.client = OpenAI(api_key=api_key)
        self.api_key = api_key

    def analyze_summoner_performance(self, summoner_name: str, role_stats: List[Dict]) -> str:
        prompt = f"Analyze the performance of summoner {summoner_name} based on the following stats:\n{role_stats}\nProvide insights on strengths and weaknesses."
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a League of Legends analyst. Provide concise and insightful analysis."},
                    {"role": "system", "content": "You are a League of Legends coach assistant."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling OpenAI: {str(e)}"

    def recommend_team_composition(self, summoners: List[str], summoner_stats: Dict[str, List[Dict]]) -> str:
        prompt = f"Given the following summoners and their stats, recommend the best team composition (assign roles):\nSummoners: {summoners}\nStats: {summoner_stats}"
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a League of Legends coach. Optimize team composition based on player strengths."},
                    {"role": "system", "content": "You are a League of Legends team strategist."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling OpenAI: {str(e)}"

def get_ai_provider():
    if Config.OPENAI_API_KEY:
        return OpenAIProvider(Config.OPENAI_API_KEY)
    return MockAIProvider()
