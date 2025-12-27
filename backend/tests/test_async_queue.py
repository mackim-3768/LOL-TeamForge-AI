import unittest
from unittest.mock import patch, MagicMock
from backend.core_api.main import app, get_db
from backend.collector.collector_service import CollectorService
from fastapi.testclient import TestClient
from backend.shared.database import Summoner

class TestAsyncQueue(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    @patch('backend.core_api.main.collect_summoner_data')
    @patch('backend.collector.collector_service.CollectorService.add_summoner')
    @patch('backend.core_api.main.get_db')
    def test_register_summoner_enqueues_task(self, mock_get_db, mock_add_summoner, mock_task):
        # Mock DB
        mock_db_session = MagicMock()
        mock_get_db.return_value = mock_db_session

        # Mock: Summoner not in DB
        mock_db_session.query.return_value.filter.return_value.first.return_value = None

        # Mock: Add summoner returns a new summoner
        mock_summoner = Summoner(id=1, summoner_name="TestSummoner", summoner_level=30)
        mock_add_summoner.return_value = mock_summoner

        # Make request
        response = self.client.post("/summoners/", json={"name": "TestSummoner"})

        # Verify response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['name'], "TestSummoner")

        # Verify task enqueued
        mock_task.delay.assert_called_once_with(1)

if __name__ == '__main__':
    unittest.main()
