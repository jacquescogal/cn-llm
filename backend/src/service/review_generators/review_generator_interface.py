from abc import ABC, abstractmethod
from src.constants.enums import *
from src.model import *
from src.service.bot import GPTClient
from src.model import *

class ReviewGeneratorInterface(ABC):
    def __init__(self,gpt_client: GPTClient = None):
        self.client = None if gpt_client == None else gpt_client.get_client()
        self.model = None if gpt_client == None else gpt_client.get_model()

    @abstractmethod
    def is_applicable(self, *word_models: WordModel) -> bool:
        """
        Check if the review generator is applicable for the given word models.
        """
        pass

    @abstractmethod
    async def generate_review_card(self, *word_models: WordModel) -> ReviewContent:
        pass