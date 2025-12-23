import os

class Config:
    RIOT_API_KEY = os.getenv("RIOT_API_KEY", "")
    # Flex Queue ID is 440
    QUEUE_ID = 440
    REGION = "kr" # Defaulting to KR as per "League of Legends" (Korean context implied)
    ROUTING_VALUE = "asia" # for match-v5
    PLATFORM_ROUTING_VALUE = "kr" # for summoner-v4
    
    # Update key at runtime
    @classmethod
    def update_api_key(cls, new_key):
        cls.RIOT_API_KEY = new_key
