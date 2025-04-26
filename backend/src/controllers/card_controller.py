from fsrs import FSRS, Card, Rating, ReviewLog
from src.repos import *
from src.model import *
from src.model.dto import *
from src.util import *
from typing import Tuple, List
from src.constants import *
from src.service.review_generators import ReviewGeneratorFactory

class CardController:
    def __init__(self, card_repo: CardRepo, word_repo: WordRepo, card_word_map_repo: CardWordMapRepo, review_generator_factory: ReviewGeneratorFactory):
        self.fsrs = FSRS()
        self.review_generator_factory = review_generator_factory
        self.card_repo = card_repo
        self.word_repo = word_repo
        self.card_word_map_repo = card_word_map_repo

    
    async def get_cards_for_word_singular(self, word_id: int) -> ReadCardDto:
        card_word_mapping_list: List[CardWordMapModel] = await self.card_word_map_repo.read_card_word_mapping_by_word_id_singular(word_id=word_id)
        cards: List[CardModel] = await self.card_repo.read_card_list_by_card_id_list([card_word_map.card_id for card_word_map in card_word_mapping_list])
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
        return ReadCardDto(word=word, card=card_list)


    
    async def create_card_all_for_word(self, word_id: int) -> ReadCardDto:
        # read cards for word_id, check if type has been created before proceeding
        card_word_mapping_list: List[CardWordMapModel] = await self.card_word_map_repo.read_card_word_mapping_by_word_id_singular(word_id=word_id)
        created_card_list = await self.card_repo.read_card_list_by_card_id_list([card_word_map.card_id for card_word_map in card_word_mapping_list])
        type_set = set([(card.card_type,card.review_type) for card in created_card_list])
        cards: List[CardModel] = created_card_list
        word: WordModel = await self.word_repo.read_word_by_id(word_id)
        for card_type in CardType:
            if card_type == CardType.TONE and word.pinyin == remove_pinyin_tones(word.pinyin):
                continue
            for review_type in ReviewType:
                if (card_type,review_type) in type_set or not review_type in VALID_REVIEW_COMBINATIONS.get(card_type):
                    continue
                fsrs_card = Card()
                fsrs_card_model = FSRSCardModel.from_fsrs_card(fsrs_card)
                card: CardModel = CardModel.make_card_template(card_type=card_type, review_type=review_type)
                card.inject_fsrs(fsrs_card_model)
                # check if card is viable for tone review
                if MULTI_WORD_CONTENT_MAP.get((card_type,review_type), SingleAnswerCardContent) == SingleAnswerCardContent:
                    review_generator = self.review_generator_factory.get_review_generator(card_type=card_type, review_type=review_type)
                    if not review_generator.is_applicable(word):
                        print(f"Skipped: Card type {card_type} and review type {review_type} is not applicable for word {word.hanzi}")
                        continue
                    card.card_content = await review_generator.generate_review_card(word)
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
        return ReadCardDto(word=word, card=card_list)
    
    async def create_card_of_word_card_type_review_type(self, word_id: int, card_type: CardType, review_type: ReviewType) -> ReadCardDto:
        card_word_mapping_list: List[CardWordMapModel] = await self.card_word_map_repo.read_card_word_mapping_by_word_id(word_id=word_id)
        card: CardModel = await self.card_repo.read_card_of_type(card_id_list=[c.card_id for c in card_word_mapping_list], card_type=card_type, review_type=review_type)
        word: WordModel = await self.word_repo.read_word_by_id(word_id)
        if card is not None:
            # enable the card
            if card.is_disabled:
                card.is_disabled = False
                await self.card_repo.update_card(card)
            return ReadCardDto(word=word, card=[CardDto(card_id=card.card_id,fsrs=card.get_fsrs_card_model(), card_type=card.card_type, review_type=card.review_type, is_disabled=card.is_disabled)])
        fsrs_card = Card()
        fsrs_card_model = FSRSCardModel.from_fsrs_card(fsrs_card)
        card = CardModel.make_card_template(card_type=card_type, review_type=review_type)
        card.card_content = self._get_card_content_singular(word=word, card_type=card_type)
        card.inject_fsrs(fsrs_card_model)
        created_card =  await self.card_repo.create_card(card)
        await self.card_word_map_repo.create_card_word_mapping_list([CardWordMapModel(card_id=created_card.card_id, word_id=word_id, is_singular=True)])
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


    
    # helper functions
    def _get_card_content_singular(self, word: WordModel, card_type: CardType) -> SingleAnswerCardContent:
        match card_type:
            case CardType.MEANING:
                return SingleAnswerCardContent(
                    question=f"What is the definition?",
                    answer=word.meaning,
                    allow_meaning=False
                )
            case CardType.PINYIN:
                return SingleAnswerCardContent(
                    question=f"What is the pinyin?",
                    answer=word.pinyin,
                    allow_pinyin=False
                )
            case CardType.HANZI:
                return SingleAnswerCardContent(
                    question=f"What is the hanzi?",
                    answer=word.hanzi,
                    allow_hanzi=False
                )
            case CardType.TONE:
                return SingleAnswerCardContent(
                    question=f"What is the tone?",
                    answer=word.pinyin,
                    allow_tone=False,
                )
            case _:
                raise Exception("Invalid card type")
            
        
    def _get_card_content_multi(self, words: List[WordModel], card_type: CardType) -> SingleAnswerCardContent:
        # this should be generated by AI
        match card_type:
            case CardType.PARAGRAPH:
                # TODO: generate paragraph
                # return OrderedAnswerCardContent(
                #     question="what",
                #     answer_list=["what"]
                # )
                pass
            case _:
                raise Exception("Invalid card type")
     
    