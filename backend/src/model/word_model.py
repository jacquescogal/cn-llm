from pydantic import BaseModel

class WordModel(BaseModel):
    word_id: int
    hanzi: str
    pinyin: str
    meaning: str
    hsk_level: int
    is_compound: bool
    is_learnt: bool 