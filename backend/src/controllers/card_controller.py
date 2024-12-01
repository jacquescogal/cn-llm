from fsrs import FSRS, Card, Rating, ReviewLog
from src.repos import *
from src.model import *
from src.dto import *
from typing import Tuple, List
from src.constants import *

class CardController:
    def __init__(self, card_repo: CardRepo, word_repo: WordRepo):
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
    
    async def get_cards_for_word_singular(self, word_id: int) -> ReadCardDto:
        card_word_mapping_list: List[CardWordMapModel] = await self.card_word_map_repo.read_card_word_mapping_by_word_id_singular(word_id=word_id)
        cards: List[CardModel] = await self.card_repo.read_card_list_by_card_id_list([card_word_map.card_id for card_word_map in card_word_mapping_list])
        print(card_word_mapping_list, cards)
        if cards is None:
            return None
        card_list: List[CardDto] = []
        for card in cards:
            card_list.append(CardDto(
                card_id=card.card_id,
                fsrs = card.get_fsrs_card_model(),
                card_type=card.card_type,
                review_type=card.review_type,
                is_disabled=card.is_disabled
            ))
        word: WordModel = await self.word_repo.read_word_by_id(word_id)
        print(word, card_list)
        return ReadCardDto(word=word, card=card_list)
    
    async def create_card_all_for_word(self, word_id: int) -> ReadCardDto:
        # read cards for word_id, check if type has been created before proceeding
        card_word_mapping_list: List[CardWordMapModel] = await self.card_word_map_repo.read_card_word_mapping_by_word_id_singular(word_id=word_id)
        created_card_list = await self.card_repo.read_card_list_by_card_id_list([card_word_map.card_id for card_word_map in card_word_mapping_list])
        type_set = set([(card.card_type,card.review_type) for card in created_card_list])
        cards: List[CardModel] = created_card_list
        for card_type in CardType:
            for review_type in ReviewType:
                if (card_type,review_type) in type_set or not review_type in VALID_REVIEW_COMBINATIONS.get(card_type):
                    continue
                fsrs_card = Card()
                fsrs_card_model = FSRSCardModel.from_fsrs_card(fsrs_card)
                card: CardModel = CardModel.make_card_template(card_type=card_type, review_type=review_type)
                card.inject_fsrs(fsrs_card_model)
                if MULTI_WORD_CONTENT_MAP.get((card_type,review_type), SingleAnswerCardContent) == SingleAnswerCardContent:
                    card.card_content = SingleAnswerCardContent(
                        question="what",
                        answer="what",
                    )
                    cards.append(await self.card_repo.create_card(card))
                # do not create multi word content cards
                # elif MULTI_WORD_CONTENT_MAP.get((card_type,review_type), SingleAnswerCardContent) == OrderedAnswerCardContent:
                #     card.card_content = OrderedAnswerCardContent(
                #         question="what",
                #         answer_list=["what"],
                #     )
        card_list: List[CardDto] = []
        for card in cards:
            card_list.append(CardDto(
                card_id=card.card_id,
                fsrs = card.get_fsrs_card_model(),
                card_type=card.card_type,
                review_type=card.review_type,
                is_disabled=card.is_disabled
            ))
            await self.card_word_map_repo.create_card_word_mapping_list([CardWordMapModel(card_id=card.card_id, word_id=word_id, is_singular=MULTI_WORD_CONTENT_MAP.get((card.card_type,card.review_type), SingleAnswerCardContent) == SingleAnswerCardContent)])
        word: WordModel = await self.word_repo.read_word_by_id(word_id)
        return ReadCardDto(word=word, card=card_list)
    
    async def create_card_of_word_card_type_review_type(self, word_id: int, card_type: CardType, review_type: ReviewType) -> ReadCardDto:
        card_word_mapping_list: List[CardWordMapModel] = await self.card_word_map_repo.read_card_word_mapping_by_word_id(word_id=word_id)
        card: CardModel = await self.card_repo.read_card_of_type(card_id_list=[c.card_id for c in card_word_mapping_list], card_type=card_type, review_type=review_type)
        if card is not None:
            # enable the card
            if card.is_disabled:
                card.is_disabled = False
                await self.card_repo.update_card(card)
            word: WordModel = await self.word_repo.read_word_by_id(word_id)
            return ReadCardDto(word=word, card=[CardDto(card_id=card.card_id,fsrs=card.get_fsrs_card_model(), card_type=card.card_type, review_type=card.review_type, is_disabled=card.is_disabled)])
        fsrs_card = Card()
        fsrs_card_model = FSRSCardModel.from_fsrs_card(fsrs_card)
        card = CardModel.make_card_template(word_id=word_id, card_type=card_type, review_type=review_type)
        card.inject_fsrs(fsrs_card_model)
        created_card =  await self.card_repo.create_card(card)
        if created_card:
            word: WordModel = await self.word_repo.read_word_by_id(word_id)
            return ReadCardDto(word=word, card=[CardDto(card_id=created_card.card_id, fsrs=fsrs_card_model, card_type=card.card_type, review_type=card.review_type, is_disabled=card.is_disabled)])
        return None
    
    async def delete_card(self, card_id: int) ->None:
        card: CardModel = await self.card_repo.read_card_by_id(card_id=card_id)
        if card is not None:
            if not card.is_disabled:
                card.is_disabled = True
                await self.card_repo.update_card(card)
        return None

    async def delete_card_of_word_card_type_review_type(self, word_id: int, card_type: CardType, review_type:ReviewType) -> ReadCardDto:
        card_word_mapping_list: List[CardWordMapModel] = await self.card_word_map_repo.read_card_word_mapping_by_word_id(word_id=word_id)
        card: CardModel = await self.card_repo.read_card_of_type(card_id_list=[c.card_id for c in card_word_mapping_list], card_type=card_type, review_type=review_type)
        if card is not None:
            if not card.is_disabled:
                card.is_disabled = True
                await self.card_repo.update_card(card)
            word: WordModel = await self.word_repo.read_word_by_id(word_id)
            return ReadCardDto(word=word, card=[CardDto(card_id=card.card_id, fsrs=card.get_fsrs_card_model(), card_type=card.card_type, review_type=card.review_type, is_disabled=card.is_disabled)])
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