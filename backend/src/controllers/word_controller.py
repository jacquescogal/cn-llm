from src.controllers import *
from src.service import *
from fastapi import APIRouter
from src.model.dto import *
from typing import List, Tuple
word_controller = APIRouter()

@word_controller.get("/word/{id}", tags=["word"])
async def read_word(id: int) -> WordModel:
    return await word_service.get_word_by_id(id)

@word_controller.get("/word/{id}/parent", tags=["word"])
async def read_parent_word_list(id: int) -> List[WordModel]:
    return await word_service.get_parent_word_list_by_child_id(id)

@word_controller.get("/word/{id}/children", tags=["word"])
async def read_children_word_list(id: int) -> List[WordModel]:
    return await word_service.get_children_word_list_by_parent_id(id)

@word_controller.get("/word/hsk/{level}/offset/{offset}/limit/{limit}", tags=["word"])
async def read_word_list_of_hsk_level(level: int, offset: int, limit: int) -> WordPageDTO:
    return await word_service.get_word_list_of_hsk_level(level, PageMeta(offset=offset, limit=limit))

@word_controller.get("/word/learnt/offset/{offset}/limit/{limit}", tags=["word"])
async def read_word_list_learnt(offset: int, limit: int) -> WordPageDTO:
    return await word_service.get_word_list_learnt(PageMeta(offset=offset, limit=limit))

@word_controller.get("/word/not-learnt/offset/{offset}/limit/{limit}", tags=["word"])
async def read_word_list_not_learnt(offset: int, limit: int) -> WordPageDTO:
    return await word_service.get_word_list_not_learnt(PageMeta(offset=offset, limit=limit))

@word_controller.get("/word/offset/{offset}/limit/{limit}", tags=["word"])
async def read_word_list(offset: int, limit: int, hsk: str = "", learnt: bool = None) -> WordPageDTO:
    hsk_list = list(map(int,hsk.split(","))) if hsk != "" else []
    return await word_service.get_word_list(hsk_list, learnt, PageMeta(offset=offset, limit=limit))

@word_controller.get("/word/search/{key_word}/offset/{offset}/limit/{limit}", tags=["word"])    
async def read_word_list_by_key_word_search(key_word: str, offset: int, limit: int, hsk: str = "", learnt: bool = None) -> WordPageDTO:
    hsk_list = list(map(int,hsk.split(","))) if hsk != "" else []
    return await word_service.get_word_list_from_key_word_search(key_word, hsk_list, learnt, PageMeta(offset=offset, limit=limit))