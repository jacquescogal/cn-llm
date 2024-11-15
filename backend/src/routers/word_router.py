from src.routers import *
from src.controllers import *
from fastapi import APIRouter
from src.dto import *
from typing import List, Tuple
word_router = APIRouter()

@word_router.get("/word/{id}")
async def read_word(id: int) -> WordModel:
    return await word_controller.get_word_by_id(id)

@word_router.get("/word/{id}/parent")
async def read_parent_word_list(id: int) -> List[WordModel]:
    return await word_controller.get_parent_word_list_by_child_id(id)

@word_router.get("/word/{id}/children")
async def read_children_word_list(id: int) -> List[WordModel]:
    return await word_controller.get_children_word_list_by_parent_id(id)

@word_router.get("/word/hsk/{level}/offset/{last_id}/limit/{limit}")
async def read_word_list_of_hsk_level(level: int, last_id: int, limit: int) -> WordPageDTO:
    return await word_controller.get_word_list_of_hsk_level(level, NextPageMetaDTO(last_id=last_id, limit=limit))

@word_router.get("/word/learnt/offset/{last_id}/limit/{limit}")
async def read_word_list_learnt(last_id: int, limit: int) -> WordPageDTO:
    return await word_controller.get_word_list_learnt(NextPageMetaDTO(last_id=last_id, limit=limit))

@word_router.get("/word/not-learnt/offset/{last_id}/limit/{limit}")
async def read_word_list_not_learnt(last_id: int, limit: int) -> WordPageDTO:
    return await word_controller.get_word_list_not_learnt(NextPageMetaDTO(last_id=last_id, limit=limit))

@word_router.get("/word/offset/{last_id}/limit/{limit}")
async def read_word_list(last_id: int, limit: int) -> WordPageDTO:
    return await word_controller.get_word_list(NextPageMetaDTO(last_id=last_id, limit=limit))

@word_router.get("/word/search/{key_word}/offset/{last_id}/limit/{limit}")
async def read_word_list_by_key_word_search(key_word: str, last_id: int, limit: int) -> WordPageDTO:
    ans =  await word_controller.get_word_list_from_key_word_search(key_word, NextPageMetaDTO(last_id=last_id, limit=limit))
    print(ans)
    return ans
