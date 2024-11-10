from src.repos import *
from src.controllers.word_controller import WordController
from src.controllers.card_controller import CardController

word_controller = WordController(word_repo = word_repo)
card_controller = CardController(card_repo = card_repo, word_repo = word_repo)