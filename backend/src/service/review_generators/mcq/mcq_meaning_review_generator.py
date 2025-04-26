from ..review_generator_interface import ReviewGeneratorInterface
from src.model import *

class MCQMeaningReviewGenerator(ReviewGeneratorInterface):
    def is_applicable(self, *word_models: WordModel) -> bool:
        # Check if the word models have a hanzi and meaning
        return len(word_models) == 1 and all(word_model.hanzi and word_model.meaning for word_model in word_models)
    async def generate_review_card(self, *word_models: WordModel) -> ReviewContent:
        # validae the len(word_models) == 1
        if len(word_models) != 1:
            raise ValueError("MCQMeaningReviewGenerator only supports one word model at a time")
        wordModel = word_models[0]
        
        hanzi = wordModel.hanzi
        meaning = wordModel.meaning
        if not hanzi or not meaning:
            raise ValueError("MCQMeaningReviewGenerator requires a hanzi and meaning")

        response = await self.client.responses.create(
            model=self.model,
            input=[
                {"role": "system", "content": "Make MCQ choices"},
                {"role": "user", "content": f"3 other wrong english definition options for the chinese word '{hanzi}' which means '{meaning}'"},
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "mcq_wrong_options",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "wrong_option_1": {
                                "type": "string"
                            },
                            "wrong_option_2": {
                                "type": "string"
                            },
                            "wrong_option_3": {
                                "type": "string"
                            },
                        },
                        "required": ["wrong_option_1", "wrong_option_2", "wrong_option_3"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            }
        )
        event = json.loads(response.output_text)
        
        content = SingleAnswerCardContent(
            question=f"Which is the correct meaning?",
            answer=meaning,
            allow_hanzi=True,
            allow_pinyin=True,
            allow_meaning=False,
            allow_tone=True,
            wrong_options=[
                event["wrong_option_1"],
                event["wrong_option_2"],
                event["wrong_option_3"],
            ]
        )
        return content