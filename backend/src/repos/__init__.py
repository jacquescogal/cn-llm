from src.db.mysql_db import Database
from src.repos.word_repo import WordRepo
from src.repos.card_repo import CardRepo
from src.repos.card_word_map_repo import CardWordMapRepo

database = Database()
word_repo = WordRepo(database)
card_repo = CardRepo(database)
card_word_map_repo = CardWordMapRepo(database)