from ..review_generator_interface import ReviewGeneratorInterface
from src.model import *

class DndPinyinReviewGenerator(ReviewGeneratorInterface):
    def is_applicable(self, *word_models: WordModel) -> bool:
        return len(word_models) > 1 and all(word_model.pinyin for word_model in word_models)
    async def generate_review_card(self, *word_models: WordModel) -> ReviewContent:
        if len(word_models) <= 1:
            raise ValueError("DndPinyinReviewGenerator must have more than one word model")
        
        answer_map = {}
        for wordModel in word_models:
            word_id = wordModel.word_id
            pinyin = wordModel.pinyin
            if not word_id or not pinyin:
                raise ValueError("DndPinyinReviewGenerator requires a word_id and pinyin")
            answer_map[str(word_id)] = pinyin


        content = MappedAnswerCardContent(
            question="Map the correct pinyin to the word",
            allow_hanzi=True,
            allow_pinyin=False,
            allow_meaning=True,
            allow_tone=False,
            answer_map=answer_map,
        )
        return content
