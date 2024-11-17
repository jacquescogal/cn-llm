from src.model import *
from typing import List

class CardDto(BaseModel):
    fsrs: FSRSCardModel
    card_type: CardType
    is_disabled: bool
class ReadCardDto(BaseModel):
    word: WordModel
    card: List[CardDto]
class RatingDto(BaseModel):
    rating: int