from src.routers import *
from src.controllers import *
from fastapi import APIRouter
from src.dto import *
from typing import List, Tuple
card_router = APIRouter()

@card_router.get("/card/{id}")
async def read_card(id: int)-> StudyCardDto:
    return await card_controller.get_card_by_id(id)

@card_router.get("/card/word/{id}")
async def read_card_by_word_id(id: int)-> CardModel:
    return await card_controller.get_card_by_word_id(id)

@card_router.post("/card/{id}")
async def create_card(id: int)-> StudyCardDto:
    return await card_controller.create_card(id)

@card_router.put("/card/{id}")
async def update_card_on_review(id: int, rating_dto: RatingDto)-> bool:
    return await card_controller.update_card_on_review(id, rating_dto.rating)


@card_router.get("/card/due/limit/{limit}")
async def read_due_card_list(limit: int)-> List[StudyCardDto]:
    return await card_controller.get_due_card_list(limit)

@card_router.get("/card/past/due/limit/{limit}")
async def read_past_due_card_list(limit: int)-> List[StudyCardDto]:
    return await card_controller.get_past_due_card_list()

@card_router.get("/card/offset/{offset}/limit/{limit}")
async def read_card_list(offset: int, limit: int) -> Tuple[List[StudyCardDto], NextPageMetaDTO]:
    return await card_controller.get_card_list(NextPageMetaDTO(last_id=offset, limit=limit))