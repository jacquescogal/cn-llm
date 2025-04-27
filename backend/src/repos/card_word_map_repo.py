from src.repos.db.mysql_db import Database
from src.model import *
from typing import List
from aiomysql import Connection, Cursor
from src.model.dto import *
from typing import List, Tuple

class CardWordMapRepo:
    instance = None
    def __init__(self, database: Database):
        self.database = database
    
    async def create_card_word_mapping(self, card_word_map: CardWordMapModel) -> CardWordMapModel:
        conn: Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    'INSERT INTO card_word_map_tab (card_id, word_id, is_singular) VALUES (%s, %s, %s)',
                    (
                        card_word_map.card_id,
                        card_word_map.word_id,
                        card_word_map.is_singular
                    )
                )
                # commit and get the last inserted id
                await conn.commit()
                return card_word_map
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return None
    
    async def create_card_word_mapping_list(self, card_word_map_list: List[CardWordMapModel]) -> List[CardWordMapModel]:
        conn: Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                for card_word_map in card_word_map_list:
                    await cur.execute(
                        'INSERT INTO card_word_map_tab (card_id, word_id, is_singular) VALUES (%s, %s, %s)',
                        (
                            card_word_map.card_id,
                            card_word_map.word_id,
                            card_word_map.is_singular
                        )
                    )
                #
                await conn.commit()
                return card_word_map_list
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return None
    
    async def read_card_word_mapping_by_card_id(self, card_id: int) -> List[CardWordMapModel]:
        conn: Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    'SELECT * FROM card_word_map_tab WHERE card_id = %s',
                    (card_id)
                )
                card_word_map_list = []
                async for row in cur:
                    card_word_map_list.append(CardWordMapModel(
                        card_id=row[0],
                        word_id=row[1],
                        is_singular=row[2]
                    ))
                return card_word_map_list
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return None
    
    async def read_card_word_mapping_by_word_id(self, word_id: int) -> List[CardWordMapModel]:
        conn: Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    'SELECT * FROM card_word_map_tab WHERE word_id = %s',
                    (word_id)
                )
                card_word_map_list = []
                async for row in cur:
                    card_word_map_list.append(CardWordMapModel(
                        card_id=row[0],
                        word_id=row[1],
                        is_singular=row[2]
                    ))
                return card_word_map_list
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return None
    
    async def read_card_word_mapping_by_word_id_singular(self, word_id: int, is_singular: bool = True) -> List[CardWordMapModel]:
        conn: Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    'SELECT * FROM card_word_map_tab WHERE word_id = %s AND is_singular = %s',
                    (word_id, is_singular)
                )
                card_word_map_list = []
                async for row in cur:
                    card_word_map_list.append(CardWordMapModel(
                        card_id=row[0],
                        word_id=row[1],
                        is_singular=row[2]
                    ))
                return card_word_map_list
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return None