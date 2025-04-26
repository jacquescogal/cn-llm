from src.model import *
from typing import List

# read card
class CardDto(BaseModel):
    card_id: int
    card_type: CardType
    review_type: ReviewType
    is_disabled: bool
    fsrs: FSRSCardModel

    @classmethod
    def from_card_model(cls, card: CardModel) -> 'CardDto':
        return CardDto(
            card_id=card.card_id,
            card_type=card.card_type,
            review_type=card.review_type,
            is_disabled=card.is_disabled,
            fsrs=card.get_fsrs_card_model()
        )

# read the card and word
class ReadCardDto(BaseModel):
    word: WordModel
    card: List[CardDto]

class RatingDto(BaseModel):
    rating: int