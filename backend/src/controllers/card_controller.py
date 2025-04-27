from src.controllers import *
from src.service import *
from fastapi import APIRouter
from src.model.dto import *
from typing import List, Tuple
card_controller = APIRouter()

@card_controller.get("/card/word/{word_id}", tags=["card"])
async def get_cards_for_word(word_id: int) -> Optional[ReadCardDto]:
    return await card_service.get_cards_for_word_singular(word_id)

@card_controller.post("/card/word/{word_id}", tags=["card"])
async def create_card_all_for_word(word_id: int) -> Optional[ReadCardDto]:
    return await card_service.create_card_all_for_word(word_id)

@card_controller.post("/card/word/{word_id}/type/{card_type}/review/{review_type}", tags=["card"])
async def create_card_of_word_card_type(word_id: int, card_type: int, review_type: int) -> Optional[ReadCardDto]:
    return await card_service.create_card_of_word_card_type_review_type(word_id, CardType(card_type), ReviewType(review_type))

@card_controller.delete("/card/word/{word_id}/type/{card_type}/review/{review_type}", tags=["card"])
async def delete_card_of_word_card_type_review_type(word_id: int, card_type: int, review_type: int) -> Optional[ReadCardDto]:
    return await card_service.delete_card_of_word_card_type_review_type(word_id, CardType(card_type), ReviewType(review_type))

@card_controller.delete("/card/{card_id}", tags=["card"])
async def delete_card(card_id: int) -> Optional[ReadCardDto]:
    return await card_service.delete_card(card_id=card_id)
