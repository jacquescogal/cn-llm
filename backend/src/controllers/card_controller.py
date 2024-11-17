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


    async def update_card_on_review(self, card_id: int, rating: Rating) -> bool:
        card: CardModel = await self.card_repo.read_card_by_id(card_id)
        if card is None:
            return False
        card.review(self.fsrs, rating)
        return await self.card_repo.update_card(card)
    
    async def get_card(self, word_id: int) -> ReadCardDto:
        cards: List[CardModel] = await self.card_repo.read_card_list_by_word_id(word_id=word_id)
        if cards is None:
            return None
        card_list: List[CardDto] = []
        for card in cards:
            card_list.append(CardDto(
                fsrs = card.get_fsrs_card_model(),
                card_type=card.card_type,
                is_disabled=card.is_disabled
            ))
        word: WordModel = await self.word_repo.read_word_by_id(word_id)
        return ReadCardDto(word=word, card=card_list)
    
    async def create_card_all(self, word_id: int) -> ReadCardDto:
        cards: List[CardModel] = []
        for card_type in CardType:
            fsrs_card = Card()
            fsrs_card_model = FSRSCardModel.from_fsrs_card(fsrs_card)
            card = CardModel.make_card_template(word_id=word_id, card_type=card_type)
            card.inject_fsrs(fsrs_card_model)
            cards.append(await self.card_repo.create_card(card))
        card_list: List[CardDto] = []
        for card in cards:
            card_list.append(CardDto(
                fsrs = card.get_fsrs_card_model(),
                card_type=card.card_type,
                is_disabled=card.is_disabled
            ))
        word: WordModel = await self.word_repo.read_word_by_id(card.get_word_id())
        return ReadCardDto(word=word, card=card_list)
    
    async def create_card(self, word_id: int, card_type: CardType) -> ReadCardDto:
        card: CardModel = await self.card_repo.read_card_of_type(word_id=word_id, card_type=card_type)
        if card is not None:
            # enable the card
            if card.is_disabled:
                card.is_disabled = False
                await self.card_repo.update_card(card)
            word: WordModel = await self.word_repo.read_word_by_id(word_id)
            return ReadCardDto(word=word, card=[CardDto(fsrs=card.get_fsrs_card_model(), card_type=card.card_type, is_disabled=card.is_disabled)])
        fsrs_card = Card()
        fsrs_card_model = FSRSCardModel.from_fsrs_card(fsrs_card)
        card = CardModel.make_card_template(word_id=word_id, card_type=card_type)
        card.inject_fsrs(fsrs_card_model)
        is_created =  await self.card_repo.create_card(card)
        if is_created:
            word: WordModel = await self.word_repo.read_word_by_id(word_id)
            return ReadCardDto(word=word, card=[CardDto(fsrs=fsrs_card_model, card_type=card.card_type, is_disabled=card.is_disabled)])
        return None
    
    async def delete_card(self, word_id: int, card_type: CardType) -> ReadCardDto:
        card: CardModel = await self.card_repo.read_card_of_type(word_id=word_id, card_type=card_type)
        if card is not None:
            if not card.is_disabled:
                card.is_disabled = True
                await self.card_repo.update_card(card)
            word: WordModel = await self.word_repo.read_word_by_id(word_id)
            return ReadCardDto(word=word, card=[CardDto(fsrs=card.get_fsrs_card_model(), card_type=card.card_type, is_disabled=card.is_disabled)])
        return None

    # async def get_scheduled_card_list(self, limit: int) -> list[StudyCardDto]:
    #     scheduled_card_list: List[CardModel] =  await self.card_repo.get_scheduled_card_list(limit)
    #     word_id_list = [card.word_id for card in scheduled_card_list]
    #     word_list: List[WordModel] = await self.word_repo.get_word_list_from_id_list(word_id_list)
    #     study_card_list = []
    #     word_id_card_map = {word.word_id: word for word in word_list}
    #     for card in scheduled_card_list:
    #         word = word_id_card_map[card.word_id]
    #         study_card_list.append(StudyCardDto(word=word, fsrs_card=card.get_fsrs_card_model(), card_type=card.card_type))
    #     return study_card_list
    
    # async def get_due_card_list(self) -> list[StudyCardDto]:
    #     due_card_list: List[CardModel] = await self.card_repo.get_due_card_list()
    #     word_id_list = [card.word_id for card in due_card_list]
    #     word_list: List[WordModel] = await self.word_repo.get_word_list_from_id_list(word_id_list)
    #     study_card_list = []
    #     word_id_card_map = {word.word_id: word for word in word_list}
    #     for card in due_card_list:
    #         word = word_id_card_map[card.word_id]
    #         study_card_list.append(StudyCardDto(word=word, fsrs_card=card.get_fsrs_card_model(), card_type=card.card_type))
    #     return study_card_list
    
    # async def get_card_list(self, page_meta: PageMeta) -> Tuple[List[StudyCardDto], PageMeta]:
    #     card_list, next_page_meta = await self.card_repo.get_card_list(page_meta.last_id, page_meta.limit)
    #     if len(card_list) == 0:
    #         return [], next_page_meta
    #     card_id_list = [card.card_id for card in card_list]
    #     word_list: List[WordModel] = await self.word_repo.get_word_list_from_id_list(card_id_list)
    #     study_card_list = []
    #     word_id_card_map = {word.word_id: word for word in word_list}
    #     for card in card_list:
    #         word = word_id_card_map[card.word_id]
    #         study_card_list.append(StudyCardDto(word=word, fsrs_card=card.get_fsrs_card()))
    #     return study_card_list, next_page_meta