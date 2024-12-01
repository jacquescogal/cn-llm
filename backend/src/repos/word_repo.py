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
                    'SELECT a.word_id, a.hanzi, a.pinyin, a.meaning, a.hsk_level, a.is_compound, CASE WHEN b.word_id IS NOT NULL THEN TRUE ELSE FALSE END AS is_learnt FROM (SELECT * from word_tab WHERE word_id = %s) a LEFT JOIN (SELECT * from card_word_map_tab WHERE word_id = %s) b ON a.word_id = b.word_id',
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
                    LEFT JOIN card_word_map_tab b ON a.word_id = b.word_id 
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
                    LEFT JOIN card_word_map_tab b ON a.word_id = b.word_id 
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

    async def get_word_list_of_hsk_level(self, level:int, offset: int, limit:int) -> Tuple[List[WordModel], PageMeta]:
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
                    WHERE hsk_level = %s
                    ORDER BY word_id ASC
                    LIMIT %s OFFSET %s) a
                    LEFT JOIN card_word_map_tab b ON a.word_id = b.word_id;''',
                    (level, limit+1, offset,)
                )
                fetched = await cur.fetchall()
                has_more = len(fetched) > limit
                words = []
                for f in fetched:
                    if len(words) == limit:
                        break
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
                return words, PageMeta(offset=offset+len(words), limit=limit, has_more=has_more)
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return [], None

    async def get_word_list_not_learnt(self, offset:int, limit:int) -> Tuple[List[WordModel], PageMeta]:
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
                        ORDER BY word_id ASC
                    ) a 
                    LEFT JOIN card_word_map_tab b ON a.word_id = b.word_id
                    WHERE b.word_id IS NULL
                    LIMIT %s OFFSET %s;
                    ''',
                    (limit+1, offset,)
                )
                fetched = await cur.fetchall()
                has_more = len(fetched) > limit
                words = []
                for f in fetched:
                    if len(words) == limit:
                        break
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
                return words, PageMeta(offset=offset+len(words), limit=limit, has_more=has_more)
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return [], None
    
    async def get_word_list_learnt(self, offset:int, limit:int) -> Tuple[List[WordModel], PageMeta]:
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
                        ORDER BY word_id ASC
                    ) a 
                    INNER JOIN card_word_map_tab b ON a.word_id = b.word_id
                    LIMIT %s OFFSET %s;
                    ''',
                    (limit+1, offset,)
                )
                fetched = await cur.fetchall()
                has_more = len(fetched) > limit
                words = []
                for f in fetched:
                    if len(words) == limit:
                        break
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
                return words, PageMeta(offset=offset+len(words), limit=limit, has_more=has_more)
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return [], None

    async def get_word_list_of_hsk_level(self, level:int, offset:int, limit:int) -> Tuple[List[WordModel], PageMeta]:
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
                    WHERE hsk_level = %s
                    ORDER BY word_id ASC
                    LIMIT %s OFFSET %s) a
                    LEFT JOIN card_word_map_tab b ON a.word_id = b.word_id;''',
                    (level, limit+1, offset,)
                )
                fetched = await cur.fetchall()
                has_more = len(fetched) > limit
                words = []
                for f in fetched:
                    if len(words) == limit:
                        break
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
                return words, PageMeta(offset=offset+len(words), limit=limit, has_more=has_more)
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
                    LEFT JOIN card_word_map_tab b ON a.word_id = b.word_id;''',
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
    async def get_word_list(self, hsk_filter: List[int], learnt_filter: bool, offset:int, limit:int) -> Tuple[List[WordModel], PageMeta]:
        conn:Connection = await self.database.get_conn()
        hsk_filter_str = ""
        if hsk_filter:
            placeholders = ', '.join(['%s'] * len(hsk_filter))
            hsk_filter_str = f"a.hsk_level IN ({placeholders})"

        learnt_filter_str = {
            True: "b.word_id IS NOT NULL",
            False: "b.word_id IS NULL",
        }.get(learnt_filter, "")
        if len(learnt_filter_str) > 0:
            if (len(hsk_filter_str) > 0):
                learnt_filter_str = "AND " + learnt_filter_str
            else:
                learnt_filter_str = "WHERE " + learnt_filter_str
        if len(hsk_filter_str) > 0:
            hsk_filter_str = "WHERE " + hsk_filter_str
        try:
            async with conn.cursor() as cur:
                query = f'''SELECT 
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
                    ORDER BY word_id ASC) a
                    LEFT JOIN (SELECT word_id from card_word_map_tab GROUP BY word_id) b ON a.word_id = b.word_id
                    {hsk_filter_str}
                    {learnt_filter_str}
                    LIMIT %s OFFSET %s;'''
                params = []
                if hsk_filter:
                    params.extend(hsk_filter)
                params.extend([limit + 1, offset])

                await cur.execute(query, params)

                fetched = await cur.fetchall()
                has_more = len(fetched) > limit
                words = []
                for f in fetched:
                    if len(words) == limit:
                        break
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
                return words, PageMeta(offset=offset + len(words), limit=limit, has_more=has_more)
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return [], None
    
    async def get_word_list_from_key_word_search(self,  key_word: str, hsk_filter: List[int], learnt_filter: bool,offset:int, limit:int) -> Tuple[List[WordModel], PageMeta]:
        conn:Connection = await self.database.get_conn()
        hsk_filter_str = ""
        if hsk_filter:
            placeholders = ', '.join(['%s'] * len(hsk_filter))
            hsk_filter_str = f"hsk_level IN ({placeholders})"

        learnt_filter_str = {
            True: "b.word_id IS NOT NULL",
            False: "b.word_id IS NULL",
        }.get(learnt_filter, "")
        if len(learnt_filter_str) > 0:
            learnt_filter_str = "WHERE " + learnt_filter_str
        if len(hsk_filter_str) > 0:
            hsk_filter_str = "AND " + hsk_filter_str
        try:
            async with conn.cursor() as cur:
                query = f'''
                    SELECT 
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
                        WHERE (hanzi LIKE %s OR pinyin LIKE %s OR pinyin LIKE %s)
                        {hsk_filter_str}
                        ORDER BY word_id ASC
                        LIMIT %s OFFSET %s
                    ) a
                    LEFT JOIN (SELECT word_id from card_word_map_tab GROUP BY word_id) b ON a.word_id = b.word_id
                    {learnt_filter_str};
                '''
                print(query)

                # Parameters: key_word, hsk_list, limit, offset
                params = [f'%{key_word}%', f'{key_word}%', f'% {key_word}%']
                if hsk_filter:
                    params.extend(hsk_filter)
                params.extend([limit + 1, offset])

                await cur.execute(query, params)
                fetched = await cur.fetchall()
                has_more = len(fetched) > limit
                words = []
                for f in fetched:
                    if len(words) == limit:
                        break
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
                return words, PageMeta(offset=offset+len(words), limit=limit, has_more=has_more)
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return [], None