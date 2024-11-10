from src.model import *

class StudyCardDto(BaseModel):
    word: WordModel
    fsrs_card: FSRSCardModel

class RatingDto(BaseModel):
    rating: int