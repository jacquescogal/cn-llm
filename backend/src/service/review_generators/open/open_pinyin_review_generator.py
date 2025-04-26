from ..review_generator_interface import ReviewGeneratorInterface
from src.model import *

class OpenPinyinReviewGenerator(ReviewGeneratorInterface):
    def is_applicable(self, *word_models: WordModel) -> bool:
        return len(word_models) == 1 and word_models[0].pinyin is not None
    async def generate_review_card(self, *word_models: WordModel) -> ReviewContent:
        # validae the len(word_models) == 1
        if len(word_models) != 1:
            raise ValueError("OpenPinyinReviewGenerator only supports one word model at a time")
        wordModel = word_models[0]
        
        answer = wordModel.pinyin
        if not answer:
            raise ValueError("OpenPinyinReviewGenerator requires a pinyin")
        
        content = SingleAnswerCardContent(
            question=f"What is the pinyin of '{wordModel.hanzi}'?",
            answer=answer,
            allow_hanzi=True,
            allow_pinyin=False,
            allow_meaning=True,
            allow_tone=False,
            wrong_options=None
        )
        return content
