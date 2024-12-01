from src.routers import *
from src.controllers import *
from fastapi import APIRouter
from src.dto import *
from typing import List, Tuple
card_router = APIRouter()

@card_router.get("/card/word/{word_id}", tags=["card"])
async def get_cards_for_word(word_id: int) -> Optional[ReadCardDto]:
    return await card_controller.get_cards_for_word(word_id)

@card_router.post("/card/word/{word_id}", tags=["card"])
async def create_card_all_for_word(word_id: int) -> Optional[ReadCardDto]:
    return await card_controller.create_card_all_for_word(word_id)

@card_router.post("/card/word/{word_id}/type/{card_type}", tags=["card"])
async def create_card_of_word_card_type(word_id: int, card_type: int) -> Optional[ReadCardDto]:
    return await card_controller.create_card_of_word_card_type(word_id, CardType(card_type))

@card_router.delete("/card/word/{word_id}/type/{card_type}", tags=["card"])
async def delete_card_of_word_card_type(word_id: int, card_type: int) -> Optional[ReadCardDto]:
    return await card_controller.delete_card_of_word_card_type(word_id, CardType(card_type))

@card_router.delete("/card/{card_id}", tags=["card"])
async def delete_card(card_id: int) -> Optional[ReadCardDto]:
    return await card_controller.delete_card(card_id=card_id)

# @card_router.put("/card/{id}", tags=["card"])
# async def update_card_on_review(id: int, rating_dto: RatingDto)-> bool:
#     return await card_controller.update_card_on_review(id, rating_dto.rating)


# @card_router.get("/card/scheduled/limit/{limit}", tags=["card"])
# async def read_due_card_list(limit: int)-> List[StudyCardDto]:
#     return await card_controller.get_scheduled_card_list(limit)

# @card_router.get("/card/due", tags=["card"])
# async def read_due_card_list()-> List[StudyCardDto]:
#     return await card_controller.get_due_card_list()

# @card_router.get("/card/offset/{offset}/limit/{limit}", tags=["card"])
# async def read_card_list(offset: int, limit: int) -> Tuple[List[StudyCardDto], PageMeta]:
#     return await card_controller.get_card_list(PageMeta(last_id=offset, limit=limit))