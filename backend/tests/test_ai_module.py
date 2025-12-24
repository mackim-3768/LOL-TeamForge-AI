import unittest
from unittest.mock import MagicMock, patch
from backend.core_api.ai_module import OpenAIProvider, get_ai_provider, MockAIProvider
from backend.collector.config import Config

class TestAIModule(unittest.TestCase):
    def setUp(self):
        self.api_key = "test_key"
        self.provider = OpenAIProvider(self.api_key)

    @patch("backend.core_api.ai_module.OpenAI")
    def test_analyze_summoner_performance(self, mock_openai_class):
        # Setup mock response
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Analysis Result"))]
        mock_client.chat.completions.create.return_value = mock_response

        # Initialize provider which calls OpenAI()
        provider = OpenAIProvider(self.api_key)

        stats = [
            {"role": "TOP", "win_rate": 55.0, "kda": 3.5, "avg_gold": 450, "vision_score": 25},
            {"role": "JUNGLE", "win_rate": 45.0, "kda": 2.0, "avg_gold": 350, "vision_score": 30}
        ]

        result = provider.analyze_summoner_performance("TestSummoner", stats)

        self.assertEqual(result, "Analysis Result")
        mock_client.chat.completions.create.assert_called_once()
        args, kwargs = mock_client.chat.completions.create.call_args
        self.assertEqual(kwargs['model'], "gpt-4o")
        self.assertTrue("TestSummoner" in kwargs['messages'][1]['content'])

    @patch("backend.core_api.ai_module.OpenAI")
    def test_recommend_team_composition(self, mock_openai_class):
        # Setup mock response
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Team Comp Recommendation"))]
        mock_client.chat.completions.create.return_value = mock_response

        provider = OpenAIProvider(self.api_key)

        summoners = ["P1", "P2", "P3", "P4", "P5"]
        stats = {
            "P1": [{"role": "TOP", "score": 80, "win_rate": 60}],
            "P2": [{"role": "JUNGLE", "score": 75, "win_rate": 55}],
            "P3": [],
            "P4": [{"role": "BOTTOM", "score": 90, "win_rate": 65}],
            "P5": [{"role": "UTILITY", "score": 85, "win_rate": 58}]
        }

        result = provider.recommend_team_composition(summoners, stats)

        self.assertEqual(result, "Team Comp Recommendation")
        mock_client.chat.completions.create.assert_called_once()
        args, kwargs = mock_client.chat.completions.create.call_args
        self.assertTrue("P1" in kwargs['messages'][1]['content'])
        self.assertTrue("No stats available" in kwargs['messages'][1]['content']) # P3

    def test_get_ai_provider_mock(self):
        Config.OPENAI_API_KEY = ""
        provider = get_ai_provider()
        self.assertIsInstance(provider, MockAIProvider)

    def test_get_ai_provider_openai(self):
        Config.OPENAI_API_KEY = "some_key"
        provider = get_ai_provider()
        self.assertIsInstance(provider, OpenAIProvider)

if __name__ == '__main__':
    unittest.main()
