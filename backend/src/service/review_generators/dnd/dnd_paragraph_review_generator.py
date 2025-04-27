from ..review_generator_interface import ReviewGeneratorInterface
from src.model import *

class DndParagraphReviewGenerator(ReviewGeneratorInterface):
    def is_applicable(self, *word_models: WordModel) -> bool:
        return len(word_models) > 1 and all(word_model.hanzi for word_model in word_models)
    async def generate_review_card(self, *word_models: WordModel) -> ReviewContent:
        if len(word_models) <2:
            raise ValueError("DndParagraphReviewGenerator must have more than one word model")

        # hanzi list
        hanzi_list = []
        for wordModel in word_models:
            hanzi = wordModel.hanzi
            if not hanzi:
                raise ValueError("DndParagraphReviewGenerator requires a hanzi")
            hanzi_list.append(hanzi)
                
        response = await self.client.responses.create(
            model=self.model,
            input=[
                {"role": "system", "content": " paragraph"},
                {"role": "user", "content": f"Make a paragraph with the following words: {', '.join(hanzi_list)}. The paragraph should be in Chinese and should have a cloze question for each word at least once. The word can be an answer for multiple cloze question boxes. The cloze question box should be in the format of %hanzi_word% meaning that the answer is contained in between the % symbols. The paragraph should be in Chinese and should be a coherent paragraph. The paragraph should be at least 3 sentences long. The paragraph should be simple and easy to understand."}
            ],
            text={
                "format": {
                    "type": "json_schema",
                    "name": "cloze_question_paragraph",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "paragraph": {
                                "type": "string"
                            },
                        },
                        "required": ["paragraph"],
                        "additionalProperties": False
                    },
                    "strict": True
                }
            }
        )
        event = json.loads(response.output_text)

        paragraph = event["paragraph"]
        para_split = paragraph.split("%")
        answer_list = []
        template_list = []
        for substring in para_split:
            if substring in hanzi_list:
                answer_list.append(substring)
            else:
                template_list.append(substring)
                
        content = OrderedAnswerCardContent(
            question=f"Drag the correct word to the answer boxes.",
            allow_hanzi=True,
            allow_pinyin=True,
            allow_meaning=True,
            allow_tone=True,
            template= "%".join(template_list),
            answer_list=answer_list,
        )
        return content
    
