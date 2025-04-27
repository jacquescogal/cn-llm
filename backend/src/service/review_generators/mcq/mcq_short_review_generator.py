from ..review_generator_interface import ReviewGeneratorInterface
from src.model import *
from src.util import *

class MCQShortReviewGenerator(ReviewGeneratorInterface):
    def is_applicable(self, *word_models: WordModel) -> bool:
        # Check if the word models have a hanzi and pinyin
        return len(word_models) == 1
    async def generate_review_card(self, *word_models: WordModel) -> ReviewContent:
        # validae the len(word_models) == 1
        if len(word_models) != 1:
            raise ValueError("MCQShortReviewGenerator only supports one word model at a time")
        wordModel = word_models[0]
        
        hanzi = wordModel.hanzi
        if not hanzi:
            raise ValueError("MCQShortReviewGenerator requires a hanzi")

        response = await self.client.responses.create(
            model=self.model,
            input=[
                {"role": "system", "content": "Make a chinese cloze question sentence"},
                {"role": "user", "content": f"Make a sentence with the following word: {hanzi}. The sentence should be in Chinese and should have a cloze question for the word. The cloze question box should be in the format of %hanzi_word% meaning that the answer is contained in between the % symbols. The sentence should be in Chinese and should be a coherent sentence. The sentence should be simple and easy to understand. Also, provide 3 other wrong hanzi options."},
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "cloze_question_sentence",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "paragraph": {
                                "type": "string"
                            },
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
                        "required": ["paragraph", "wrong_option_1", "wrong_option_2", "wrong_option_3"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            }
        )
        event = json.loads(response.output_text)
        paragraph = event["paragraph"]
        para_split = paragraph.split("%")
        template_list = []
        for substring in para_split:
            if substring == hanzi:
                continue
            else:
                template_list.append(substring)
        
        content = SingleAnswerCardContent(
            question='%'.join(template_list),
            answer=hanzi,
            allow_hanzi=True,
            allow_pinyin=True,
            allow_meaning=True,
            allow_tone=True,
            wrong_options=[
                event["wrong_option_1"],
                event["wrong_option_2"],
                event["wrong_option_3"],
            ]
        )
        return content