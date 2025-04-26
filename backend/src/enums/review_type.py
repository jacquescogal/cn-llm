from enum import Enum

class ReviewType(Enum):
    # respond with text input
    OpenEnded = 1
    # choose from list of options
    MCQ = 2

    # # respond with drawing then OCR
    # OCR = 3

    # Some uses:
    # 1. for paragraph type, generate a paragraph with extracted words that need to be dragged and dropped into the correct order
    # ?? how to select words (perhaps use the last 5 due cards -> an issue is that the paragraph may not be coherent)
    # 2. for hanzi composites, drag and drop the components into the correct order
    # 3. for tone, drag and drop the tone mark into the correct position
    DRAG_AND_DROP = 3
