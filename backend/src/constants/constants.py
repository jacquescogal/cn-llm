from src.enums import *
from src.model import *

VALID_REVIEW_COMBINATIONS = {
    CardType.MEANING: set([ReviewType.OpenEnded, ReviewType.MCQ, ReviewType.DRAG_AND_DROP]),
    CardType.PINYIN: set([ReviewType.OpenEnded, ReviewType.MCQ, ReviewType.DRAG_AND_DROP]),
    CardType.HANZI: set([ReviewType.MCQ, ReviewType.OCR, ReviewType.DRAG_AND_DROP]),
    CardType.TONE: set([ReviewType.MCQ, ReviewType.DRAG_AND_DROP]),
    CardType.PARAGRAPH: set([ReviewType.OpenEnded, ReviewType.DRAG_AND_DROP]),
}

MULTI_WORD_CONTENT_MAP = {
    (CardType.PARAGRAPH, ReviewType.DRAG_AND_DROP): OrderedAnswerCardContent,
    (CardType.PARAGRAPH, ReviewType.OpenEnded): OrderedAnswerCardContent,
    (CardType.MEANING, ReviewType.DRAG_AND_DROP): OrderedAnswerCardContent,
}