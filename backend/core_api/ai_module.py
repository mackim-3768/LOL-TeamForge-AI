from abc import ABC, abstractmethod
from typing import List, Dict
import os
import openai

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
        self.client = openai.OpenAI(api_key=api_key)
        self.api_key = api_key

    def analyze_summoner_performance(self, summoner_name: str, role_stats: List[Dict]) -> str:
        # Construct Prompt
        prompt = f"Analyze the performance of summoner {summoner_name} based on the following stats:\n"
        for stat in role_stats:
            prompt += f"Role: {stat['role']}, Win Rate: {stat['win_rate']}%, KDA: {stat['kda']}, Gold/Min: {stat['avg_gold']}, Vision Score: {stat['vision_score']}\n"
        prompt += "\nProvide a brief summary of their strengths and weaknesses."

        # call openai
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a League of Legends analyst. Provide concise and insightful analysis."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling OpenAI: {str(e)}"

    def recommend_team_composition(self, summoners: List[str], summoner_stats: Dict[str, List[Dict]]) -> str:
        # Construct Context
        prompt = "Recommend the best team composition (lane assignments) for the following summoners based on their stats:\n\n"
        for name, stats in summoner_stats.items():
            prompt += f"Summoner: {name}\n"
            if not stats:
                prompt += "  No stats available.\n"
            for stat in stats:
                prompt += f"  Role: {stat['role']}, Score: {stat['score']}, Win Rate: {stat['win_rate']}%\n"
            prompt += "\n"

        prompt += "Assign each summoner to one unique role (TOP, JUNGLE, MIDDLE, BOTTOM, UTILITY) to maximize the team's winning chance. Explain why."

        # call openai
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a League of Legends coach. Optimize team composition based on player strengths."},
                    {"role": "user", "content": prompt}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error calling OpenAI: {str(e)}"

def get_ai_provider():
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return OpenAIProvider(api_key)
    return MockAIProvider()
