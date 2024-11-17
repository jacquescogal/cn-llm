from src.db.mysql_db import Database
from src.model import *
from typing import List
from aiomysql import Connection, Cursor
from src.dto import *
from typing import List, Tuple

class CardRepo:
    instance = None
    def __init__(self, database: Database):
        self.database = database
    
    async def create_card(self, card: CardModel) -> CardModel:
        conn: Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    'INSERT INTO card_tab (word_id, card_type, due_dt_unix, stability, difficulty, elapsed_days, scheduled_days, reps, lapses, card_state, last_review_dt_unix, is_disabled) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (
                        card.word_id,
                        card.card_type.value,
                        card.due_dt_unix,
                        card.stability_int,
                        card.difficulty_int,
                        card.elapsed_days,
                        card.scheduled_days,
                        card.reps,
                        card.lapses,
                        card.state,
                        card.last_review_dt_unix,
                        card.is_disabled
                    )
                )  
                await conn.commit()
                return card
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return None
    
    async def read_card_of_type(self, word_id: int, card_type: CardType) -> CardModel:
        conn: Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    'SELECT word_id, card_type, due_dt_unix, stability, difficulty, elapsed_days, scheduled_days, reps, lapses, card_state, last_review_dt_unix, is_disabled FROM card_tab WHERE word_id = %s AND card_type = %s',
                    (word_id, card_type.value)
                )
                fetched = await cur.fetchone()
                if fetched:
                    card = CardModel(
                        word_id=fetched[0],
                        card_type=fetched[1],
                        due_dt_unix=fetched[2],
                        stability_int=fetched[3],
                        difficulty_int=fetched[4],
                        elapsed_days=fetched[5],
                        scheduled_days=fetched[6],
                        reps=fetched[7],
                        lapses=fetched[8],
                        state=fetched[9],
                        last_review_dt_unix=fetched[10],
                        is_disabled=fetched[11]
                    )
                    return card
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return None
    
    async def read_card_list_by_word_id(self, word_id: int) -> List[CardModel]:
        conn: Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    'SELECT word_id, card_type, due_dt_unix, stability, difficulty, elapsed_days, scheduled_days, reps, lapses, card_state, last_review_dt_unix, is_disabled FROM card_tab WHERE word_id = %s',
                    (word_id,)
                )
                fetched = await cur.fetchall()
                cards = []
                for f in fetched:
                    card = CardModel(
                        word_id=f[0],
                        card_type=f[1],
                        due_dt_unix=f[2],
                        stability_int=f[3],
                        difficulty_int=f[4],
                        elapsed_days=f[5],
                        scheduled_days=f[6],
                        reps=f[7],
                        lapses=f[8],
                        state=f[9],
                        last_review_dt_unix=f[10],
                        is_disabled=f[11]
                    )
                    cards.append(card)
                return cards
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return None
    
    async def update_card(self, card: CardModel) -> bool:
        conn: Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    'UPDATE card_tab SET due_dt_unix=%s, stability=%s, difficulty=%s, elapsed_days=%s, scheduled_days=%s, reps=%s, lapses=%s, card_state=%s, last_review_dt_unix=%s, is_disabled=%s WHERE word_id=%s AND card_type=%s',
                    (
                        card.due_dt_unix,
                        card.stability_int,
                        card.difficulty_int,
                        card.elapsed_days,
                        card.scheduled_days,
                        card.reps,
                        card.lapses,
                        card.state,
                        card.last_review_dt_unix,
                        card.is_disabled,
                        card.word_id,
                        card.card_type.value
                    )
                )
                await conn.commit()
                return True
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return False
    
    async def get_scheduled_card_list(self, limit:int) -> List[CardModel]:
        conn: Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    'SELECT word_id, card_type, due_dt_unix, stability, difficulty, elapsed_days, scheduled_days, reps, lapses, card_state, last_review_dt_unix, is_disabled FROM card_tab WHERE is_disabled=false ORDER BY due_dt_unix ASC LIMIT %s',
                    (limit,)
                )
                fetched = await cur.fetchall()
                cards = []
                for f in fetched:
                    card = CardModel(
                        word_id=f[0],
                        card_type=f[1],
                        due_dt_unix=f[2],
                        stability_int=f[3],
                        difficulty_int=f[4],
                        elapsed_days=f[5],
                        scheduled_days=f[6],
                        reps=f[7],
                        lapses=f[8],
                        state=f[9],
                        last_review_dt_unix=f[10],
                        is_disabled=f[11]
                    )
                    cards.append(card)
                return cards
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return []
        
    async def get_due_card_list(self) -> List[CardModel]:
        conn: Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    'SELECT word_id, card_type, due_dt_unix, stability, difficulty, elapsed_days, scheduled_days, reps, lapses, card_state, last_review_dt_unix, is_disabled FROM card_tab WHERE is_disabled=false AND due_dt_unix <= UNIX_TIMESTAMP()'
                )
                fetched = await cur.fetchall()
                cards = []
                for f in fetched:
                    card = CardModel(
                        word_id=f[0],
                        card_type=f[1],
                        due_dt_unix=f[2],
                        stability_int=f[3],
                        difficulty_int=f[4],
                        elapsed_days=f[5],
                        scheduled_days=f[6],
                        reps=f[7],
                        lapses=f[8],
                        state=f[9],
                        last_review_dt_unix=f[10],
                        is_disabled=f[11]
                    )
                    cards.append(card)
                return cards
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return []
    
    async def get_card_list(self, offset:int, limit:int) -> Tuple[List[CardModel], PageMeta]:
        conn: Connection = await self.database.get_conn()
        try:
            async with conn.cursor() as cur:
                await cur.execute(
                    'SELECT card_id, word_id, due_dt_unix, stability, difficulty, elapsed_days, scheduled_days, reps, lapses, card_state, last_review_dt_unix FROM card_tab ORDER BY card_id ASC LIMIT %s OFFSET %s',
                    (limit+1, offset)
                )
                fetched = await cur.fetchall()
                has_more = False
                if len(fetched) > limit:
                    has_more = True
                cards = []
                for f in fetched:
                    if len(cards) == limit:
                        break
                    card = CardModel(
                        card_id=f[0],
                        word_id=f[1],
                        due_dt_unix=f[2],
                        stability_int=f[3],
                        difficulty_int=f[4],
                        elapsed_days=f[5],
                        scheduled_days=f[6],
                        reps=f[7],
                        lapses=f[8],
                        state=f[9],
                        last_review_dt_unix=f[10]
                    )
                    cards.append(card)
                return cards, PageMeta(offset=offset+len(cards), limit=limit, has_more=has_more)
        finally:
            # Release the connection back to the pool
            await self.database.release_connection(conn)
        return [], None