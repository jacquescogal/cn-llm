from pydantic import BaseModel, Field
from typing import List
from src.model import *
class NextPageMetaDTO(BaseModel):
    last_id: int
    limit: int
    has_more: bool = Field(default=False)

class WordPageDTO(BaseModel):
    word_list: List[WordModel]
    next_page_meta: NextPageMetaDTO