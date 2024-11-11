from fsrs import FSRS, Card, Rating, ReviewLog
from src.repos import *
from src.model import *
from src.dto import *
from typing import Tuple, List

class CardController:
    def __init__(self, card_repo: CardRepo, word_repo: WordRepo):
        self.fsrs = FSRS()
        self.card_repo = card_repo
        self.word_repo = word_repo

    def _review_card(self, card: FSRSCardModel, rating: Rating) -> Tuple[FSRSCardModel, ReviewLog] :
        fsrs_card, review_log = self.fsrs.review_card(card.get_fsrs_card(), rating)
        return FSRSCardModel.from_fsrs_card(fsrs_card), review_log

    async def update_card_on_review(self, card_id: int, rating: Rating) -> bool:
        card: CardModel = await self.card_repo.read_card_by_id(card_id)
        fsrs_card: Card = card.get_fsrs_card()
        updated_card, review_log = self._review_card(fsrs_card, rating)
        updated_card_model = CardModel.from_fsrs_card(card_id, card.get_word_id(), updated_card)
        return await self.card_repo.update_card(updated_card_model)
    
    async def get_card_by_id(self, card_id: int) -> StudyCardDto:
        card: CardModel = await self.card_repo.read_card_by_id(card_id)
        if card is None:
            return None
        word: WordModel = await self.word_repo.read_word_by_id(card.get_word_id())
        fsrs_card: FSRSCardModel = card.get_fsrs_card()
        return StudyCardDto(word=word, fsrs_card=fsrs_card)
    
    async def get_card_by_word_id(self, word_id: int) -> StudyCardDto:
        card: CardModel = await self.card_repo.read_card_by_word_id(word_id)
        if card is None:
            return None
        word: WordModel = await self.word_repo.read_word_by_id(word_id)
        fsrs_card: FSRSCardModel = card.get_fsrs_card()
        return StudyCardDto(word=word, fsrs_card=fsrs_card)
    
    async def create_card(self, word_id: int) -> StudyCardDto:
        word: WordModel = await self.word_repo.read_word_by_id(word_id)
        if word is None or word.is_learnt == True:
            return None
        fsrs_card = Card()
        fsrs_card_model = FSRSCardModel.from_fsrs_card(fsrs_card)
        card = CardModel.from_fsrs_card(0, word_id, fsrs_card_model)
        card_id =  await self.card_repo.create_card(card)
        card.card_id = card_id
        return StudyCardDto(word=word, fsrs_card=fsrs_card_model)
    
    async def get_due_card_list(self, limit: int) -> list[StudyCardDto]:
        due_card_list: List[CardModel] =  await self.card_repo.get_due_card_list(limit)
        card_id_list = [card.card_id for card in due_card_list]
        word_list: List[WordModel] = await self.word_repo.get_word_list_from_id_list(card_id_list)
        study_card_list = []
        word_id_card_map = {word.word_id: word for word in word_list}
        for card in due_card_list:
            word = word_id_card_map[card.word_id]
            study_card_list.append(StudyCardDto(word=word, fsrs_card=card.get_fsrs_card()))
        return study_card_list
    async def get_past_due_card_list(self) -> list[StudyCardDto]:
        past_due_card_list: List[CardModel] = await self.card_repo.get_past_due_card_list()
        card_id_list = [card.card_id for card in past_due_card_list]
        word_list: List[WordModel] = await self.word_repo.get_word_list_from_id_list(card_id_list)
        study_card_list = []
        word_id_card_map = {word.word_id: word for word in word_list}
        for card in past_due_card_list:
            word = word_id_card_map[card.word_id]
            study_card_list.append(StudyCardDto(word=word, fsrs_card=card.get_fsrs_card()))
        return study_card_list
    
    async def get_card_list(self, page_meta: NextPageMetaDTO) -> Tuple[List[StudyCardDto], NextPageMetaDTO]:
        card_list, next_page_meta = await self.card_repo.get_card_list(page_meta.last_id, page_meta.limit)
        if len(card_list) == 0:
            return [], next_page_meta
        card_id_list = [card.card_id for card in card_list]
        word_list: List[WordModel] = await self.word_repo.get_word_list_from_id_list(card_id_list)
        study_card_list = []
        word_id_card_map = {word.word_id: word for word in word_list}
        for card in card_list:
            word = word_id_card_map[card.word_id]
            study_card_list.append(StudyCardDto(word=word, fsrs_card=card.get_fsrs_card()))
        return study_card_list, next_page_meta