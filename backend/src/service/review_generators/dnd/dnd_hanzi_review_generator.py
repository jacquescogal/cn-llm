from ..review_generator_interface import ReviewGeneratorInterface
from src.model import *

class DndHanziReviewGenerator(ReviewGeneratorInterface):
    def is_applicable(self, *word_models: WordModel) -> bool:
        return len(word_models) > 1 and all(word_model.hanzi for word_model in word_models)
    
    async def generate_review_card(self, *word_models: WordModel) -> ReviewContent:
        if len(word_models) <= 1:
            raise ValueError("DndHanziReviewGenerator must have more than one word model")
        
        answer_map = {}
        for wordModel in word_models:
            word_id = wordModel.word_id
            hanzi = wordModel.hanzi
            if not word_id or not hanzi:
                raise ValueError("DndHanziReviewGenerator requires a word_id and hanzi")
            answer_map[str(word_id)] = hanzi


        content = MappedAnswerCardContent(
            question="Map the correct hanzi",
            allow_hanzi=False,
            allow_pinyin=True,
            allow_meaning=True,
            allow_tone=True,
            answer_map=answer_map,
        )
        return content
