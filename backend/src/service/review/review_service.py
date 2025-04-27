from fsrs import FSRS, Card, Rating, ReviewLog
from src.repos import *
from src.model import *
from src.model.dto import *
from src.util import *
from typing import Tuple, List
from src.constants import *
from random import shuffle

class ReviewService:
    def __init__(self, card_repo: CardRepo, word_repo: WordRepo, card_word_map_repo: CardWordMapRepo):
        self.fsrs = FSRS()
        self.card_repo = card_repo
        self.word_repo = word_repo
        self.card_word_map_repo = card_word_map_repo


    async def update_card_on_review(self, card_id: int, rating: Rating) -> bool:
        card: CardModel = await self.card_repo.read_card_by_id(card_id)
        if card is None:
            return False
        card.review(self.fsrs, rating)
        return await self.card_repo.update_card(card)
    
    async def get_review_card_by_id(self, card_id: int) -> ReviewDto:
        card:CardModel = await self.card_repo.read_card_by_id(card_id)
        if card is None:
            return None
        card_dto: CardDto = CardDto.from_card_model(card)

        if MULTI_WORD_CONTENT_MAP.get((card.card_type,card.review_type), SingleAnswerCardContent) == SingleAnswerCardContent:
            # get word
            mapped_word_id: List[CardWordMapModel] = await self.card_word_map_repo.read_card_word_mapping_by_card_id(card_id)
            if mapped_word_id is None or len(mapped_word_id) == 0:
                return None
            word: WordModel = await self.word_repo.read_word_by_id(mapped_word_id[0].word_id)
            review_dto: ReviewDto = ReviewDto(
                card=card_dto,
                question=card.card_content.question, 
                hanzi=word.hanzi if card.card_content.allow_hanzi else None,
                pinyin=word.pinyin if card.card_content.allow_pinyin and card.card_content.allow_tone else None,
                meaning=word.meaning if card.card_content.allow_meaning else None,
                toneless_pinyin=remove_pinyin_tones(word.pinyin) if card.card_content.allow_pinyin and not card.card_content.allow_tone else None,
                options = card.card_content.wrong_options + [card.card_content.answer] if card.card_content.wrong_options else None,
            )
            if review_dto.options:
                shuffle(review_dto.options)  
        # TODO: multiple answer
        return review_dto