from pydantic import BaseModel, Field
from src.enums import *
from typing import Optional

class CardWordMapModel(BaseModel):
    card_id: int
    word_id: int
    is_singular: bool