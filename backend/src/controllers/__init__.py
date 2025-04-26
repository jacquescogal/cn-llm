from src.repos import *
from src.controllers.word_controller import WordController
from src.controllers.card_controller import CardController
from src.controllers.review_controller import ReviewController
from src.service.review_generators import *

word_controller = WordController(word_repo = word_repo)
card_controller = CardController(card_repo = card_repo, word_repo = word_repo, card_word_map_repo = card_word_map_repo, review_generator_factory = review_generator_factory)
review_controller = ReviewController(card_repo = card_repo, word_repo = word_repo, card_word_map_repo = card_word_map_repo)
