import unittest
from datetime import datetime
from backend.core_api.main import _compute_role_scores_for_summoner, ScoreResponse
from backend.shared.database import Summoner, MatchPerformance

# Mock DB Session
class MockSession:
    def __init__(self, query_result):
        self.query_result = query_result

    def query(self, *args):
        return self

    def filter(self, *args, **kwargs):
        return self

    def in_(self, *args):
        return self

    def all(self):
        return self.query_result

class TestRadarMetrics(unittest.TestCase):
    def test_compute_metrics(self):
        summoner = Summoner(id=1, summoner_name="TestSummoner")

        # Create mock matches
        matches = [
            MatchPerformance(
                lane="TOP",
                win=True,
                kda=4.0,
                gold_per_min=400.0,
                vision_score=20,
                total_damage_dealt_to_champions=20000,
                total_minions_killed=200
            ),
            MatchPerformance(
                lane="TOP",
                win=False,
                kda=2.0,
                gold_per_min=300.0,
                vision_score=10,
                total_damage_dealt_to_champions=10000,
                total_minions_killed=100
            )
        ]

        # In the function, it filters by role.
        # For TOP role, it should find these matches.

        # We need to mock the DB session to return these matches when queried
        db = MockSession(matches)

        scores = _compute_role_scores_for_summoner(summoner, db)

        # Find TOP score
        top_score = next((s for s in scores if s.role == "TOP"), None)
        self.assertIsNotNone(top_score)

        # Expected Averages:
        # KDA: (4+2)/2 = 3.0
        # Gold: (400+300)/2 = 350.0
        # Vision: (20+10)/2 = 15.0
        # Damage: (20000+10000)/2 = 15000.0
        # CS: (200+100)/2 = 150.0

        self.assertEqual(top_score.kda, 3.0)
        self.assertEqual(top_score.avg_gold, 350.0)
        self.assertEqual(top_score.vision_score, 15.0)
        self.assertEqual(top_score.avg_damage, 15000.0)
        self.assertEqual(top_score.avg_cs, 150.0)

if __name__ == '__main__':
    unittest.main()
