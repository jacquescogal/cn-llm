from src.routers import *
from src.controllers import *
from fastapi import APIRouter
from src.model.dto import *
from src.service.review_generators import ReviewGeneratorFactory
from typing import List, Tuple
review_router = APIRouter()

mock_word_model = WordModel(
    hanzi="你好",
    pinyin="nǐ hǎo",
    meaning="hello",
    word_id=1,
    hsk_level=1,
    is_compound=False,
    is_learnt=False
)

mock_word_model_2 = WordModel(
    hanzi="再见",
    pinyin="zài jiàn",
    meaning="goodbye",
    word_id=2,
    hsk_level=1,
    is_compound=False,
    is_learnt=False
)

mock_word_model_3 = WordModel(
    hanzi="谢谢",
    pinyin="xiè xie",
    meaning="thank you",
    word_id=3,
    hsk_level=1,
    is_compound=False,
    is_learnt=False
)
mock_word_model_4 = WordModel(
    hanzi="我爱你",
    pinyin="wǒ ài nǐ",
    meaning="I love you",
    word_id=4,
    hsk_level=1,
    is_compound=False,
    is_learnt=False
)

@review_router.get("/review/card/{card_id}", tags=["review"]) 
async def get_review_card_by_id(card_id: int) -> Optional[ReviewDto]:
    return await review_controller.get_review_card_by_id(card_id)





# TODO: remove
from enum import Enum
class card_type_dto(Enum):
    MEANING = "meaning"
    PINYIN = "pinyin"
    HANZI = "hanzi"
    TONE = "tone"
    PARAGRAPH = "paragraph"

    def get_int_value(self):
        return {
            card_type_dto.MEANING: 1,
            card_type_dto.PINYIN: 2,
            card_type_dto.HANZI: 3,
            card_type_dto.TONE: 4,
            card_type_dto.PARAGRAPH: 5
        }[self]

class review_type_dto(Enum):
    OpenEnded = "open"
    MCQ = "mcq"
    DRAG_AND_DROP = "dnd"
    def get_int_value(self):
        return {
            review_type_dto.OpenEnded: 1,
            review_type_dto.MCQ: 2,
            review_type_dto.DRAG_AND_DROP: 3
        }[self]

@review_router.get("/review/{card_type}/{review_type}", tags=["review"])
async def get_test_review_definition(card_type: card_type_dto, review_type: review_type_dto):

    return await ReviewGeneratorFactory.get_review_generator(CardType(int(card_type.get_int_value())), ReviewType(int(review_type.get_int_value()))).generate_review_card(mock_word_model, mock_word_model_2, mock_word_model_3, mock_word_model_4)

