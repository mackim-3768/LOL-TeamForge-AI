import os

class Config:
    RIOT_API_KEY = os.getenv("RIOT_API_KEY", "RGAPI-d23289f8-167f-46d9-a091-bfe3a90fdc86")
    # Flex Queue ID is 440
    QUEUE_ID = 440
    REGION = "kr" # Defaulting to KR as per "League of Legends" (Korean context implied)
    ROUTING_VALUE = "asia" # for match-v5
    PLATFORM_ROUTING_VALUE = "kr" # for summoner-v4
    
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

    # Update key at runtime
    @classmethod
    def update_api_key(cls, new_key):
        cls.RIOT_API_KEY = new_key

    @classmethod
    def update_openai_key(cls, new_key):
        cls.OPENAI_API_KEY = new_key
