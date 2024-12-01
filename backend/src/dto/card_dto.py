from src.model import *
from typing import List

# read card
class CardDto(BaseModel):
    card_id: int
    card_type: CardType
    review_type: ReviewType
    is_disabled: bool
    fsrs: FSRSCardModel

# read the card and word
class ReadCardDto(BaseModel):
    word: WordModel
    card: List[CardDto]

class RatingDto(BaseModel):
    rating: int