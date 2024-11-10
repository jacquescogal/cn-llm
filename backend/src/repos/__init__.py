from src.db.mysql_db import Database
from src.repos.word_repo import WordRepo
from src.repos.card_repo import CardRepo

database = Database()
word_repo = WordRepo(database)
card_repo = CardRepo(database)