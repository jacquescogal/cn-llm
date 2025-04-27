from .bot import *
from .review_generators import *
from .card.card_service import CardService
from .review.review_service import ReviewService
from .word.word_service import WordService
from src.repos import *


review_generator_factory = ReviewGeneratorFactory()
word_service =  WordService(word_repo)
card_service = CardService(card_repo, word_repo, card_word_map_repo, review_generator_factory)
review_service = ReviewService(card_repo, word_repo, card_word_map_repo)