from src.enums import *
from src.model import *
from src.service.bot import *
from .review_generator_interface import ReviewGeneratorInterface
from .mcq import *
from .open import *
from .dnd import *

class ReviewGeneratorFactory:
    
    _gpt_client: GPTClient = GPTClient()
    _mcq_hanzi_review_generator: MCQHanziReviewGenerator = MCQHanziReviewGenerator(_gpt_client)
    _mcq_meaning_review_generator: MCQMeaningReviewGenerator = MCQMeaningReviewGenerator(_gpt_client)
    _mcq_pinyin_review_generator: MCQPinyinReviewGenerator = MCQPinyinReviewGenerator(_gpt_client)
    _mcq_tone_review_generator: MCQToneReviewGenerator = MCQToneReviewGenerator(_gpt_client)

    _open_meaning_review_generator: OpenMeaningReviewGenerator = OpenMeaningReviewGenerator(_gpt_client)
    _open_pinyin_review_generator: OpenPinyinReviewGenerator = OpenPinyinReviewGenerator(_gpt_client)

    _dnd_hanzi_review_generator: DndHanziReviewGenerator = DndHanziReviewGenerator(_gpt_client)
    _dnd_meaning_review_generator: DndMeaningReviewGenerator = DndMeaningReviewGenerator(_gpt_client)
    _dnd_pinyin_review_generator: DndPinyinReviewGenerator = DndPinyinReviewGenerator(_gpt_client)
    _dnd_tone_review_generator: DndToneReviewGenerator = DndToneReviewGenerator(_gpt_client)
    _dnd_paragraph_review_generator: DndParagraphReviewGenerator = DndParagraphReviewGenerator(_gpt_client)
    @classmethod
    def get_review_generator(cls, card_type: CardType, review_type: ReviewType) -> ReviewGeneratorInterface:
        match (card_type, review_type):
            case (CardType.MEANING, ReviewType.MCQ):
                return cls._mcq_meaning_review_generator
            case (CardType.PINYIN, ReviewType.MCQ):
                return cls._mcq_pinyin_review_generator
            case (CardType.TONE, ReviewType.MCQ):
                return cls._mcq_tone_review_generator
            case (CardType.HANZI, ReviewType.MCQ):
                return cls._mcq_hanzi_review_generator
            case (CardType.MEANING, ReviewType.OpenEnded):
                return cls._open_meaning_review_generator
            case (CardType.PINYIN, ReviewType.OpenEnded):
                return cls._open_pinyin_review_generator
            case (CardType.HANZI, ReviewType.DRAG_AND_DROP):
                return cls._dnd_hanzi_review_generator
            case (CardType.MEANING, ReviewType.DRAG_AND_DROP):
                return cls._dnd_meaning_review_generator
            case (CardType.PINYIN, ReviewType.DRAG_AND_DROP):
                return cls._dnd_pinyin_review_generator
            case (CardType.TONE, ReviewType.DRAG_AND_DROP):
                return cls._dnd_tone_review_generator
            case (CardType.PARAGRAPH, ReviewType.DRAG_AND_DROP):
                return cls._dnd_paragraph_review_generator
            case _:
                raise ValueError(f"Unsupported combination of card type {card_type} and review type {review_type}")
            