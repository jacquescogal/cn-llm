from src.enums import *
from src.model import *

VALID_QUESTION_TYPES = [QuestionType.OpenEnded, QuestionType.SingleSelect, QuestionType.MultiSelect]
VALID_REVIEW_TYPES = [ReviewType.OpenEnded, ReviewType.SingleSelect, ReviewType.MultiSelect]
VALID_CARD_REVIEW_COMBINATIONS = {
    CardType.MEANING: [ReviewType.OpenEnded, ReviewType.MCQ],
    CardType.PINYIN: [ReviewType.OpenEnded, ReviewType.MCQ, ReviewType.DRAG_AND_DROP],
    CardType.HANZI: [ReviewType.MCQ, ReviewType.OCR, ReviewType.DRAG_AND_DROP],
    CardType.TONE: [ReviewType.MCQ, ReviewType.DRAG_AND_DROP],
    CardType.PARAGRAPH: [ReviewType.OpenEnded, ReviewType.DRAG_AND_DROP],
}