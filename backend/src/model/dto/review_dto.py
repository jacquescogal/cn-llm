from pydantic import BaseModel, field_validator
from typing import List, Optional
from src.enums import *
from src.model.dto.card_dto import *

# review the card
class ReviewDto(BaseModel):
    card: CardDto
    question: str
    hanzi: Optional[str] = None
    pinyin: Optional[str] = None
    toneless_pinyin: Optional[str] = None
    meaning: Optional[str] = None
    options: Optional[List[str]] = None # to be filled by ai 
    map_to: Optional[List[str]] = None # for mapped answer

class ReviewAnswerDto(BaseModel):
    card_id: int
    answer: str