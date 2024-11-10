from src.db.mysql_db import Database
from src.model.word_model import WordModel
from src.dto import *
from typing import List, Tuple
from aiomysql import Connection, Cursor

class WordRepo:
    instance = None
    def __init__(self, database: Database):
        self.database = database
    
    async def read_word_by_id(self, id: int) -> WordModel:
        conn:Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    'SELECT a.word_id, a.hanzi, a.pinyin, a.meaning, a.hsk_level, a.is_compound, CASE WHEN b.word_id IS NOT NULL THEN TRUE ELSE FALSE END AS is_learnt FROM (SELECT * from word_tab WHERE word_id = %s) a LEFT JOIN (SELECT * from card_tab WHERE word_id = %s) b ON a.word_id = b.word_id',
                    (id, id,)
                )
                fetched = await cur.fetchone()
                if fetched:
                    word = WordModel(
                        word_id=fetched[0],
                        hanzi=fetched[1],
                        pinyin=fetched[2],
                        meaning=fetched[3],
                        hsk_level=fetched[4],
                        is_compound=fetched[5],
                        is_learnt=fetched[6]
                    )
                    return word
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        
        return None
    
    async def get_children_word_list_by_parent_id(self, id:int) -> List[WordModel]:
        conn:Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    '''SELECT 
                    a.word_id, 
                    a.hanzi, 
                    a.pinyin, 
                    a.meaning, 
                    a.hsk_level, 
                    a.is_compound, 
                    CASE WHEN b.word_id IS NOT NULL THEN TRUE ELSE FALSE END AS is_learnt 
                FROM (
                    SELECT * 
                    FROM word_tab a 
                    INNER JOIN (SELECT child_id FROM word_map_tab WHERE parent_id = %s) b 
                    ON a.word_id = b.child_id) a 
                    LEFT JOIN card_tab b ON a.word_id = b.word_id 
                    AND b.word_id = %s;''',
                    (id,id,)
                )
                fetched = await cur.fetchall()
                words = []
                for f in fetched:
                    word = WordModel(
                        word_id=f[0],
                        hanzi=f[1],
                        pinyin=f[2],
                        meaning=f[3],
                        hsk_level=f[4],
                        is_compound=f[5],
                        is_learnt=f[6]
                    )
                    words.append(word)
                return words
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
    
    async def get_parent_word_list_by_child_id(self, id:int) -> List[WordModel]:
        conn:Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    '''SELECT 
                    a.word_id, 
                    a.hanzi, 
                    a.pinyin, 
                    a.meaning, 
                    a.hsk_level, 
                    a.is_compound, 
                    CASE WHEN b.word_id IS NOT NULL THEN TRUE ELSE FALSE END AS is_learnt 
                FROM (
                    SELECT * 
                    FROM word_tab a 
                    INNER JOIN (SELECT parent_id FROM word_map_tab WHERE child_id = %s) b 
                    ON a.word_id = b.parent_id) a 
                    LEFT JOIN card_tab b ON a.word_id = b.word_id 
                    AND b.word_id = %s;''',
                    (id,id,)
                )
                fetched = await cur.fetchall()
                words = []
                for f in fetched:
                    word = WordModel(
                        word_id=f[0],
                        hanzi=f[1],
                        pinyin=f[2],
                        meaning=f[3],
                        hsk_level=f[4],
                        is_compound=f[5],
                        is_learnt=f[6]
                    )
                    words.append(word)
                return words
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)

    async def get_word_list_of_hsk_level(self, level:int, last_id: int, limit:int) -> Tuple[List[WordModel], NextPageMetaDTO]:
        conn:Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    '''SELECT 
                    a.word_id, 
                    a.hanzi, 
                    a.pinyin, 
                    a.meaning, 
                    a.hsk_level, 
                    a.is_compound, 
                    CASE WHEN b.word_id IS NOT NULL THEN TRUE ELSE FALSE END AS is_learnt 
                FROM (
                    SELECT * 
                    FROM word_tab a 
                    WHERE hsk_level = %s AND word_id > %s
                    ORDER BY word_id ASC
                    LIMIT %s) a 
                    LEFT JOIN card_tab b ON a.word_id = b.word_id;''',
                    (level, last_id, limit+1,)
                )
                fetched = await cur.fetchall()
                has_more = len(fetched) > limit
                words = []
                new_last_id = last_id
                for f in fetched:
                    if len(words) == limit:
                        break
                    new_last_id = f[0]
                    word = WordModel(
                        word_id=f[0],
                        hanzi=f[1],
                        pinyin=f[2],
                        meaning=f[3],
                        hsk_level=f[4],
                        is_compound=f[5],
                        is_learnt=f[6]
                    )
                    words.append(word)
                return words, NextPageMetaDTO(last_id=new_last_id, limit=limit, has_more=has_more)
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return [], None

    async def get_word_list_not_learnt(self, last_id:int, limit:int) -> Tuple[List[WordModel], NextPageMetaDTO]:
        conn:Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    '''
                    SELECT 
                        a.word_id, 
                        a.hanzi, 
                        a.pinyin, 
                        a.meaning, 
                        a.hsk_level, 
                        a.is_compound
                    FROM (
                        SELECT * 
                        FROM word_tab 
                        WHERE word_id > %s
                        ORDER BY word_id ASC
                    ) a 
                    LEFT JOIN card_tab b ON a.word_id = b.word_id
                    WHERE b.word_id IS NULL
                    LIMIT %s;
                    ''',
                    (last_id, limit+1,)
                )
                fetched = await cur.fetchall()
                has_more = len(fetched) > limit
                words = []
                new_last_id = last_id
                for f in fetched:
                    if len(words) == limit:
                        break
                    new_last_id = f[0]
                    word = WordModel(
                        word_id=f[0],
                        hanzi=f[1],
                        pinyin=f[2],
                        meaning=f[3],
                        hsk_level=f[4],
                        is_compound=f[5],
                        is_learnt=f[6]
                    )
                    words.append(word)
                return words, NextPageMetaDTO(last_id=new_last_id, limit=limit, has_more=has_more)
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return [], None
    
    async def get_word_list_learnt(self, last_id:int, limit:int) -> Tuple[List[WordModel], NextPageMetaDTO]:
        conn:Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    '''
                    SELECT 
                        a.word_id, 
                        a.hanzi, 
                        a.pinyin, 
                        a.meaning, 
                        a.hsk_level, 
                        a.is_compound
                    FROM (
                        SELECT * 
                        FROM word_tab 
                        WHERE word_id > %s
                        ORDER BY word_id ASC
                    ) a 
                    INNER JOIN card_tab b ON a.word_id = b.word_id
                    LIMIT %s;
                    ''',
                    (last_id, limit+1,)
                )
                fetched = await cur.fetchall()
                has_more = len(fetched) > limit
                words = []
                new_last_id = last_id
                for f in fetched:
                    if len(words) == limit:
                        break
                    new_last_id = f[0]
                    word = WordModel(
                        word_id=f[0],
                        hanzi=f[1],
                        pinyin=f[2],
                        meaning=f[3],
                        hsk_level=f[4],
                        is_compound=f[5],
                        is_learnt=f[6]
                    )
                    words.append(word)
                return words, NextPageMetaDTO(last_id=new_last_id, limit=limit, has_more=has_more)
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return [], None

    async def get_word_list_of_hsk_level(self, level:int, last_id:int, limit:int) -> Tuple[List[WordModel], NextPageMetaDTO]:
        conn:Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    '''SELECT 
                    a.word_id, 
                    a.hanzi, 
                    a.pinyin, 
                    a.meaning, 
                    a.hsk_level, 
                    a.is_compound, 
                    CASE WHEN b.word_id IS NOT NULL THEN TRUE ELSE FALSE END AS is_learnt 
                FROM (
                    SELECT * 
                    FROM word_tab a 
                    WHERE hsk_level = %s AND word_id > %s
                    ORDER BY word_id ASC
                    LIMIT %s) a 
                    LEFT JOIN card_tab b ON a.word_id = b.word_id;''',
                    (level, last_id, limit+1,)
                )
                fetched = await cur.fetchall()
                has_more = len(fetched) > limit
                words = []
                new_last_id = last_id
                for f in fetched:
                    if len(words) == limit:
                        break
                    new_last_id = f[0]
                    word = WordModel(
                        word_id=f[0],
                        hanzi=f[1],
                        pinyin=f[2],
                        meaning=f[3],
                        hsk_level=f[4],
                        is_compound=f[5],
                        is_learnt=f[6]
                    )
                    words.append(word)
                return words, NextPageMetaDTO(last_id=new_last_id, limit=limit, has_more=has_more)
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return [], None

    async def get_word_list(self, last_id:int, limit:int) -> Tuple[List[WordModel], NextPageMetaDTO]:
        conn:Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    '''SELECT 
                    a.word_id, 
                    a.hanzi, 
                    a.pinyin, 
                    a.meaning, 
                    a.hsk_level, 
                    a.is_compound, 
                    CASE WHEN b.word_id IS NOT NULL THEN TRUE ELSE FALSE END AS is_learnt 
                FROM (
                    SELECT * 
                    FROM word_tab a 
                    WHERE word_id > %s
                    ORDER BY word_id ASC
                    LIMIT %s) a 
                    LEFT JOIN card_tab b ON a.word_id = b.word_id;''',
                    (last_id, limit+1,)
                )
                fetched = await cur.fetchall()
                has_more = len(fetched) > limit
                words = []
                new_last_id = last_id
                for f in fetched:
                    if len(words) == limit:
                        break
                    new_last_id = f[0]
                    word = WordModel(
                        word_id=f[0],
                        hanzi=f[1],
                        pinyin=f[2],
                        meaning=f[3],
                        hsk_level=f[4],
                        is_compound=f[5],
                        is_learnt=f[6]
                    )
                    words.append(word)
                return words, NextPageMetaDTO(last_id=new_last_id, limit=limit, has_more=has_more)
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return [], None
    
    async def get_word_list_from_id_list(self, word_id_list: List[int]) -> List[WordModel]:
        conn:Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    '''SELECT 
                    a.word_id, 
                    a.hanzi, 
                    a.pinyin, 
                    a.meaning, 
                    a.hsk_level, 
                    a.is_compound, 
                    CASE WHEN b.word_id IS NOT NULL THEN TRUE ELSE FALSE END AS is_learnt 
                FROM (
                    SELECT * 
                    FROM word_tab a 
                    WHERE word_id IN %s
                    ORDER BY word_id ASC) a 
                    LEFT JOIN card_tab b ON a.word_id = b.word_id;''',
                    (word_id_list,)
                )
                fetched = await cur.fetchall()
                words = []
                for f in fetched:
                    word = WordModel(
                        word_id=f[0],
                        hanzi=f[1],
                        pinyin=f[2],
                        meaning=f[3],
                        hsk_level=f[4],
                        is_compound=f[5],
                        is_learnt=f[6]
                    )
                    words.append(word)
                return words
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return []