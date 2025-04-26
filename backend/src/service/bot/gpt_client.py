from src.config.configuration import Config
from openai import AsyncOpenAI
import json

config = Config()

class GPTClient:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=config.openai_api_key)
        self.model = config.openai_model

    def get_client(self):
        return self.client
    
    def get_model(self):
        return self.model