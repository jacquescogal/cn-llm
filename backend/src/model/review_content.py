from pydantic import BaseModel, Field
from fsrs import Card as fsrsCard, State, FSRS, Rating, ReviewLog
from datetime import datetime, timezone
from src.model.word_model import WordModel
from src.enums import *
from typing import Optional, List,Dict
import json

class ReviewContent(BaseModel):
    question: str
    allow_hanzi: Optional[bool] = Field(default=True)
    allow_pinyin: Optional[bool] = Field(default=True)
    allow_meaning: Optional[bool] = Field(default=True)
    allow_tone: Optional[bool] = Field(default=True)

    def get_json(self):
        return json.dumps(self.dict())

class SingleAnswerCardContent(ReviewContent):
    answer: str
    wrong_options: Optional[List[str]] = Field(default=None)
    answer_map: Optional[Dict[str, str]] = Field(default=None)

class OrderedAnswerCardContent(ReviewContent):
    template: str
    answer_list: List[str]

class MappedAnswerCardContent(ReviewContent):
    answer_map: Dict[str, str]