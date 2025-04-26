from ..review_generator_interface import ReviewGeneratorInterface
from src.model import *

class OpenMeaningReviewGenerator(ReviewGeneratorInterface):
    def is_applicable(self, *word_models: WordModel) -> bool:
        return len(word_models) == 1 and word_models[0].meaning is not None
    async def generate_review_card(self, *word_models: WordModel) -> ReviewContent:
        # validae the len(word_models) == 1
        if len(word_models) != 1:
            raise ValueError("OpenMeaningReviewGenerator only supports one word model at a time")
        wordModel = word_models[0]
        
        answer = wordModel.meaning
        if not answer:
            raise ValueError("OpenMeaningReviewGenerator requires a meaning")
        
        content = SingleAnswerCardContent(
            question=f"What is the meaning of '{wordModel.hanzi}'?",
            answer=answer,
            allow_hanzi=True,
            allow_pinyin=True,
            allow_meaning=False,
            allow_tone=True,
            wrong_options=None
        )
        return content
