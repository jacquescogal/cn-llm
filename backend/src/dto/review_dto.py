from pydantic import BaseModel
from src.enums import *
from src.dto import *


# review the card
class ReviewDto(BaseModel):
    card: CardDto
    review_type: ReviewType

class OpenEndedReviewDto(ReviewDto):
    question: str

class ReviewType(Enum):
    OpenEnded = 1
    SingleSelect = 2
    MultiSelect = 3