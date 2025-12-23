# Mock responses for verification
MOCK_SUMMONER = {
    "id": "mock_summ_id",
    "accountId": "mock_acc_id",
    "puuid": "mock_puuid_123",
    "name": "Faker",
    "profileIconId": 1,
    "revisionDate": 123456789,
    "summonerLevel": 999
}

MOCK_MATCH_IDS = ["KR_1001", "KR_1002"]

MOCK_MATCH_DETAIL = {
    "metadata": {
        "matchId": "KR_1001",
    },
    "info": {
        "gameCreation": 1600000000000,
        "gameDuration": 1800, # 30 mins
        "participants": [
            {
                "puuid": "mock_puuid_123",
                "summonerName": "Faker",
                "teamPosition": "MIDDLE",
                "role": "SOLO",
                "championName": "Ahri",
                "win": True,
                "kills": 10,
                "deaths": 2,
                "assists": 8,
                "goldEarned": 15000,
                "visionScore": 30,
                "totalMinionsKilled": 200,
                "neutralMinionsKilled": 10,
                "totalDamageDealtToChampions": 25000
            }
        ]
    }
}
