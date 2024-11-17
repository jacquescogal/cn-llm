from abc import ABC, abstractmethod
from src.enums import QuestionType
from src.repos import *
from typing import Dict
class QuestionControllerFactory:
    @staticmethod
    def get_controller(question_type:QuestionType, word_repo: WordRepo, word_id: int) -> 'QuestionController':
        mapping:Dict[QuestionType, QuestionController] = {
            QuestionType.MEANING: MeaningQuestionController,
            QuestionType.PINYIN: PinyinQuestionController,
            QuestionType.HANZI: HanziQuestionController,
            QuestionType.MCQ: McqQuestionController,
            QuestionType.OCR: OcrQuestionController,
        }
        return mapping[question_type](word_repo, word_id)

class QuestionController(ABC):
    def __init__(self, word_repo: WordRepo, word_id: int):
        self.word_repo = word_repo
        self.word_id = word_id

    @abstractmethod
    def get_question_json(self) -> str:
        pass

    @abstractmethod
    def evaluate_answer(self, question_json: str, answer: any) -> int:
        """returns a fuzzy score [0, 100]"""
        pass

class MeaningQuestionController(QuestionController):
    def get_question_json(self) -> str:
        pass
    
    def evaluate_answer(self, question_json: str, answer: any) -> int:
        pass

