from src.constants.enums import *
from src.model import *

VALID_REVIEW_COMBINATIONS = {
    CardType.MEANING: set([ReviewType.OpenEnded, ReviewType.MCQ, ReviewType.DRAG_AND_DROP]),
    CardType.PINYIN: set([ReviewType.OpenEnded, ReviewType.MCQ, ReviewType.DRAG_AND_DROP]),
    CardType.HANZI: set([ReviewType.MCQ, ReviewType.DRAG_AND_DROP]),
    CardType.TONE: set([ReviewType.MCQ, ReviewType.DRAG_AND_DROP]),
    CardType.PARAGRAPH: set([ReviewType.DRAG_AND_DROP]),
    CardType.SHORT_PARAGRAPH: set([ReviewType.MCQ]),
}

MULTI_WORD_CONTENT_MAP = {
    (CardType.MEANING, ReviewType.DRAG_AND_DROP): MappedAnswerCardContent,
    (CardType.PINYIN, ReviewType.DRAG_AND_DROP): MappedAnswerCardContent,
    (CardType.HANZI, ReviewType.DRAG_AND_DROP): MappedAnswerCardContent,
    (CardType.PARAGRAPH, ReviewType.DRAG_AND_DROP): OrderedAnswerCardContent,
}