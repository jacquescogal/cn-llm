from src.repos.word_repo import WordRepo
from src.dto import *
from typing import *
class WordController:
    def __init__(self, word_repo: WordRepo):
        self.word_repo = word_repo

    async def get_word_by_id(self, id: int) -> WordModel:
        return await self.word_repo.read_word_by_id(id)
    
    async def get_parent_word_list_by_child_id(self, id: int) -> List[WordModel]:
        return await self.word_repo.get_parent_word_list_by_child_id(id)
    
    async def get_children_word_list_by_parent_id(self, id: int) -> List[WordModel]:
        return await self.word_repo.get_children_word_list_by_parent_id(id)
    
    async def get_word_list_of_hsk_level(self, level: int, page_meta: NextPageMetaDTO) -> WordPageDTO:
        word_list, next_page_meta =  await self.word_repo.get_word_list_of_hsk_level(level, page_meta.last_id, page_meta.limit)
        return WordPageDTO(word_list=word_list, next_page_meta=next_page_meta)
    
    async def get_word_list_learnt(self, page_meta: NextPageMetaDTO) -> WordPageDTO:
        word_list, next_page_meta =  await self.word_repo.get_word_list_learnt(page_meta.last_id, page_meta.limit)
        return WordPageDTO(word_list=word_list, next_page_meta=next_page_meta)
    
    async def get_word_list_not_learnt(self, page_meta: NextPageMetaDTO) -> WordPageDTO:
        word_list, next_page_meta = await self.word_repo.get_word_list_not_learnt(page_meta.last_id, page_meta.limit)
        return WordPageDTO(word_list=word_list, next_page_meta=next_page_meta)
    
    async def get_word_list(self, page_meta: NextPageMetaDTO) -> WordPageDTO:
        word_list, next_page_meta = await self.word_repo.get_word_list(page_meta.last_id, page_meta.limit)
        return WordPageDTO(word_list=word_list, next_page_meta=next_page_meta)
    
    async def get_word_list_from_key_word_search(self, key_word: str, page_meta: NextPageMetaDTO) -> WordPageDTO:
        word_list, next_page_meta = await self.word_repo.get_word_list_from_key_word_search(key_word, page_meta.last_id, page_meta.limit)
        return WordPageDTO(word_list=word_list, next_page_meta=next_page_meta)