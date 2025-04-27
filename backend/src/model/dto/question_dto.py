from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from src.constants.enums import *

class QuestionDTO(BaseModel):
    question: str
    options: Optional[List[str]] = Field(default=None)

class GetQuestionDTO(BaseModel):
    card_id: int
    word_id: int
    question: QuestionDTO
    question_type: QuestionType

class CreateQuestionDTO(BaseModel):
    word_id: int
    question_type: QuestionType

class ReviewDTO(BaseModel):
    question: str
    options: Optional[List[str]] = Field(default=None)
    answer: str

class GetReviewQuestionDTO(BaseModel):
    card_id: int
    word_id: int
    question: QuestionDTO
    question_type: QuestionType
    review: ReviewDTO