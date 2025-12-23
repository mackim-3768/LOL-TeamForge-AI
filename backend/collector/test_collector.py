import unittest
from unittest.mock import MagicMock, patch
from backend.collector.collector_service import CollectorService
from backend.collector.mock_data import MOCK_SUMMONER, MOCK_MATCH_IDS, MOCK_MATCH_DETAIL
from backend.shared.database import SessionLocal, Summoner, MatchPerformance, Base, engine

class TestCollectorService(unittest.TestCase):
    def setUp(self):
        # Reset DB
        Base.metadata.drop_all(bind=engine)
        Base.metadata.create_all(bind=engine)
        self.service = CollectorService()

    @patch('backend.collector.riot_client.RiotAPIClient.get_summoner_by_name')
    @patch('backend.collector.riot_client.RiotAPIClient.get_match_ids')
    @patch('backend.collector.riot_client.RiotAPIClient.get_match_details')
    def test_add_and_collect_summoner(self, mock_details, mock_ids, mock_summ):
        # Setup Mocks
        mock_summ.return_value = MOCK_SUMMONER
        mock_ids.return_value = MOCK_MATCH_IDS
        mock_details.return_value = MOCK_MATCH_DETAIL
        
        # Test add_summoner
        summoner = self.service.add_summoner("Faker")
        self.assertIsNotNone(summoner)
        self.assertEqual(summoner.summoner_name, "Faker")
        
        # Verify DB
        db = SessionLocal()
        s = db.query(Summoner).filter_by(summoner_name="Faker").first()
        self.assertIsNotNone(s)
        
        # Verify Matches Collected
        matches = db.query(MatchPerformance).filter_by(summoner_id=s.id).all()
        self.assertTrue(len(matches) > 0)
        self.assertEqual(matches[0].match_id, "KR_1001")
        self.assertEqual(matches[0].lane, "MIDDLE")
        self.assertEqual(matches[0].kda, 9.0) # (10+8)/2
        
        db.close()
        print("Test Passed: Summoner added and matches collected.")

if __name__ == '__main__':
    unittest.main()
