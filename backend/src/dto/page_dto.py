from pydantic import BaseModel, Field
from typing import List
from src.model import *
class PageMeta(BaseModel):
    # database is less than 10_000 rows, using (offset, limit) pagination
    offset: int
    limit: int
    has_more: Optional[bool] = Field(default=False)

class WordPageDTO(BaseModel):
    word_list: List[WordModel]
    page_meta: PageMeta