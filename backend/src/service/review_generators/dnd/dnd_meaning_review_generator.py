from ..review_generator_interface import ReviewGeneratorInterface
from src.model import *

class DndMeaningReviewGenerator(ReviewGeneratorInterface):
    def is_applicable(self, *word_models: WordModel) -> bool:
        return len(word_models) > 1 and all(word_model.meaning for word_model in word_models)
    async def generate_review_card(self, *word_models: WordModel) -> ReviewContent:
        if len(word_models) <= 1:
            raise ValueError("DndMeaningReviewGenerator must have more than one word model")
        
        answer_map = {}
        for wordModel in word_models:
            word_id = wordModel.word_id
            meaning = wordModel.meaning
            if not word_id or not meaning:
                raise ValueError("DndMeaningReviewGenerator requires a word_id and meaning")
            answer_map[str(word_id)] = meaning


        content = MappedAnswerCardContent(
            question="Map the correct meaning to the word",
            allow_hanzi=True,
            allow_pinyin=True,
            allow_meaning=False,
            allow_tone=True,
            answer_map=answer_map,
        )
        return content
