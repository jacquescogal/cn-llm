from .db.mysql_db import Database
from .word_repo import WordRepo
from .card_repo import CardRepo
from .card_word_map_repo import CardWordMapRepo

database = Database()
word_repo = WordRepo(database)
card_repo = CardRepo(database)
card_word_map_repo = CardWordMapRepo(database)