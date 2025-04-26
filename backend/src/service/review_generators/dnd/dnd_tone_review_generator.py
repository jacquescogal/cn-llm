from ..review_generator_interface import ReviewGeneratorInterface
from src.model import *
from src.util import *

class DndToneReviewGenerator(ReviewGeneratorInterface):
    def is_applicable(self, *word_models: WordModel) -> bool:
        return len(word_models) == 1 and count_tones(word_models[0].pinyin) > 1
    
    async def generate_review_card(self, *word_models: WordModel) -> ReviewContent:
        if len(word_models) > 1 or count_tones(word_models[0].pinyin) < 2:
            raise ValueError("DndToneReviewGenerator must have only one word model with more than one tone")
        word_model = word_models[0]
        tone_to_char_map = get_tone_to_char_map()
        answer_map = {}
        for i in range(len(word_model.pinyin)):
            tone = tone_to_char_map.get(word_model.pinyin[i], None)
            if not tone:
                continue
            answer_map[str(i)] = word_model.pinyin[i]

        content = SingleAnswerCardContent(
            question="Map the correct tone to the pinyin",
            allow_hanzi=True,
            allow_pinyin=True,
            allow_meaning=True,
            allow_tone=False,
            answer=word_model.pinyin,
            answer_map=answer_map,
        )
        return content
